"""Scenarios 6 and 7 - add to cart and remove from cart."""
from playwright.sync_api import expect

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"
ONESIE = "Sauce Labs Onesie"


# Scenario 6 (one item)
def test_add_one_item_updates_badge_and_cart(logged_in, inventory_page, cart_page):
    inventory_page.add_to_cart(BACKPACK)

    expect(inventory_page.cart_badge).to_have_text("1")
    inventory_page.open_cart()
    expect(cart_page.items).to_have_count(1)
    expect(cart_page.item_names).to_have_text([BACKPACK])


# Scenario 6 (multiple items)
def test_add_multiple_items_updates_badge_and_cart(logged_in, inventory_page, cart_page):
    chosen = [BACKPACK, BIKE_LIGHT, ONESIE]
    for name in chosen:
        inventory_page.add_to_cart(name)

    expect(inventory_page.cart_badge).to_have_text("3")
    inventory_page.open_cart()
    expect(cart_page.items).to_have_count(3)
    # compare as sorted lists so the test does not depend on the cart's display order
    assert sorted(cart_page.item_names.all_inner_texts()) == sorted(chosen)


# Scenario 7
def test_remove_item_updates_badge_and_cart(logged_in, inventory_page, cart_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    expect(inventory_page.cart_badge).to_have_text("2")
    inventory_page.open_cart()

    cart_page.remove(BACKPACK)

    expect(cart_page.items).to_have_count(1)
    expect(cart_page.item_names).to_have_text([BIKE_LIGHT])
    expect(cart_page.cart_badge).to_have_text("1")


# Scenario 7 (edge: removing the last item makes the badge disappear)
def test_remove_last_item_hides_badge(logged_in, inventory_page, cart_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.open_cart()

    cart_page.remove(BACKPACK)

    expect(cart_page.items).to_have_count(0)
    expect(cart_page.cart_badge).to_have_count(0)
