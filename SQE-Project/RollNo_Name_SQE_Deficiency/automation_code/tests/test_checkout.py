"""Scenarios 8, 9 and 12 - checkout end to end, validation messages, totals."""
import re

import pytest
from playwright.sync_api import expect

from utils.data_reader import read_csv
from utils.flows import start_checkout

CHECKOUT_DATA = read_csv("checkout_data.csv")  # data-driven: 3 data sets from CSV
BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


# Scenario 8
def test_checkout_end_to_end_shows_order_complete(
    logged_in, inventory_page, cart_page, checkout_page, page
):
    start_checkout(inventory_page, cart_page, [BACKPACK])
    expect(page).to_have_url(re.compile(r"checkout-step-one\.html"))

    checkout_page.fill_information("Test", "User", "12345")
    checkout_page.continue_to_overview()
    expect(page).to_have_url(re.compile(r"checkout-step-two\.html"))

    checkout_page.finish()
    expect(page).to_have_url(re.compile(r"checkout-complete\.html"))
    expect(checkout_page.complete_header).to_have_text("Thank you for your order!")


# Scenario 9 (missing first name / last name / postal code)
@pytest.mark.parametrize("row", CHECKOUT_DATA, ids=[r["case_id"] for r in CHECKOUT_DATA])
def test_checkout_missing_field_shows_validation_message(
    logged_in, inventory_page, cart_page, checkout_page, page, row
):
    start_checkout(inventory_page, cart_page, [BACKPACK])

    checkout_page.fill_information(row["first_name"], row["last_name"], row["postal_code"])
    checkout_page.continue_to_overview()

    expect(checkout_page.error_message).to_contain_text(row["expected_error"])
    expect(page).to_have_url(re.compile(r"checkout-step-one\.html"))  # did not move on


# Scenario 12
def test_checkout_overview_totals_are_correct(
    logged_in, inventory_page, cart_page, checkout_page
):
    chosen = [BACKPACK, BIKE_LIGHT]
    expected_item_total = sum(inventory_page.price_of(name) for name in chosen)

    start_checkout(inventory_page, cart_page, chosen)
    checkout_page.fill_information("Test", "User", "12345")
    checkout_page.continue_to_overview()
    expect(checkout_page.total_label).to_be_visible()

    item_total = checkout_page.item_total()
    tax = checkout_page.tax()
    total = checkout_page.total()

    assert item_total == pytest.approx(expected_item_total, abs=0.001), "item total != sum of prices"
    assert total == pytest.approx(item_total + tax, abs=0.01), "total != item total + tax"
