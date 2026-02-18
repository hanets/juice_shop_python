"""
Usage examples for the Page Object Model classes

This file demonstrates how to use the page objects in your Playwright tests.
"""

from playwright.sync_api import Page
from .home_page import HomePage
from .login_page import LoginPage
from .register_page import RegisterPage
from .checkout_page import CheckoutPage


def example_basic_navigation(page: Page):
    """Example: Basic navigation and homepage interaction"""
    # Initialize HomePage
    home_page = HomePage(page)

    # Navigate to the application
    home_page.navigate_sync("http://localhost:3000/#/")

    # Dismiss popups/cookies
    home_page.dismiss_popup_and_cookies_sync()

    # Check how many products are visible
    product_count = home_page.get_visible_products_count_sync()
    print(f"Found {product_count} products on the homepage")

    # Verify user is not logged in initially
    home_page.verify_user_not_logged_in_sync()


def example_user_registration_and_login(page: Page):
    """Example: Complete user registration and login flow"""
    home_page = HomePage(page)

    # Setup
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()

    # Go to login page, then registration
    login_page = home_page.open_login_page_sync()
    login_page.register_link.click()

    # Register a new user
    register_page = RegisterPage(page)
    unique_email = register_page.register_user_sync(
        password="mypassword123", security_answer="mysecret"
    )

    # Login with the newly registered user
    login_page = LoginPage(page)
    login_page.email_field.fill(unique_email)
    login_page.password_field.fill("mypassword123")
    login_page.login_button.click()

    # Verify successful login
    home_page.verify_logged_in_sync()

    return unique_email


def example_shopping_flow(page: Page):
    """Example: Complete shopping flow including checkout"""
    home_page = HomePage(page)

    # First register and login a user
    unique_email = example_user_registration_and_login(page)

    # Add a product to the basket
    product_name = "Apple Juice (1000ml)"
    home_page.add_product_to_basket_sync(product_name)

    # Verify basket has the item
    home_page.verify_basket_items_count_sync(1)

    # Open basket and proceed to checkout
    home_page.open_basket_sync()

    # Complete checkout process
    checkout_page = CheckoutPage(page)
    checkout_page.checkout_sync()

    # Add shipping address
    checkout_page.add_address_sync(
        country="United States",
        name="John Doe",
        mobile="5551234567",
        zip_code="12345",
        address="123 Main Street",
        city="Anytown",
        state="California",
    )

    # Proceed to payment
    checkout_page.proceed_to_payment_sync()


def example_navigation_features(page: Page):
    """Example: Using navigation features"""
    home_page = HomePage(page)

    # Setup
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()

    # Navigate to different sections
    home_page.navigate_to_feedback_sync()  # Goes to feedback/contact page

    # Go back to home
    home_page.go_to_home_page_sync()

    # Navigate to About Us
    home_page.navigate_to_about_us_sync()


# Async versions (for async tests)
async def example_async_flow(page: Page):
    """Example: Using async versions of the methods"""
    home_page = HomePage(page)

    # Navigate and setup (async versions)
    await home_page.navigate("http://localhost:3000/#/")
    await home_page.dismiss_popup_and_cookies()

    # Add product (async)
    await home_page.add_product_to_basket("Apple Juice (1000ml)")

    # Open basket (async)
    await home_page.open_basket()

    # Checkout flow (async)
    checkout_page = CheckoutPage(page)
    await checkout_page.checkout()
    await checkout_page.add_address()
    await checkout_page.proceed_to_payment()


# Testing helpers
def setup_logged_in_user(page: Page) -> str:
    """Helper function to quickly setup a logged-in user for tests"""
    return example_user_registration_and_login(page)


def add_product_to_basket_as_guest(page: Page, product_name: str):
    """Helper function to add product as guest user"""
    home_page = HomePage(page)
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()
    home_page.add_product_to_basket_sync(product_name)
