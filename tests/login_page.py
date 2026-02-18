from playwright.sync_api import Page, Locator, expect


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

    async def login(self, email: str, password: str):
        await self.email_field.fill(email)
        await self.password_field.fill(password)
        await self.login_button.click()

    async def go_to_register(self):
        await self.register_link.click()
