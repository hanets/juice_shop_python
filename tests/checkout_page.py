from playwright.sync_api import Page, Locator, expect


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.__checkout_button = page.get_by_role("button", name="Checkout")
        self.add_address_button = page.get_by_role("button", name="Add a new address")
        self.country_field = page.get_by_role("textbox", name="Country")
        self.name_field = page.get_by_role("textbox", name="Name")
        self.mobile_field = page.get_by_role("spinbutton", name="Mobile Number")
        self.zip_field = page.get_by_role("textbox", name="ZIP Code")
        self.address_field = page.get_by_role("textbox", name="Address")
        self.city_field = page.get_by_role("textbox", name="City")
        self.state_field = page.get_by_role("textbox", name="State")
        self.submit_address_button = page.get_by_role("button", name="Submit")
        self.proceed_to_payment_button = page.get_by_role(
            "button", name="Proceed to payment selection"
        )

    def checkout_sync(self):
        self.__checkout_button.click()

    def add_address_sync(
        self,
        country: str = "dsdsds",
        name: str = "ds",
        mobile: str = "1212212121",
        zip_code: str = "21212",
        address: str = "dsdsdff",
        city: str = "fdsfdsfds",
        state: str = "dsds",
    ):
        self.add_address_button.click()
        self.country_field.fill(country)
        self.name_field.fill(name)
        self.mobile_field.fill(mobile)
        self.zip_field.fill(zip_code)
        self.address_field.fill(address)
        self.city_field.fill(city)
        self.state_field.fill(state)
        # Click the Add New button (assuming it's the first div with that text)
        self.page.locator("div").filter(has_text="Add New").first.click()
        self.submit_address_button.click()

    def proceed_to_payment_sync(self):
        self.proceed_to_payment_button.click()

    async def checkout(self):
        await self.__checkout_button.click()

    async def add_address(
        self,
        country: str = "dsdsds",
        name: str = "ds",
        mobile: str = "1212212121",
        zip_code: str = "21212",
        address: str = "dsdsdff",
        city: str = "fdsfdsfds",
        state: str = "dsds",
    ):
        await self.add_address_button.click()
        await self.country_field.fill(country)
        await self.name_field.fill(name)
        await self.mobile_field.fill(mobile)
        await self.zip_field.fill(zip_code)
        await self.address_field.fill(address)
        await self.city_field.fill(city)
        await self.state_field.fill(state)
        # Click the Add New button (assuming it's the first div with that text)
        await self.page.locator("div").filter(has_text="Add New").first.click()
        await self.submit_address_button.click()

    async def proceed_to_payment(self):
        await self.proceed_to_payment_button.click()
