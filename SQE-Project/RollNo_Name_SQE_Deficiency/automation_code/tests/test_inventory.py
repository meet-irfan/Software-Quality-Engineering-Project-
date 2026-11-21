"""Scenarios 5 and 11 - sorting products and the product detail page."""
import re

import pytest
from playwright.sync_api import expect

# (dropdown value, what is sorted, descending?)
SORT_CASES = [
    ("az", "name", False),
    ("za", "name", True),
    ("lohi", "price", False),
    ("hilo", "price", True),
]
PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Fleece Jacket"]


# Scenario 5
@pytest.mark.parametrize(
    "option, key, descending",
    SORT_CASES,
    ids=["name_az", "name_za", "price_low_high", "price_high_low"],
)
def test_sort_products(logged_in, inventory_page, option, key, descending):
    expect(inventory_page.items).to_have_count(6)

    # Work out the expected order from the unsorted data, then let the app sort
    if key == "name":
        expected = sorted(inventory_page.get_names(), reverse=descending)
    else:
        expected = sorted(inventory_page.get_prices(), reverse=descending)

    inventory_page.sort_by(option)

    # to_have_text(list) retries until the whole list matches (auto-wait, no sleep)
    if key == "name":
        expect(inventory_page.item_names).to_have_text(expected)
    else:
        expect(inventory_page.item_prices).to_have_text([f"${p:.2f}" for p in expected])


# Scenario 11
@pytest.mark.parametrize("product", PRODUCTS)
def test_product_detail_matches_inventory_list(
    logged_in, inventory_page, product_page, page, product
):
    list_price = inventory_page.price_text_of(product)

    inventory_page.open_product(product)

    expect(page).to_have_url(re.compile(r"inventory-item\.html"))
    expect(product_page.name).to_have_text(product)
    expect(product_page.price).to_have_text(list_price)
