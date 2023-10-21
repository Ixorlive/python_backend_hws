import grpc
from domain.common import Confirmation
from proto_gen import user_auth_pb2, user_auth_pb2_grpc


class IdentityGRPCClient:
    def __init__(self, channel_str: str):
        channel = grpc.insecure_channel(channel_str)
        self.stub = user_auth_pb2_grpc.UserAuthStub(channel)

    def register(self, login: str, password: str) -> Confirmation:
        res = self.stub.Register(
            user_auth_pb2.UserInfo(username=login, password=password)
        )
        return Confirmation(res.success, res.message)

    def login(self, login: str, password: str) -> Confirmation:
        res = self.stub.Login(
            user_auth_pb2.UserCredentials(username=login, password=password)
        )
        return Confirmation(res.success, res.message)

    def get_balance(self, login: str) -> int:
        res = self.stub.Balance(user_auth_pb2.UserLogin(login=login))
        return res.value

    def deposit(self, login: str, amount: int) -> Confirmation:
        res = self.stub.Deposit(user_auth_pb2.Transaction(login=login, amount=amount))
        return Confirmation(res.success, res.message)
