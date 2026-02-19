from playwright.sync_api import Page, expect

from page_objects import HomePage


def test_juice_shop_title(page: Page):
    home_page = HomePage(page)
    home_page.navigate_sync("http://localhost:3000/#/")
    # Expect the title to contain "OWASP Juice Shop"
    expect(page).to_have_title("OWASP Juice Shop")


def test_dismiss_cookies_and_navigate(page: Page):
    """Test dismissing popup and cookies, then verify basic navigation"""
    home_page = HomePage(page)
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()

    # Verify we can see product cards after dismissing popups
    products_count = home_page.get_visible_products_count_sync()
    assert products_count > 0, "Should see products on homepage"


def test_login_flow(page: Page):
    """Test opening login page flow"""
    home_page = HomePage(page)
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()

    # Open login page
    login_page = home_page.open_login_page_sync()

    # Verify we're on login page (check for login button)
    expect(login_page.login_button).to_be_visible()


def test_add_product_to_basket(page: Page):
    """Test adding a product to the basket without logging in first"""
    home_page = HomePage(page)
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()

    # Verify user is not logged in
    home_page.verify_user_not_logged_in_sync()

    # Try to add a product - should still work for guest users
    home_page.add_product_to_basket_sync("Apple Juice (1000ml)")
