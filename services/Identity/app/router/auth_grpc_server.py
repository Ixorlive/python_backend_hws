from concurrent import futures

import domain.errors as errors
import proto_gen.user_auth_pb2 as user_auth_pb2
import proto_gen.user_auth_pb2_grpc as user_auth_pb2_grpc
from user_manager import UserManager


class UserAuthServicer(user_auth_pb2_grpc.UserAuthServicer):
    def __init__(self, user_mgr: UserManager):
        self.user_mgr = user_mgr

    def Register(self, request, context):
        acc = self.user_mgr.register(request.username, request.password)
        if acc:
            return user_auth_pb2.Confirmation(success=True, message="User registered!")
        return user_auth_pb2.Confirmation(success=False, message="User exists?")

    def Login(self, request, context):
        message = "Registration successful"
        success = False
        token = "-1"
        try:
            self.user_mgr.login(request.username, request.password)
            success = True
            token = "hz"
        except errors.LoginNotFoundException:
            message = "Login not found"
        except errors.IncorrectPasswordException:
            message = "Password is incorrect"
        except Exception as e:
            message = str(e)
        return user_auth_pb2.LoginConfirmation(
            success=success, message=message, token=token
        )

    def Balance(self, request, context):
        balance = self.user_mgr.balance(request.login)
        return user_auth_pb2.Amount(value=balance)

    def Deposit(self, request, context):
        success = False
        message = "Deposited successfully!"
        try:
            self.user_mgr.deposit(request.login, request.amount)
            success = True
        except errors.LoginNotFoundException:
            message = "Login not found"
        except Exception as e:
            message = str(e)
        return user_auth_pb2.Confirmation(success=success, message=message)

    def Withdraw(self, request, context):
        success = False
        message = "Withdraw successfully!"
        try:
            self.user_mgr.withdraw(request.login, request.amount)
            success = True
        except errors.LoginNotFoundException:
            message = "Login not found"
        except errors.InsufficientFundsException:
            message = "Unsufficient funds"
        except Exception as e:
            message = str(e)
        return user_auth_pb2.Confirmation(success=success, message=message)
