from dataclasses import dataclass
from enum import IntEnum


class MatchStatus(IntEnum):
    UPCOMING = 0
    ONGOING = 1
    COMPLETED = 2


@dataclass
class Match:
    id: str
    team1: str
    team2: str
    match_time: str
