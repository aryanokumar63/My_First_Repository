# Simple Playwright POM

This small UI test project uses Python, pytest, and Playwright.

## Structure

- `config/settings.py` holds the site URL, timeout, and sample test credentials.
- `pages/base_page.py` holds browser actions shared by page objects.
- `pages/login_page.py` holds the login page's locators and login actions.
- `tests/test_login.py` runs the login test and checks its result.
- `pytest.ini` tells pytest where tests live.
- `requirements.txt` lists the Python packages the framework needs.

## Setup and run

Run these commands in the project terminal:

```bash
pip install -r requirements.txt
playwright install chromium
pytest -v
```

The sample Sauce Demo username and password are in `config/settings.py`. You can override them with `TEST_USERNAME` and `TEST_PASSWORD` environment variables.

## Execution flow

1. Pytest reads `pytest.ini` and discovers `tests/test_login.py`.
2. The `page` fixture from `pytest-playwright` starts a browser page.
3. The test creates `LoginPage(page)`; its parent `BasePage` sets the action and navigation timeouts.
4. `LoginPage` creates locators for the username, password, Login button, error message, and Products heading.
5. `open()` calls the shared `BasePage.open()` and navigates to `BASE_URL`.
6. `login(USERNAME, PASSWORD)` fills both fields and clicks Login.
7. Playwright's `expect(...).to_be_visible()` waits for the Products heading; if it does not appear before the timeout, the test fails with the locator assertion details.
8. If navigation or a form action raises a Playwright error, the page object raises a `RuntimeError` with workflow context and keeps the original error as its cause.
