from pydantic import BaseModel


class User(BaseModel):
    login: str
    password: str


class Bet(BaseModel):
    login: str
    matchID: str
    team_pos: int
    amount: int
