from dataclasses import dataclass


@dataclass
class LoginDetails:
    login: str
    password: str
