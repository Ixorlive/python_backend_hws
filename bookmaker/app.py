from typing import Optional

from clients.bets_grpc_client import BetsGRPCClient
from clients.identity_grpc_client import IdentityGRPCClient
from clients.match_grpc_client import MatchServiceGRPCClient
from domain.match import MatchStatus
from fastapi import FastAPI, HTTPException
from models.models import Bet, User

app = FastAPI()

# Mock in-memory database for user sessions
registered_users = set()


identity_client = IdentityGRPCClient("localhost:50051")
match_client = MatchServiceGRPCClient("localhost:50052")
bet_client = BetsGRPCClient("localhost:50053")


@app.post("/register/")
async def register(user: User):
    confirmation = identity_client.register(user.login, user.password)
    if confirmation.success:
        registered_users.add(user.login)
        return {"success": True, "message": confirmation.message}
    raise HTTPException(status_code=400, detail=confirmation.message)


@app.post("/login/")
async def login(user: User):
    confirmation = identity_client.login(user.login, user.password)
    if confirmation.success:
        return {"success": True, "message": confirmation.message}
    raise HTTPException(status_code=401, detail=confirmation.message)


@app.get("/matches/")
async def list_matches(status: Optional[str]):
    status_filter = MatchStatus.UPCOMING  # default value
    if status:
        try:
            status_filter = MatchStatus[status.upper()]
        except KeyError:
            raise HTTPException(
                status_code=400, detail=f"Invalid match status: {status}"
            )

    return match_client.list_matches(status_filter)


@app.post("/bet/")
async def place_bet(bet: Bet):
    # if bet.login not in registered_users:
    #     raise HTTPException(status_code=400, detail="Unregistered user")
    confirmation = bet_client.place_bet(
        bet.login, bet.matchID, bet.team_pos, bet.amount
    )
    if confirmation.success:
        return {"message": confirmation.message}
    raise HTTPException(status_code=400, detail=confirmation.message)


@app.get("/balance/")
async def get_balance(login: str):
    # if login not in registered_users:
    #     raise HTTPException(status_code=400, detail="Unregistered user")
    balance = identity_client.get_balance(login)
    return {"balance": balance}
