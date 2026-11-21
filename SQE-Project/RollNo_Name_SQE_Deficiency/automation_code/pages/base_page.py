"""Base page: elements and helpers shared by every SauceDemo page."""
from playwright.sync_api import Page

from config import BASE_URL


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        # The cart icon lives in the header, so it exists on every logged-in page
        self.cart_link = page.locator("[data-test='shopping-cart-link']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")

    def open(self, path: str = "") -> None:
        self.page.goto(f"{BASE_URL}/{path}")
