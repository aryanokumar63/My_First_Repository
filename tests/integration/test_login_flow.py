"""Integration tests for complete login, inventory, and logout flows."""

import pytest
from playwright.sync_api import expect

from config.settings import BASE_URL, PASSWORD, USERNAME
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.mark.integration
@pytest.mark.login
def test_valid_login_opens_inventory(authenticated_inventory_page: InventoryPage) -> None:
    """A valid login should display inventory content at the inventory URL."""
    expect(authenticated_inventory_page.products_heading).to_be_visible()
    expect(authenticated_inventory_page.backpack_product).to_be_visible()
    expect(authenticated_inventory_page.page).to_have_url(
        f"{BASE_URL.rstrip('/')}/inventory.html"
    )


@pytest.mark.integration
@pytest.mark.login
def test_login_can_be_submitted_with_enter(login_page: LoginPage) -> None:
    """Pressing Enter in the password field should submit valid credentials."""
    if not USERNAME or not PASSWORD:
        pytest.skip("Set TEST_USERNAME and TEST_PASSWORD before running this test")

    login_page.login_with_enter(USERNAME, PASSWORD)
    inventory_page = InventoryPage(login_page.page)
    expect(inventory_page.products_heading).to_be_visible()
    expect(inventory_page.backpack_product).to_be_visible()


@pytest.mark.integration
@pytest.mark.login
def test_user_can_retry_after_invalid_login(login_page: LoginPage) -> None:
    """A rejected attempt should allow the user to correct credentials and proceed."""
    if not USERNAME or not PASSWORD:
        pytest.skip("Set TEST_USERNAME and TEST_PASSWORD before running this test")

    login_page.login("invalid_user", "invalid_password")
    assert login_page.get_error_message() == (
        "Epic sadface: Username and password do not match any user in this service"
    )
    login_page.login(USERNAME, PASSWORD)
    expect(InventoryPage(login_page.page).products_heading).to_be_visible()


@pytest.mark.integration
@pytest.mark.login
def test_user_can_logout(authenticated_inventory_page: InventoryPage) -> None:
    """Logging out from inventory should return to a clean login screen."""
    authenticated_inventory_page.logout()
    expect(authenticated_inventory_page.page).to_have_url(f"{BASE_URL.rstrip('/')}/")
    expect(authenticated_inventory_page.page.get_by_placeholder("Username")).to_be_visible()
    expect(authenticated_inventory_page.page.get_by_role("button", name="Login")).to_be_visible()
