"""Fixtures shared by the login tests."""

import pytest
from playwright.sync_api import Page, expect

from config.settings import PASSWORD, USERNAME
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Open a fresh login page for each test that requests this fixture."""
    page_object = LoginPage(page)
    page_object.open()
    return page_object


@pytest.fixture
def authenticated_inventory_page(login_page: LoginPage) -> InventoryPage:
    """Log in with the configured account and return the inventory page object."""
    if not USERNAME or not PASSWORD:
        pytest.skip("Set TEST_USERNAME and TEST_PASSWORD before running this test")

    login_page.login(USERNAME, PASSWORD)
    inventory_page = InventoryPage(login_page.page)
    expect(inventory_page.products_heading).to_be_visible()
    return inventory_page
