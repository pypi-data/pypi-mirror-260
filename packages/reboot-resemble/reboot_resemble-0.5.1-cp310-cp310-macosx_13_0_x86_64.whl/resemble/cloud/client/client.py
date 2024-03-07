from resemble.aio.errors import SystemAborted
from resemble.aio.workflows import Workflow
from resemble.cloud.secret_id import SecretId
from resemble.cloud.v1alpha1.auth.auth_rsm import APIKey
from resemble.cloud.v1alpha1.secrets.secrets_rsm import (
    DeleteTaskResponse,
    NotFoundError,
    Secret,
    WriteTaskResponse,
)
from resemble.naming import UserId
from resemble.v1alpha1.errors_pb2 import ActorNotConstructed
from typing import Optional


async def secret_read(
    workflow: Workflow,
    user_id: UserId,
    secret_name: str,
) -> Optional[bytes]:
    secret = _secret(user_id, secret_name)
    try:
        response = await secret.Read(workflow)
    except Secret.ReadAborted as aborted:
        match aborted.error:
            case NotFoundError():  # type: ignore[misc]
                return None
            case _:
                # NOTE: this is actually unreachable (as of the time
                # this comment was written), i.e., the only declared
                # error in `Sercret.Read` is `NotFoundError`.
                # Unfortunately without "mypy protobuf" support, mypy
                # thinks that `NotFoundError` is of type `Any` and
                # thus it both (1) requires that we add a `type:
                # ignore[misc]` and (2) requires this default `case
                # _`.
                raise
    except SystemAborted as aborted:
        match aborted.error:
            case ActorNotConstructed():  # type: ignore[misc]
                return None
            case _:
                raise
    else:
        return response.data


async def secret_write(
    workflow: Workflow, user_id: UserId, secret_name: str, secret_value: bytes
) -> None:
    secret = _secret(user_id, secret_name)
    write_response = await secret.Write(workflow, data=secret_value)
    write_task_response = await workflow.future_from_task_id(
        task_id=write_response.task_id, response_type=WriteTaskResponse
    )
    if write_task_response.HasField('error'):
        # TODO: See `SecretServicer`: we have not fully audited the errors thrown by k8s,
        # so any more useful classification of this error would be difficult.
        raise Exception(write_task_response.error)


async def secret_delete(
    workflow: Workflow, user_id: UserId, secret_name: str
) -> None:
    secret = _secret(user_id, secret_name)
    delete_response = await secret.Delete(workflow)
    delete_task_response = await workflow.future_from_task_id(
        task_id=delete_response.task_id, response_type=DeleteTaskResponse
    )
    if delete_task_response.HasField('error'):
        # TODO: See `SecretServicer`: we have not fully audited the errors thrown by k8s,
        # so any more useful classification of this error would be difficult.
        raise Exception(delete_task_response.error)


async def user_id(workflow: Workflow, api_key: str) -> UserId:
    # TODO(rjh): have the parser validate that the given API key has the right shape.
    api_key_id, api_key_secret = api_key.split("-")
    authenticate_response = await APIKey(api_key_id).Authenticate(
        workflow, secret=api_key_secret
    )
    user_id = authenticate_response.user_id
    return user_id


def _secret(user_id: UserId, secret_name: str) -> Secret:
    # The server validates this ID.
    return Secret(
        SecretId.from_parts(
            user_id=user_id, space_name=user_id, secret_name=secret_name
        ).encode()
    )
