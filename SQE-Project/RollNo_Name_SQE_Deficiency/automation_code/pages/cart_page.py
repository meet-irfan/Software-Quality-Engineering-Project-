"""Page Object for the shopping cart page."""
from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.items = page.locator("[data-test='inventory-item']")
        self.item_names = page.locator("[data-test='inventory-item-name']")
        self.checkout_button = page.locator("[data-test='checkout']")

    def remove(self, name: str) -> None:
        self.items.filter(has_text=name).get_by_role("button", name="Remove").click()

    def checkout(self) -> None:
        self.checkout_button.click()
