"""Scenarios 1, 2, 3, 4 and 10 - login and logout."""
import re

import pytest
from playwright.sync_api import expect

from config import PASSWORD, USERS
from utils.data_reader import read_csv

LOGIN_DATA = read_csv("login_data.csv")  # data-driven: 5 data sets from CSV
INVENTORY_URL = re.compile(r"inventory\.html")


# Scenario 1
def test_login_valid_standard_user_shows_products(login_page, inventory_page, page):
    login_page.login(USERS["standard"], PASSWORD)

    expect(page).to_have_url(INVENTORY_URL)
    expect(inventory_page.title).to_have_text("Products")
    expect(inventory_page.items).to_have_count(6)


# Scenario 2
def test_login_invalid_password_shows_error(login_page, page):
    login_page.login(USERS["standard"], "wrong_password")

    expect(login_page.error_message).to_contain_text("Username and password do not match")
    expect(login_page.login_button).to_be_visible()  # still on the login page
    expect(page).not_to_have_url(INVENTORY_URL)


# Scenarios 3 and 4 (empty username, empty password, both empty, unknown user, locked-out user)
@pytest.mark.parametrize("row", LOGIN_DATA, ids=[r["case_id"] for r in LOGIN_DATA])
def test_login_negative_cases_data_driven(login_page, page, row):
    login_page.login(row["username"], row["password"])

    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text(row["expected_error"])
    expect(page).not_to_have_url(INVENTORY_URL)


# Scenario 10 (part 1)
def test_logout_returns_to_login_page(logged_in, inventory_page, login_page):
    inventory_page.logout()

    expect(login_page.login_button).to_be_visible()
    expect(login_page.username_input).to_be_empty()


# Scenario 10 (part 2)
def test_back_button_after_logout_does_not_restore_session(
    logged_in, inventory_page, login_page, page
):
    inventory_page.logout()
    expect(login_page.login_button).to_be_visible()

    page.go_back()

    # Session is gone: the user must still see the login form and no products
    expect(login_page.login_button).to_be_visible()
    expect(inventory_page.items).to_have_count(0)
