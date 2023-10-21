import grpc
from domain.match import Match, MatchStatus
from proto_gen import match_service_pb2, match_service_pb2_grpc

STATUS_MAPPING = {
    MatchStatus.UPCOMING: match_service_pb2.MatchStatus.UPCOMING,
    MatchStatus.ONGOING: match_service_pb2.MatchStatus.ONGOING,
    MatchStatus.COMPLETED: match_service_pb2.MatchStatus.COMPLETED,
}


class MatchServiceGRPCClient:
    def __init__(self, channel_str: str):
        channel = grpc.insecure_channel(channel_str)
        self.stub = match_service_pb2_grpc.MatchServiceStub(channel)

    def add_match(self, team1: str, team2: str, match_time: str) -> Match:
        res = self.stub.AddMatch(
            match_service_pb2.AddMatchRequest(
                team1=team1, team2=team2, match_time=match_time
            )
        )
        return Match(
            id=res.match.id,
            team1=res.match.team1,
            team2=res.match.team2,
            match_time=res.match.match_time,
        )

    def update_match_time(self, match_id: str, new_time: str) -> Match:
        res = self.stub.UpdateMatchTime(
            match_service_pb2.UpdateMatchTimeRequest(id=match_id, new_time=new_time)
        )
        return Match(
            id=res.match.id,
            team1=res.match.team1,
            team2=res.match.team2,
            match_time=res.match.match_time,
        )

    def mark_match_as_completed(self, match_id: str) -> Match:
        res = self.stub.MarkMatchAsCompleted(
            match_service_pb2.MarkMatchRequest(id=match_id)
        )
        return Match(
            id=res.match.id,
            team1=res.match.team1,
            team2=res.match.team2,
            match_time=res.match.match_time,
        )

    def list_matches(self, status_filter: MatchStatus) -> list[Match]:
        res = self.stub.ListMatches(
            match_service_pb2.ListMatchesRequest(status_filter=status_filter)
        )
        return [
            Match(
                id=match.id,
                team1=match.team1,
                team2=match.team2,
                match_time=match.match_time,
            )
            for match in res.matches
        ]
