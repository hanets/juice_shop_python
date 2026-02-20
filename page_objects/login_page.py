from playwright.sync_api import Page
import allure


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_field = page.get_by_role(
            "textbox", name="Text field for the login email"
        )
        self.password_field = page.get_by_role(
            "textbox", name="Text field for the login password"
        )
        self.login_button = page.get_by_role("button", name="Login", exact=True)
        self.register_link = page.get_by_role("link", name="Not yet a customer?")

    @allure.step
    def login(self, email: str, password: str):
        self.email_field.fill(email)
        self.password_field.fill(password)
        self.login_button.click()

    @allure.step
    def go_to_register(self):
        self.register_link.click()
