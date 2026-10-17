"""Page object for the Sauce Demo login screen."""

from playwright.sync_api import Error as PlaywrightError  # Playwright's common error type.
from playwright.sync_api import Locator, Page  # Types for the tab and its element locators.

from pages.base_page import BasePage  # Reuse navigation and shared timeout handling.


class LoginPage(BasePage):  # Group login-screen locators and actions in one page object.
    def __init__(self, page: Page) -> None:  # Create the page object for pytest's browser tab.
        super().__init__(page)  # Set up the shared browser behavior first.
        self.username_input: Locator = page.get_by_placeholder("Username")  # Find user field by its placeholder.
        self.password_input: Locator = page.get_by_placeholder("Password")  # Find password field by its placeholder.
        self.login_button: Locator = page.get_by_role("button", name="Login")  # Find the accessible Login button.
        self.error_message: Locator = page.locator('[data-test="error"]')  # Sauce Demo marks errors with data-test.
        self.products_heading: Locator = page.get_by_text("Products", exact=True)  # Text shown after successful login.

    def login(self, username: str, password: str) -> None:  # Enter credentials and submit the form.
        try:  # A missing or unresponsive form element can time out during an action.
            self.username_input.fill(username)  # Replace the username field's current value.
            self.password_input.fill(password)  # Replace the password field's current value.
            self.login_button.click()  # Submit the form after both fields are filled.
        except PlaywrightError as error:  # Preserve the original Playwright failure for debugging.
            raise RuntimeError("Could not complete the login form") from error  # Explain which workflow failed.
