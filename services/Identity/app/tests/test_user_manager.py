from unittest.mock import Mock

import bcrypt
import domain.errors as errors
import pytest
from domain.account import Account
from domain.account_repo_interface import IAccountRepo
from user_manager import UserManager


# Setup for the tests
@pytest.fixture
def user_manager():
    repo_mock = Mock(spec=IAccountRepo)
    return UserManager(repo_mock)


@pytest.fixture
def sample_account():
    sample_login = "testuser"
    sample_password = "testpass"
    sample_hashed_password = bcrypt.hashpw(
        sample_password.encode("utf-8"), bcrypt.gensalt()
    )
    return Account(
        sample_login, sample_hashed_password.decode("utf-8"), UserManager.first_deposit
    )


# Tests
def test_register(user_manager, sample_account):
    user_manager.repo.add_account.return_value = sample_account
    account = user_manager.register(sample_account.login, "testpass")

    assert account.login == sample_account.login
    assert account.balance == UserManager.first_deposit
    assert bcrypt.checkpw("testpass".encode("utf-8"), account.password.encode("utf-8"))


def test_login_success(user_manager, sample_account):
    user_manager.repo.find_by_login.return_value = sample_account
    account = user_manager.login(sample_account.login, "testpass")

    assert account.login == sample_account.login
    assert account.balance == UserManager.first_deposit


def test_login_failure_incorrect_password(user_manager, sample_account):
    user_manager.repo.find_by_login.return_value = sample_account

    with pytest.raises(errors.IncorrectPasswordException):
        user_manager.login(sample_account.login, "wrongpass")


def test_login_failure_login_not_found(user_manager):
    user_manager.repo.find_by_login.return_value = None

    with pytest.raises(errors.LoginNotFoundException):
        user_manager.login("unknownuser", "testpass")
