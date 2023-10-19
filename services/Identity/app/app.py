from concurrent import futures

import grpc
from pymongo import MongoClient

import proto_gen.user_auth_pb2_grpc as user_auth_pb2_grpc
from infras.mongodb.account_repo import AccountRepo
from router.auth_grpc_server import UserAuthServicer
from user_manager import UserManager

# todo: create config
CONNECTION_STRING = "mongodb://ixor:ixor@localhost:27017/"
DATABASE_NAME = "bookmaker_db"
COLLECTION_NAME = "user_accounts"


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    # todo: exceptions
    client = MongoClient(CONNECTION_STRING)
    account_repo = AccountRepo(client[DATABASE_NAME][COLLECTION_NAME])

    user_mgr = UserManager(account_repo)
    user_auth_service = UserAuthServicer(user_mgr)

    user_auth_pb2_grpc.add_UserAuthServicer_to_server(user_auth_service, server)

    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
