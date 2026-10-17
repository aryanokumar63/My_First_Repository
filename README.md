# Simple Playwright POM

This small UI test project uses Python, pytest, and Playwright.

## Structure

- `config/settings.py` holds the site URL, timeout, and sample test credentials.
- `pages/base_page.py` holds browser actions shared by page objects.
- `pages/login_page.py` holds the login page's locators, submit actions, and error capture.
- `pages/inventory_page.py` holds inventory locators and the logout action.
- `tests/functional/test_login_validation.py` checks invalid credentials and boundary inputs.
- `tests/integration/test_login_flow.py` checks complete login, retry, keyboard submit, inventory, and logout flows.
- `tests/conftest.py` provides fresh login pages and a reusable authenticated inventory page.
- `pytest.ini` tells pytest where tests live and runs Playwright in a visible, slowed-down browser.
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

1. Pytest reads `pytest.ini` and discovers test files under `tests/`.
2. The `page` fixture from `pytest-playwright` starts a browser page.
3. The shared `login_page` fixture creates `LoginPage(page)`; its parent `BasePage` sets the action and navigation timeouts.
4. `LoginPage` creates locators for the username, password, Login button, and error message. `InventoryPage` owns selectors for the inventory screen and logout menu.
5. `open()` calls the shared `BasePage.open()` and navigates to `BASE_URL`.
6. Functional cases submit invalid or boundary credentials and compare the captured alert text with the expected validation message.
7. Integration cases use the authenticated fixture or exercise a full workflow, then assert inventory, retry, keyboard submission, or logout behavior.
8. Playwright's `expect(...)` assertions wait for the expected page state; failures include locator details. Page-object browser actions wrap Playwright errors with workflow context.

The functional suite covers empty fields, each missing-field case, incorrect credentials, case sensitivity, surrounding whitespace, and the locked-out account. The integration suite covers valid login, successful login with Enter, recovery after a rejected attempt, and logout. Error capture is centralized in `LoginPage.get_error_message()`, while test cases assert the exact site message.

Playwright is configured with `--headed --slowmo 500`, so the browser window is visible and actions are slowed by 500 milliseconds. The browser closes when the test completes.
