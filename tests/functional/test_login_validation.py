"""Functional tests for login input validation and negative cases."""

import pytest
from playwright.sync_api import expect

from config.settings import PASSWORD, USERNAME
from pages.login_page import LoginPage

INVALID_CREDENTIALS = (
    "Epic sadface: Username and password do not match any user in this service"
)
USERNAME_REQUIRED = "Epic sadface: Username is required"
PASSWORD_REQUIRED = "Epic sadface: Password is required"
LOCKED_OUT = "Epic sadface: Sorry, this user has been locked out."


@pytest.mark.functional
@pytest.mark.login
@pytest.mark.parametrize(
    ("username", "password", "expected_message"),
    [
        pytest.param("", "", USERNAME_REQUIRED, id="both-fields-empty"),
        pytest.param("", PASSWORD, USERNAME_REQUIRED, id="username-empty"),
        pytest.param(USERNAME, "", PASSWORD_REQUIRED, id="password-empty"),
        pytest.param("invalid_user", "invalid_password", INVALID_CREDENTIALS, id="both-invalid"),
        pytest.param(USERNAME, "invalid_password", INVALID_CREDENTIALS, id="wrong-password"),
        pytest.param("invalid_user", PASSWORD, INVALID_CREDENTIALS, id="wrong-username"),
        pytest.param("STANDARD_USER", PASSWORD, INVALID_CREDENTIALS, id="username-case-sensitive"),
        pytest.param(USERNAME, "SECRET_SAUCE", INVALID_CREDENTIALS, id="password-case-sensitive"),
        pytest.param(f" {USERNAME} ", PASSWORD, INVALID_CREDENTIALS, id="username-whitespace"),
        pytest.param(USERNAME, f" {PASSWORD} ", INVALID_CREDENTIALS, id="password-whitespace"),
        pytest.param("locked_out_user", PASSWORD, LOCKED_OUT, id="locked-account"),
    ],
)
def test_login_validation_messages(
    login_page: LoginPage,
    username: str,
    password: str,
    expected_message: str,
) -> None:
    """Each invalid or boundary input should produce the expected message."""
    login_page.login(username, password)
    try:
        actual_message = login_page.get_error_message()
    except (AssertionError, RuntimeError) as error:
        raise AssertionError(
            f"Login error was not captured for case {username=!r}, {password=!r}"
        ) from error

    assert actual_message == expected_message
    expect(login_page.products_heading).not_to_be_visible()
