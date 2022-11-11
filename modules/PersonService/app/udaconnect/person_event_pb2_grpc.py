# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from app.udaconnect import person_event_pb2 as person__event__pb2


class PersonServiceGrpcStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.retrieve = channel.unary_unary(
                '/PersonServiceGrpc/retrieve',
                request_serializer=person__event__pb2.PersonID.SerializeToString,
                response_deserializer=person__event__pb2.PersonMessage.FromString,
                )
        self.retrieve_all = channel.unary_unary(
                '/PersonServiceGrpc/retrieve_all',
                request_serializer=person__event__pb2.Empty.SerializeToString,
                response_deserializer=person__event__pb2.PersonMessageList.FromString,
                )


class PersonServiceGrpcServicer(object):
    """Missing associated documentation comment in .proto file."""

    def retrieve(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def retrieve_all(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PersonServiceGrpcServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'retrieve': grpc.unary_unary_rpc_method_handler(
                    servicer.retrieve,
                    request_deserializer=person__event__pb2.PersonID.FromString,
                    response_serializer=person__event__pb2.PersonMessage.SerializeToString,
            ),
            'retrieve_all': grpc.unary_unary_rpc_method_handler(
                    servicer.retrieve_all,
                    request_deserializer=person__event__pb2.Empty.FromString,
                    response_serializer=person__event__pb2.PersonMessageList.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'PersonServiceGrpc', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PersonServiceGrpc(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def retrieve(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PersonServiceGrpc/retrieve',
            person__event__pb2.PersonID.SerializeToString,
            person__event__pb2.PersonMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def retrieve_all(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PersonServiceGrpc/retrieve_all',
            person__event__pb2.Empty.SerializeToString,
            person__event__pb2.PersonMessageList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
