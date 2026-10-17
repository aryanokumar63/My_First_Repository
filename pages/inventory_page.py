"""Page object for the inventory screen and its logout flow."""

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Locators and actions available after a successful login."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.products_heading: Locator = page.get_by_text("Products", exact=True)
        self.backpack_product: Locator = page.get_by_text("Sauce Labs Backpack", exact=True)
        self.menu_button: Locator = page.get_by_role("button", name="Open Menu")
        self.logout_link: Locator = page.locator('[data-test="logout-sidebar-link"]')

    def logout(self) -> None:
        """Open the navigation menu and return to the login page."""
        self.click(self.menu_button)
        self.click(self.logout_link)
