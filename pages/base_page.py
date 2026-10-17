"""Shared browser behavior inherited by page objects."""

from playwright.sync_api import Error as PlaywrightError  # Common Playwright operation error.
from playwright.sync_api import Page  # Type of the browser tab supplied by pytest-playwright.

from config.settings import BASE_URL, DEFAULT_TIMEOUT  # Reuse the configured URL and timeout.


class BasePage:
    """Common browser actions; page-specific locators live in page classes."""

    def __init__(self, page: Page) -> None:
        self.page = page  # Keep the tab so the page object can use it.
        timeout_ms = DEFAULT_TIMEOUT * 1000  # Convert the readable seconds setting to ms.
        self.page.set_default_timeout(timeout_ms)  # Apply it to locator actions and assertions.
        self.page.set_default_navigation_timeout(timeout_ms)  # Apply it to page navigation too.

    def open(self, path: str = "") -> None:
        url = f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"  # Join base URL and path with one slash.
        try:  # Navigation can fail because of a timeout or browser/network problem.
            self.page.goto(url, wait_until="domcontentloaded")  # Open page and wait for its HTML.
        except PlaywrightError as error:  # Keep the browser error as the underlying cause.
            raise RuntimeError(f"Could not open {url}") from error  # Add the URL to the failure.
