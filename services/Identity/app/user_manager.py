import bcrypt
import domain.errors as errors
from domain.account import Account
from domain.account_repo_interface import IAccountRepo


# todo: create interface?
class UserManager:
    first_deposit = 1000  # how to use default value in mongodb...

    def __init__(self, repo: IAccountRepo):
        self.repo = repo

    def register(self, login: str, pwd: str):
        try:
            self._get_account_or_raise_exception(login)
            raise errors.AccountAlreadyExistsException
        except Exception:
            pass
        hashed = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())
        account = self.repo.add_account(
            Account(login, hashed.decode("utf-8"), self.first_deposit)
        )
        return account

    def login(self, login: str, pwd: str):
        acc = self._get_account_or_raise_exception(login)
        if bcrypt.checkpw(pwd.encode("utf-8"), acc.password.encode("utf-8")):
            return acc
        else:
            raise errors.IncorrectPasswordException

    def balance(self, login: str):
        acc = self._get_account_or_raise_exception(login)
        return acc.balance

    def deposit(self, login: str, amount: int):
        self._get_account_or_raise_exception(login)
        return self.repo.update_balance(login, amount)

    def withdraw(self, login: str, amount: int):
        acc = self._get_account_or_raise_exception(login)
        if acc.balance < amount:
            raise errors.InsufficientFundsException
        return self.repo.update_balance(login, -amount)

    def _get_account_or_raise_exception(self, login: str):
        acc = self.repo.find_by_login(login)
        if acc is None:
            raise errors.LoginNotFoundException
        return acc
