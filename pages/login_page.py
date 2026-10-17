"""Page object for the Sauce Demo login screen."""

from playwright.sync_api import Error as PlaywrightError, Locator, Page, expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Locators and actions for the login screen."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input: Locator = page.get_by_placeholder("Username")
        self.password_input: Locator = page.get_by_placeholder("Password")
        self.login_button: Locator = page.get_by_role("button", name="Login")
        self.error_message: Locator = page.locator('[data-test="error"]')
        self.products_heading: Locator = page.get_by_text("Products", exact=True)

    def login(self, username: str, password: str) -> None:
        """Fill both credentials and submit the login form."""
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)

    def login_with_enter(self, username: str, password: str) -> None:
        """Submit the form with Enter, as a keyboard user would."""
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        try:
            self.password_input.press("Enter")
        except PlaywrightError as error:
            raise RuntimeError("Could not submit the login form with Enter") from error

    def get_error_message(self) -> str:
        """Wait for a login error and return its text."""
        try:
            expect(self.error_message).to_be_visible()
            return self.read_text(self.error_message)
        except AssertionError as error:
            raise AssertionError("The login error message did not appear") from error
        except (PlaywrightError, RuntimeError) as error:
            raise RuntimeError("Could not capture the login error message") from error
