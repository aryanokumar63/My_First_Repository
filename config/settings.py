"""Configuration used by the Sauce Demo login test."""

import os  # Read optional overrides from the environment.

# The page object opens this site; BASE_URL can override it when needed.
BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")

# Playwright uses this wait limit, in seconds, for actions and locator checks.
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))

# Sauce Demo publishes these credentials for its sample login page.
USERNAME = os.getenv("TEST_USERNAME", "standard_user")
PASSWORD = os.getenv("TEST_PASSWORD", "secret_sauce")
