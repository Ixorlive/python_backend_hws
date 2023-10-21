from dataclasses import dataclass


@dataclass
class Confirmation:
    success: bool
    message: str
