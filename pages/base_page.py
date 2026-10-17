"""Reusable browser actions shared by page objects."""

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Locator, Page

from config.settings import BASE_URL, DEFAULT_TIMEOUT


class BasePage:
    """Base class for page objects that share navigation and element actions."""

    def __init__(self, page: Page) -> None:
        self.page = page
        timeout_ms = DEFAULT_TIMEOUT * 1000
        self.page.set_default_timeout(timeout_ms)
        self.page.set_default_navigation_timeout(timeout_ms)

    def open(self, path: str = "") -> None:
        url = f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"
        try:
            self.page.goto(url, wait_until="domcontentloaded")
        except PlaywrightError as error:
            raise RuntimeError(f"Could not open {url}") from error

    def click(self, locator: Locator) -> None:
        """Click an element, adding context if Playwright cannot interact with it."""
        try:
            locator.click()
        except PlaywrightError as error:
            raise RuntimeError(f"Could not click {locator}") from error

    def fill(self, locator: Locator, value: str) -> None:
        """Replace the value in an input field."""
        try:
            locator.fill(value)
        except PlaywrightError as error:
            raise RuntimeError(f"Could not fill {locator}") from error

    def read_text(self, locator: Locator) -> str:
        """Return the visible text of an element without surrounding whitespace."""
        try:
            return locator.inner_text().strip()
        except PlaywrightError as error:
            raise RuntimeError(f"Could not read text from {locator}") from error
