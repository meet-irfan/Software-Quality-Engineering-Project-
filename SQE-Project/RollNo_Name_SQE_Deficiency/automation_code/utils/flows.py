"""Reusable multi-step flows, so the same steps are not copy-pasted in many tests."""


def start_checkout(inventory_page, cart_page, item_names: list[str]) -> None:
    """Add the given items, open the cart and click Checkout (ends on step one)."""
    for name in item_names:
        inventory_page.add_to_cart(name)
    inventory_page.open_cart()
    cart_page.checkout()
