from typing import Optional

from pymongo.database import Database

from domain.account import Account
from domain.account_repo_interface import IAccountRepo
from pymongo import MongoClient


def get_database(db_name: str):
    CONNECTION_STRING = "mongodb://ixor:ixor@localhost:27017/"
    client = MongoClient(CONNECTION_STRING)
    return client[db_name]


class AccountRepo(IAccountRepo):
    def __init__(self, collection) -> None:
        self.user_accounts = collection

    def add_account(self, account: Account) -> str:
        doc = {
            "login": account.login,
            "password": account.password,
            "balance": account.balance,
        }
        res = self.user_accounts.insert_one(doc)
        return str(res.inserted_id)

    def find_by_login(self, login: str) -> Optional[Account]:
        doc = self.user_accounts.find_one({"login": login})
        return self._get_account_from_doc(doc)

    def update_balance(self, login: str, amount: float) -> bool:
        filter_criteria = {"login": login}
        update_data = {"$inc": {"balance": amount}}

        result = self.user_accounts.update_one(filter_criteria, update_data)
        return result is not None

    def _get_account_from_doc(self, doc) -> Optional[Account]:
        if doc is None:
            return None
        return Account(doc["login"], doc["password"], doc["balance"])
