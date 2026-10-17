"""Project settings, with environment variables available for overrides."""

import os

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
USERNAME = os.getenv("TEST_USERNAME", "standard_user")
PASSWORD = os.getenv("TEST_PASSWORD", "secret_sauce")
