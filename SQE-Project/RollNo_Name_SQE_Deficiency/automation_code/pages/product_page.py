"""Page Object for a single product detail page."""
from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.name = page.locator("[data-test='inventory-item-name']")
        self.price = page.locator("[data-test='inventory-item-price']")
        self.back_button = page.locator("[data-test='back-to-products']")
