from dataclasses import dataclass


@dataclass
class Account:
    login: str
    password: str
    balance: int
