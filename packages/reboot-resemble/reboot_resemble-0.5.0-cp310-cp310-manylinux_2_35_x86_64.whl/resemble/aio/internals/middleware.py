import grpc
import uuid
from abc import ABC, abstractmethod
from google.protobuf.message import Message
from resemble.aio.auth.authorizers import Authorizer
from resemble.aio.auth.token_verifiers import TokenVerifier
from resemble.aio.contexts import ContextT
from resemble.aio.headers import Headers
from resemble.aio.internals.channel_manager import _ChannelManager
from resemble.aio.internals.contextvars import Servicing, _servicing
from resemble.aio.internals.tasks_dispatcher import TasksDispatcher
from resemble.aio.tasks import TaskEffect
from resemble.aio.types import ActorId, ApplicationId, ServiceName
from typing import AsyncIterator, Optional


class Middleware(ABC):
    """Base class for generated middleware.
    """
    # We expect these values to be set by generated subclass constructors.
    tasks_dispatcher: TasksDispatcher
    request_type_by_method_name: dict[str, type[Message]]

    _token_verifier: Optional[TokenVerifier]
    _authorizer: Optional[Authorizer]

    def __init__(
        self,
        *,
        application_id: ApplicationId,
        service_name: ServiceName,
        channel_manager: _ChannelManager,
    ):
        self._application_id = application_id
        self._service_name = service_name
        self._channel_manager = channel_manager

    @property
    def application_id(self) -> ApplicationId:
        return self._application_id

    @property
    def service_name(self) -> ServiceName:
        return self._service_name

    def create_context(
        self,
        *,
        headers: Headers,
        context_type: type[ContextT],
    ) -> ContextT:
        """Create a Context object given the parameters."""
        # Toggle 'servicing' to indicate we are initializing the
        # servicing of an RPC which will, for example, permit the
        # construction of a context without raising an error.
        _servicing.set(Servicing.INITIALIZING)

        # Sanity check: we're handling the right type, right?
        if headers.service_name != self._service_name:
            raise ValueError(
                f'Requested unexpected service name {headers.service_name}; '
                f'this servicer is of type {self._service_name}'
            )

        context = context_type(
            channel_manager=self._channel_manager,
            headers=headers,
        )

        # Now toggle 'servicing' to indicate that we are servicing the
        # RPC which will, for example, forbid the construction of a
        # context by raising an error.
        _servicing.set(Servicing.YES)

        return context

    def create_context_from_grpc(
        self,
        *,
        grpc_context: grpc.aio.ServicerContext,
        context_type: type[ContextT],
    ) -> ContextT:
        """Create a Context object based on the gRPC metadata."""
        return self.create_context(
            headers=Headers.from_grpc_context(grpc_context),
            context_type=context_type,
        )

    async def stop(self):
        """Stop the middleware background tasks.
        """
        await self.tasks_dispatcher.stop()

    @abstractmethod
    async def dispatch(
        self, task: TaskEffect, *, only_validate: bool = False
    ) -> Message:
        """Abstract dispatch method; implemented by code generation for each
        of the service's task methods."""
        raise NotImplementedError

    @abstractmethod
    async def inspect(self, actor_id: ActorId) -> AsyncIterator[Message]:
        """Abstract method for handling an Inspect request; implemented by code
        generation for each of the service's."""
        raise NotImplementedError
        yield  # Necessary for type checking.

    @abstractmethod
    async def react_query(
        self,
        grpc_context: grpc.aio.ServicerContext,
        headers: Headers,
        method: str,
        request_bytes: bytes,
    ) -> AsyncIterator[tuple[Optional[Message], list[uuid.UUID]]]:
        """Abstract method for handling a React request; implemented by code
        generation for each of the service's React compatible reader methods."""
        raise NotImplementedError
        yield  # Necessary for type checking.

    @abstractmethod
    async def react_mutate(
        self,
        headers: Headers,
        method: str,
        request_bytes: bytes,
    ) -> Message:
        """Abstract method for handling a React mutation; implemented by code
        generation for each of the service's React compatible mutator methods."""
        raise NotImplementedError

    @abstractmethod
    def add_to_server(self, server: grpc.aio.Server) -> None:
        raise NotImplementedError
