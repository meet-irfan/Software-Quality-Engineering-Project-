"""Task 3 - 'Hello World' test: proves the environment works end to end."""
from playwright.sync_api import expect

from config import BASE_URL


def test_hello_world_sauce_demo_opens(page):
    page.goto(BASE_URL)
    expect(page).to_have_title("Swag Labs")
