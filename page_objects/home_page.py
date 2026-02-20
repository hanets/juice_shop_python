from playwright.sync_api import Page, expect

from .login_page import LoginPage


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.dismiss_button = page.locator("text=Dismiss")
        self.dismiss_cookie_button = page.locator(
            "[aria-label='dismiss cookie message']"
        )
        self.account_menu = page.locator("#navbarAccount")
        self.login_button = page.locator("#navbarLoginButton")
        self.basket_link = page.get_by_text("Your Basket")
        self.home_button = page.locator("#homeButton")
        # Product cards on the homepage grid
        self.product_cards = page.locator("mat-card")
        # Navigation locators
        self.sidenav_toggle = page.get_by_role("button", name="open sidenav")
        self.contact_us_link = page.get_by_role("link", name="contact us page")
        self.about_us_link = page.get_by_role("link", name="about us")

    def navigate(self, url: str):
        self.page.goto(url)

    def go_to_home_page(self):
        self.home_button.click()

    def dismiss_popup_and_cookies(self):
        self.page.get_by_role("button", name="Close Welcome Banner").click()
        self.page.get_by_role("button", name="dismiss cookie message").click()

    def open_login_page(self) -> LoginPage:
        self.page.get_by_role("button", name="Show/hide account menu").click()
        self.page.get_by_role("menuitem", name="Go to login page").click()
        return LoginPage(self.page)

    def verify_user_logged_in(self):
        expect(self.basket_link).to_be_visible()
        self.account_menu.click()
        expect(self.page.get_by_role("menuitem", name="Logout")).to_be_visible()
        self.page.keyboard.press("Escape")

    def verify_user_not_logged_in(self):
        expect(self.basket_link).to_be_hidden()

    def get_visible_products_count(self) -> int:
        return self.product_cards.count()

    def verify_visible_products_count(self, expected_count: int):
        expect(self.product_cards).to_have_count(expected_count)

    def verify_basket_items_count(self, expected_count: int | str):
        basket_root = self.page.locator(".mdc-button__label", has_text="Your Basket")
        expect(basket_root.locator(".warn-notification")).to_have_text(
            expected_count if isinstance(expected_count, str) else str(expected_count)
        )

    def add_product_to_basket(self, product_name: str):
        product_card = self.page.locator("mat-card").filter(has_text=product_name)
        product_card.get_by_label("Add to Basket").click()
        expect(
            self.page.get_by_text(f"Placed {product_name} into basket.")
        ).to_be_visible()

    def open_basket(self):
        self.page.get_by_role("button", name="Show the shopping cart").click()

    def verify_logged_in(self):
        expect(
            self.page.get_by_role("button", name="Show the shopping cart")
        ).to_be_visible()
        expect(self.page.get_by_text("Your Basket")).to_be_visible()

    def navigate_to_feedback(self):
        """Navigate to the feedback page from the sidenav"""
        self.sidenav_toggle.click()
        self.contact_us_link.click()

    def navigate_to_about_us(self):
        """Navigate to About Us page from the sidenav"""
        self.sidenav_toggle.click()
        self.about_us_link.click()
