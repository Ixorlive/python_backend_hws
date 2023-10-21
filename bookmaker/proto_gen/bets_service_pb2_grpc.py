# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import proto_gen.bets_service_pb2 as bets__service__pb2


class BetsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PlaceBet = channel.unary_unary(
            "/bets.Bets/PlaceBet",
            request_serializer=bets__service__pb2.PlaceBetRequest.SerializeToString,
            response_deserializer=bets__service__pb2.Confirmation.FromString,
        )
        self.CalculateOdds = channel.unary_unary(
            "/bets.Bets/CalculateOdds",
            request_serializer=bets__service__pb2.CalculateOddsRequest.SerializeToString,
            response_deserializer=bets__service__pb2.CalculateOddsResponse.FromString,
        )


class BetsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def PlaceBet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CalculateOdds(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_BetsServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "PlaceBet": grpc.unary_unary_rpc_method_handler(
            servicer.PlaceBet,
            request_deserializer=bets__service__pb2.PlaceBetRequest.FromString,
            response_serializer=bets__service__pb2.Confirmation.SerializeToString,
        ),
        "CalculateOdds": grpc.unary_unary_rpc_method_handler(
            servicer.CalculateOdds,
            request_deserializer=bets__service__pb2.CalculateOddsRequest.FromString,
            response_serializer=bets__service__pb2.CalculateOddsResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "bets.Bets", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Bets(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def PlaceBet(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/bets.Bets/PlaceBet",
            bets__service__pb2.PlaceBetRequest.SerializeToString,
            bets__service__pb2.Confirmation.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def CalculateOdds(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/bets.Bets/CalculateOdds",
            bets__service__pb2.CalculateOddsRequest.SerializeToString,
            bets__service__pb2.CalculateOddsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
