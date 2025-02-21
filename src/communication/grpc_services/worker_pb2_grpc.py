# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import src.communication.grpc_services.worker_pb2 as worker__pb2

GRPC_GENERATED_VERSION = '1.69.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in worker_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class WorkerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ManageWorker = channel.stream_stream(
                '/worker.WorkerService/ManageWorker',
                request_serializer=worker__pb2.WorkerCommand.SerializeToString,
                response_deserializer=worker__pb2.WorkerStatus.FromString,
                _registered_method=True)


class WorkerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ManageWorker(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WorkerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ManageWorker': grpc.stream_stream_rpc_method_handler(
                    servicer.ManageWorker,
                    request_deserializer=worker__pb2.WorkerCommand.FromString,
                    response_serializer=worker__pb2.WorkerStatus.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'worker.WorkerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('worker.WorkerService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class WorkerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ManageWorker(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            '/worker.WorkerService/ManageWorker',
            worker__pb2.WorkerCommand.SerializeToString,
            worker__pb2.WorkerStatus.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
