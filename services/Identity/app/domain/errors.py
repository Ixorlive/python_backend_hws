class LoginNotFoundException(Exception):
    """Raised when the login is not found"""

    pass


class IncorrectPasswordException(Exception):
    """Raised when the password is incorrect"""

    pass


class InsufficientFundsException(Exception):
    """When the user does not have enough balance to withdraw money"""

    pass


class AccountAlreadyExistsException(Exception):
    pass
