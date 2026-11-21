"""Shared fixtures and hooks for the whole suite.

- one browser per test session, a fresh browser context (clean cookies/storage) per test,
  so tests are independent and can run in any order
- automatic screenshot when a test fails (saved in screenshots/ and embedded in the HTML report)
"""
import base64
import re
from datetime import datetime
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from config import PASSWORD, USERS
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage

try:  # pytest-html is only needed for the HTML report
    import pytest_html
except ImportError:  # pragma: no cover
    pytest_html = None

SCREENSHOT_DIR = Path(__file__).resolve().parent / "screenshots"


# --------------------------------------------------------------------------
# Command line options:  pytest --browser-name firefox --show-browser
# --------------------------------------------------------------------------
def pytest_addoption(parser):
    parser.addoption(
        "--browser-name",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser to run the tests in (default: chromium)",
    )
    parser.addoption(
        "--show-browser",
        action="store_true",
        help="Run with a visible browser window instead of headless",
    )


# --------------------------------------------------------------------------
# Browser / page fixtures
# --------------------------------------------------------------------------
@pytest.fixture(scope="session")
def browser(request):
    name = request.config.getoption("--browser-name")
    headless = not request.config.getoption("--show-browser")
    with sync_playwright() as playwright:
        browser = getattr(playwright, name).launch(headless=headless)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """A brand-new, isolated browser context and page for every test."""
    context = browser.new_context(viewport={"width": 1366, "height": 768})
    page = context.new_page()
    yield page
    context.close()


# --------------------------------------------------------------------------
# Page object fixtures
# --------------------------------------------------------------------------
@pytest.fixture
def login_page(page):
    """Login page object, already opened in the browser."""
    login = LoginPage(page)
    login.open()
    return login


@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)


@pytest.fixture
def product_page(page):
    return ProductPage(page)


@pytest.fixture
def logged_in(login_page, page):
    """Log in as the standard user and wait until the Products page is shown."""
    login_page.login(USERS["standard"], PASSWORD)
    page.wait_for_url(re.compile(r"inventory\.html"))
    return page


# --------------------------------------------------------------------------
# Screenshot on failure
# --------------------------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when not in ("setup", "call") or not report.failed:
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    SCREENSHOT_DIR.mkdir(exist_ok=True)
    safe_name = re.sub(r"[^\w\-]+", "_", item.name)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = SCREENSHOT_DIR / f"FAIL_{safe_name}_{stamp}.png"
    try:
        page.screenshot(path=str(path), full_page=True)
    except Exception:  # the page may already be closed; do not hide the real failure
        return

    if pytest_html is not None:
        extras = getattr(report, "extras", [])
        extras.append(pytest_html.extras.png(base64.b64encode(path.read_bytes()).decode()))
        report.extras = extras
