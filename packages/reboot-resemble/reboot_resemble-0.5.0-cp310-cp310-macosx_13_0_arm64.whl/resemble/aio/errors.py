import grpc
import resemble.v1alpha1.errors_pb2 as errors_pb2
from google.protobuf import any_pb2, text_format
from google.protobuf.message import Message
from google.rpc import code_pb2, status_pb2
from resemble.aio.types import assert_type
from typing import Optional, TypeVar, Union


class Aborted(Exception):
    """Base class of all RPC specific code generated errors used for
    aborting an RPC.

    NOTE: Given the issues[1] with multiple inheritance from `abc.ABC` and `Exception`
    we do not inherit from `abc.ABC` but raise `NotImplementedError` for
    "abstract" methods.

    [1] https://bugs.python.org/issue12029
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        result = f"aborted with '{self.error.DESCRIPTOR.name}"

        # NOTE: we use `text_format` to ensure `as_one_line=True`.
        body = text_format.MessageToString(
            self.error,
            as_one_line=True,
        ).strip()

        if len(body) == 0:
            result += "'"
        else:
            result += f" {{ {body} }}'"

        if self.message is not None:
            result += f": {self.message}"

        return result

    @property
    def error(self) -> Message:
        raise NotImplementedError

    @property
    def code(self) -> grpc.StatusCode:
        raise NotImplementedError

    @property
    def message(self) -> Optional[str]:
        raise NotImplementedError

    def to_status(self) -> status_pb2.Status:
        detail = any_pb2.Any()
        detail.Pack(self.error)

        return status_pb2.Status(
            # A `grpc.StatusCode` is a `tuple[int, str]` where the
            # `int` is the actual code that we need to pass on.
            code=self.code.value[0],
            message=self.message or "",
            details=[detail],
        )


AbortedT = TypeVar('AbortedT', bound=Aborted)


# TODO(benh): move this to `Aborted`.
def _from_status(
    cls: type[AbortedT],
    status: status_pb2.Status,
) -> Optional[AbortedT]:
    # TODO(rjh, benh): think about how to handle cases where there are
    # multiple errors (since there are multiple details).
    assert issubclass(cls, Aborted)

    for detail in status.details:
        # TODO: https://github.com/reboot-dev/respect/issues/2418
        for error_type in cls.ERROR_TYPES:  # type: ignore[attr-defined]
            if detail.Is(error_type.DESCRIPTOR):
                error = error_type()
                detail.Unpack(error)

                message = status.message if len(status.message) > 0 else None

                # TODO(benh): figure out why we need to ignore this type.
                return cls(error, message=message)  # type: ignore[call-arg]

    return None


class SystemAborted(Aborted):
    """Encapsulates errors due to the system aborting."""

    # Type alias for the union of possible errors.
    Error = Union[
        # Resemble:
        errors_pb2.ActorAlreadyConstructed,
        errors_pb2.ActorNotConstructed,
        errors_pb2.TransactionParticipantFailedToPrepare,
        errors_pb2.TransactionParticipantFailedToCommit,
        errors_pb2.UnknownService,
        errors_pb2.UnknownTask,

        # gRPC:
        errors_pb2.Cancelled,
        errors_pb2.Unknown,
        errors_pb2.InvalidArgument,
        errors_pb2.DeadlineExceeded,
        errors_pb2.NotFound,
        errors_pb2.AlreadyExists,
        errors_pb2.PermissionDenied,
        errors_pb2.ResourceExhausted,
        errors_pb2.FailedPrecondition,
        errors_pb2.Aborted,
        errors_pb2.OutOfRange,
        errors_pb2.Unimplemented,
        errors_pb2.Internal,
        errors_pb2.Unavailable,
        errors_pb2.DataLoss,
        errors_pb2.Unauthenticated,
    ]

    ERROR_TYPES: list[type[Error]] = [
        # Resemble:
        errors_pb2.ActorAlreadyConstructed,
        errors_pb2.ActorNotConstructed,
        errors_pb2.TransactionParticipantFailedToPrepare,
        errors_pb2.TransactionParticipantFailedToCommit,
        errors_pb2.UnknownService,
        errors_pb2.UnknownTask,

        # gRPC:
        errors_pb2.Cancelled,
        errors_pb2.Unknown,
        errors_pb2.InvalidArgument,
        errors_pb2.DeadlineExceeded,
        errors_pb2.NotFound,
        errors_pb2.AlreadyExists,
        errors_pb2.PermissionDenied,
        errors_pb2.ResourceExhausted,
        errors_pb2.FailedPrecondition,
        errors_pb2.Aborted,
        errors_pb2.OutOfRange,
        errors_pb2.Unimplemented,
        errors_pb2.Internal,
        errors_pb2.Unavailable,
        errors_pb2.DataLoss,
        errors_pb2.Unauthenticated,
    ]

    _error: Error
    _code: grpc.StatusCode
    _message: Optional[str]

    def __init__(
        self,
        error: Error,
        *,
        code: Optional[grpc.StatusCode] = None,
        message: Optional[str] = None,
    ):
        super().__init__()

        assert_type(error, self.ERROR_TYPES)

        self._error = error

        if isinstance(error, errors_pb2.Cancelled):
            self._code = grpc.StatusCode.CANCELLED

        elif isinstance(error, errors_pb2.Unknown):
            self._code = grpc.StatusCode.UNKNOWN

        elif isinstance(error, errors_pb2.InvalidArgument):
            self._code = grpc.StatusCode.INVALID_ARGUMENT

        elif isinstance(error, errors_pb2.DeadlineExceeded):
            self._code = grpc.StatusCode.DEADLINE_EXCEEDE

        elif isinstance(error, errors_pb2.NotFound):
            self._code = grpc.StatusCode.NOT_FOUND

        elif isinstance(error, errors_pb2.AlreadyExists):
            self._code = grpc.StatusCode.ALREADY_EXISTS

        elif isinstance(error, errors_pb2.PermissionDenied):
            self._code = grpc.StatusCode.PERMISSION_DENIED

        elif isinstance(error, errors_pb2.ResourceExhausted):
            self._code = grpc.StatusCode.RESOURCE_EXHAUSTED

        elif isinstance(error, errors_pb2.FailedPrecondition):
            self._code = grpc.StatusCode.FAILED_PRECONDITION

        elif isinstance(error, errors_pb2.Aborted):
            self._code = grpc.StatusCode.ABORTED

        elif isinstance(error, errors_pb2.OutOfRange):
            self._code = grpc.StatusCode.OUT_OF_RANGE

        elif isinstance(error, errors_pb2.Unimplemented):
            self._code = grpc.StatusCode.UNIMPLEMENTED

        elif isinstance(error, errors_pb2.Internal):
            self._code = grpc.StatusCode.INTERNAL

        elif isinstance(error, errors_pb2.Unavailable):
            self._code = grpc.StatusCode.UNAVAILABLE

        elif isinstance(error, errors_pb2.DataLoss):
            self._code = grpc.StatusCode.DATA_LOSS

        elif isinstance(error, errors_pb2.Unauthenticated):
            self._code = grpc.StatusCode.UNAUTHENTICATED

        else:
            self._code = grpc.StatusCode.ABORTED

        self._message = message

    @property
    def error(self) -> Error:
        return self._error

    @property
    def code(self) -> grpc.StatusCode:
        return self._code

    @property
    def message(self) -> Optional[str]:
        return self._message

    @classmethod
    def from_status(
        cls,
        status: status_pb2.Status,
    ) -> Optional['SystemAborted']:
        if len(status.details) != 0:
            return _from_status(cls, status)

        if status.code == code_pb2.Code.CANCELLED:
            return SystemAborted(
                errors_pb2.Cancelled(),
                message=status.message,
            )

        if status.code == code_pb2.Code.UNKNOWN:
            return SystemAborted(
                errors_pb2.Unknown(),
                message=status.message,
            )

        if status.code == code_pb2.Code.INVALID_ARGUMENT:
            return SystemAborted(
                errors_pb2.InvalidArgument(),
                message=status.message,
            )

        if status.code == code_pb2.Code.DEADLINE_EXCEEDED:
            return SystemAborted(
                errors_pb2.DeadlineExceeded(),
                message=status.message,
            )

        if status.code == code_pb2.Code.NOT_FOUND:
            return SystemAborted(
                errors_pb2.NotFound(),
                message=status.message,
            )

        if status.code == code_pb2.Code.ALREADY_EXISTS:
            return SystemAborted(
                errors_pb2.AlreadyExists(),
                message=status.message,
            )

        if status.code == code_pb2.Code.PERMISSION_DENIED:
            return SystemAborted(
                errors_pb2.PermissionDenied(),
                message=status.message,
            )

        if status.code == code_pb2.Code.RESOURCE_EXHAUSTED:
            return SystemAborted(
                errors_pb2.ResourceExhausted(),
                message=status.message,
            )

        if status.code == code_pb2.Code.FAILED_PRECONDITION:
            return SystemAborted(
                errors_pb2.FailedPrecondition(),
                message=status.message,
            )

        if status.code == code_pb2.Code.ABORTED:
            return SystemAborted(
                errors_pb2.Aborted(),
                message=status.message,
            )

        if status.code == code_pb2.Code.OUT_OF_RANGE:
            return SystemAborted(
                errors_pb2.OutOfRange(),
                message=status.message,
            )

        if status.code == code_pb2.Code.UNIMPLEMENTED:
            return SystemAborted(
                errors_pb2.Unimplemented(),
                message=status.message,
            )

        if status.code == code_pb2.Code.INTERNAL:
            return SystemAborted(
                errors_pb2.Internal(),
                message=status.message,
            )

        if status.code == code_pb2.Code.UNAVAILABLE:
            return SystemAborted(
                errors_pb2.Unavailable(),
                message=status.message,
            )

        if status.code == code_pb2.Code.DATA_LOSS:
            return SystemAborted(
                errors_pb2.DataLoss(),
                message=status.message,
            )

        if status.code == code_pb2.Code.UNAUTHENTICATED:
            return SystemAborted(
                errors_pb2.Unauthenticated(),
                message=status.message,
            )

        return SystemAborted(
            errors_pb2.Unknown(),
            message=status.message,
        )

    @classmethod
    def from_grpc_aio_rpc_error(
        cls,
        aio_rpc_error: grpc.aio.AioRpcError,
    ) -> 'SystemAborted':
        if aio_rpc_error.code() == grpc.StatusCode.CANCELLED:
            return SystemAborted(
                errors_pb2.Cancelled(),
                message=aio_rpc_error.details(),
            )

        if aio_rpc_error.code() == grpc.StatusCode.UNKNOWN:
            return SystemAborted(
                errors_pb2.Unknown(),
                message=aio_rpc_error.details(),
            )

        if aio_rpc_error.code() == grpc.StatusCode.INVALID_ARGUMENT:
            return SystemAborted(
                errors_pb2.InvalidArgument(),
                message=aio_rpc_error.details(),
            )

        if aio_rpc_error.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
            return SystemAborted(
                errors_pb2.DeadlineExceeded(),
                message=aio_rpc_error.details(),
            )

        if aio_rpc_error.code() == grpc.StatusCode.NOT_FOUND:
            return SystemAborted(
                errors_pb2.NotFound(),
                message=aio_rpc_error.details(),
            )

        if aio_rpc_error.code() == grpc.StatusCode.ALREADY_EXISTS:
            return SystemAborted(
                errors_pb2.AlreadyExists(),
                message=aio_rpc_error.details(),
            )

        if aio_rpc_error.code() == grpc.StatusCode.PERMISSION_DENIED:
            return SystemAborted(
                errors_pb2.PermissionDenied(),
                message=aio_rpc_error.details(),
            )

        if aio_rpc_error.code() == grpc.StatusCode.RESOURCE_EXHAUSTED:
            return SystemAborted(
                errors_pb2.ResourceExhausted(),
                message=aio_rpc_error.details(),
            )

        if aio_rpc_error.code() == grpc.StatusCode.FAILED_PRECONDITION:
            return SystemAborted(
                errors_pb2.FailedPrecondition(),
                message=aio_rpc_error.details(),
            )

        if aio_rpc_error.code() == grpc.StatusCode.ABORTED:
            return SystemAborted(
                errors_pb2.Aborted(),
                message=aio_rpc_error.details(),
            )

        if aio_rpc_error.code() == grpc.StatusCode.OUT_OF_RANGE:
            return SystemAborted(
                errors_pb2.OutOfRange(),
                message=aio_rpc_error.details(),
            )

        if aio_rpc_error.code() == grpc.StatusCode.UNIMPLEMENTED:
            return SystemAborted(
                errors_pb2.Unimplemented(),
                message=aio_rpc_error.details(),
            )

        if aio_rpc_error.code() == grpc.StatusCode.INTERNAL:
            return SystemAborted(
                errors_pb2.Internal(),
                message=aio_rpc_error.details(),
            )

        if aio_rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
            return SystemAborted(
                errors_pb2.Unavailable(),
                message=aio_rpc_error.details(),
            )

        if aio_rpc_error.code() == grpc.StatusCode.DATA_LOSS:
            return SystemAborted(
                errors_pb2.DataLoss(),
                message=aio_rpc_error.details(),
            )

        if aio_rpc_error.code() == grpc.StatusCode.UNAUTHENTICATED:
            return SystemAborted(
                errors_pb2.Unauthenticated(),
                message=aio_rpc_error.details(),
            )

        return SystemAborted(
            errors_pb2.Unknown(),
            message=aio_rpc_error.details(),
        )
