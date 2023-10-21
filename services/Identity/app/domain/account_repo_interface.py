from abc import ABC, abstractmethod
from typing import Optional

from domain.account import Account


class IAccountRepo(ABC):
    @abstractmethod
    def add_account(self, account: Account) -> str:
        """
        Persist a user in the repository. If a user with the given ID already exists,
        it should update the existing user.
        """
        pass

    @abstractmethod
    def find_by_login(self, login: str) -> Optional[Account]:
        """
        Retrieve a user by their login. If no user is found, return None.
        """
        pass

    @abstractmethod
    def update_balance(self, login: str, amount: int) -> bool:
        """
        Update the balance of a user by a certain amount. This can be positive (for deposits)
        or negative (for withdrawals).
        """
        pass
