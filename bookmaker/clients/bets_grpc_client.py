import grpc
from domain.common import Confirmation
from proto_gen import bets_service_pb2, bets_service_pb2_grpc


class BetsGRPCClient:
    def __init__(self, channel_str: str):
        channel = grpc.insecure_channel(channel_str)
        self.stub = bets_service_pb2_grpc.BetsStub(channel)

    def place_bet(
        self, login: str, matchID: str, team_pos: int, amount: int
    ) -> Confirmation:
        res = self.stub.PlaceBet(
            bets_service_pb2.PlaceBetRequest(
                login=login, matchID=matchID, team_pos=team_pos, amount=amount
            )
        )
        return Confirmation(res.success, res.message)

    def calculate_odds(self, matchID: str):
        res = self.stub.CalculateOdds(
            bets_service_pb2.CalculateOddsRequest(matchID=matchID)
        )
        return res.oddsTeam1, res.oddsTeam2
