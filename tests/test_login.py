import pytest
from playwright.sync_api import Page, expect

from config.settings import PASSWORD, USERNAME
from pages.login_page import LoginPage


@pytest.mark.login  # Label this test so it can be selected with `pytest -m login`.
def test_login_with_valid_credentials(page: Page) -> None:
    """Log in with Sauce Demo's sample account and verify the inventory screen."""
    if not USERNAME or not PASSWORD:  # Do not try to submit an empty account.
        pytest.skip("Set TEST_USERNAME and TEST_PASSWORD before running this test")  # Report as skipped.

    login_page = LoginPage(page)  # Wrap the pytest-playwright browser tab in our page object.
    login_page.open()  # Open the configured Sauce Demo URL.
    login_page.login(USERNAME, PASSWORD)  # Fill the two fields and submit the login form.
    try:  # Wait for the page that should appear after a successful login.
        expect(login_page.products_heading).to_be_visible()  # Playwright retries until visible or timed out.
    except AssertionError as error:  # The expected page did not appear before the assertion timeout.
        if login_page.error_message.is_visible():  # Check whether Sauce Demo explains a rejected login.
            message = login_page.error_message.inner_text()  # Read the app's own error text.
            raise AssertionError(f"Login was rejected: {message}") from error  # Keep original timeout context.
        raise  # Re-raise unchanged when no login-specific message is present.
