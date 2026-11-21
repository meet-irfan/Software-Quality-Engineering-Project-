"""Page Object for the Products (inventory) page."""
from playwright.sync_api import Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title = page.locator("[data-test='title']")
        self.items = page.locator("[data-test='inventory-item']")
        self.item_names = page.locator("[data-test='inventory-item-name']")
        self.item_prices = page.locator("[data-test='inventory-item-price']")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.menu_button = page.locator("#react-burger-menu-btn")  # unique id
        self.logout_link = page.locator("[data-test='logout-sidebar-link']")

    # ---- helpers ---------------------------------------------------------
    def _item(self, name: str):
        """The product card that contains the given product name."""
        return self.items.filter(has_text=name)

    # ---- actions ---------------------------------------------------------
    def add_to_cart(self, name: str) -> None:
        self._item(name).get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, name: str) -> None:
        self._item(name).get_by_role("button", name="Remove").click()

    def sort_by(self, option_value: str) -> None:
        """option_value: az, za, lohi or hilo."""
        self.sort_dropdown.select_option(option_value)

    def open_product(self, name: str) -> None:
        self.item_names.filter(has_text=name).click()

    def open_cart(self) -> None:
        self.cart_link.click()

    def logout(self) -> None:
        self.menu_button.click()
        self.logout_link.click()

    # ---- reading data ----------------------------------------------------
    def get_names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def get_prices(self) -> list[float]:
        return [float(text.replace("$", "")) for text in self.item_prices.all_inner_texts()]

    def price_text_of(self, name: str) -> str:
        return self._item(name).locator("[data-test='inventory-item-price']").inner_text()

    def price_of(self, name: str) -> float:
        return float(self.price_text_of(name).replace("$", ""))
