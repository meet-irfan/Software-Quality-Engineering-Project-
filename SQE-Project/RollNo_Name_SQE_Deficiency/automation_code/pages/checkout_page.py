"""Page Object for the three checkout screens (information, overview, complete)."""
import re

from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Step one: your information
        self.first_name = page.locator("[data-test='firstName']")
        self.last_name = page.locator("[data-test='lastName']")
        self.postal_code = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.error_message = page.locator("[data-test='error']")
        # Step two: overview
        self.subtotal_label = page.locator("[data-test='subtotal-label']")
        self.tax_label = page.locator("[data-test='tax-label']")
        self.total_label = page.locator("[data-test='total-label']")
        self.finish_button = page.locator("[data-test='finish']")
        # Complete page
        self.complete_header = page.locator("[data-test='complete-header']")

    def fill_information(self, first: str, last: str, postal: str) -> None:
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)

    def continue_to_overview(self) -> None:
        self.continue_button.click()

    def finish(self) -> None:
        self.finish_button.click()

    @staticmethod
    def _amount(text: str) -> float:
        """'Item total: $39.98' -> 39.98"""
        return float(re.search(r"\$(\d+(?:\.\d+)?)", text).group(1))

    def item_total(self) -> float:
        return self._amount(self.subtotal_label.inner_text())

    def tax(self) -> float:
        return self._amount(self.tax_label.inner_text())

    def total(self) -> float:
        return self._amount(self.total_label.inner_text())
