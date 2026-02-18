from typing import Generator

import pandas as pd
import pytest
from playwright.sync_api import APIRequestContext, Page, Playwright, expect

from page_objects.checkout_page import CheckoutPage
from page_objects.home_page import HomePage
from page_objects.login_page import LoginPage
from page_objects.register_page import RegisterPage


def load_checkout_items():
    """Load test data from CSV file."""
    df = pd.read_csv("tests/checkout_items.csv")
    return [tuple(row) for row in df.values]


@pytest.mark.parametrize("item_name,quantity,price", load_checkout_items())
def test_checkout_with_item_data(page: Page, item_name, quantity, price):
    """Test checkout flow using item data from CSV"""
    home_page = HomePage(page)
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()
    login_page = home_page.open_login_page_sync()
    login_page.register_link.click()
    register_page = RegisterPage(page)
    unique_email = register_page.register_user_sync()
    login_page = LoginPage(page)
    login_page.email_field.fill(unique_email)
    login_page.password_field.fill("123456")
    login_page.login_button.click()
    home_page.verify_logged_in_sync()
    for _ in range(int(quantity)):
        home_page.add_product_to_basket_sync(item_name)
    home_page.open_basket_sync()
    checkout_page = CheckoutPage(page)
    checkout_page.checkout_sync()
    checkout_page.add_address_sync()


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    """Create API request context for API testing."""
    request_context = playwright.request.new_context()
    yield request_context
    request_context.dispose()


def test_full_checkout_flow(page: Page):
    """Test complete checkout flow: register -> login -> add product -> checkout -> add address"""
    home_page = HomePage(page)
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()
    login_page = home_page.open_login_page_sync()
    login_page.register_link.click()
    register_page = RegisterPage(page)
    unique_email = register_page.register_user_sync()
    login_page = LoginPage(page)
    login_page.email_field.fill(unique_email)
    login_page.password_field.fill("123456")
    login_page.login_button.click()
    home_page.verify_logged_in_sync()
    home_page.add_product_to_basket_sync("Apple Juice (1000ml)")
    home_page.open_basket_sync()
    checkout_page = CheckoutPage(page)
    checkout_page.checkout_sync()
    checkout_page.add_address_sync()


def test_register_user(page: Page):
    """Test user registration flow"""
    home_page = HomePage(page)
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()
    login_page = home_page.open_login_page_sync()
    login_page.register_link.click()
    register_page = RegisterPage(page)
    register_page.register_user_sync()
    login_page = LoginPage(page)
    expect(login_page.email_field).to_be_visible()


def test_add_multiple_products(page: Page):
    """Test adding multiple products to basket after login"""
    home_page = HomePage(page)
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()

    # Register and login user
    login_page = home_page.open_login_page_sync()
    login_page.register_link.click()

    register_page = RegisterPage(page)
    unique_email = register_page.register_user_sync()

    # Login
    login_page = LoginPage(page)
    login_page.email_field.fill(unique_email)
    login_page.password_field.fill("123456")
    login_page.login_button.click()

    # Add product to basket
    home_page.add_product_to_basket_sync("Apple Juice (1000ml)")

    # Verify basket has items
    home_page.verify_basket_items_count_sync(1)


def test_product_visibility(page: Page):
    """Test that products are visible on the homepage"""
    home_page = HomePage(page)
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()

    # Verify products are visible
    products_count = home_page.get_visible_products_count_sync()
    assert products_count > 0, "Should have visible products on homepage"
