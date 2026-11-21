"""Central settings for the SauceDemo suite (published demo credentials only)."""
import os

# Can be overridden:  BASE_URL=https://www.saucedemo.com pytest
BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com").rstrip("/")

# Standard demo users published on the SauceDemo login page
PASSWORD = "secret_sauce"
USERS = {
    "standard": "standard_user",
    "locked": "locked_out_user",
    "problem": "problem_user",
    "glitch": "performance_glitch_user",
}
