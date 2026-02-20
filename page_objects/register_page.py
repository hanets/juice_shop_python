import time

from playwright.sync_api import Page
import allure


class RegisterPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_field = page.get_by_role("textbox", name="Email address field")
        self.password_field = page.get_by_role("textbox", name="Field for the password")
        self.confirm_password_field = page.get_by_role(
            "textbox", name="Field to confirm the password"
        )
        self.security_question_dropdown = page.locator(
            ".mat-mdc-form-field.mat-mdc-form-field-type-mat-select > .mat-mdc-text-field-wrapper > .mat-mdc-form-field-flex > .mat-mdc-form-field-infix"
        )
        self.security_answer_field = page.get_by_role(
            "textbox", name="Field for the answer to the"
        )
        self.register_button = page.get_by_role("button", name="Button to complete the")

    @allure.step
    def generate_unique_email(self):
        return f"test{int(time.time())}@test.tt"

    @allure.step
    def register_user(
        self, password: str = "123456", security_answer: str = "test"
    ):
        unique_email = self.generate_unique_email()
        self.email_field.fill(unique_email)
        self.password_field.fill(password)
        self.confirm_password_field.fill(password)
        self.security_question_dropdown.click()
        self.page.get_by_role("option", name="Mother's maiden name?").click()
        self.security_answer_field.fill(security_answer)
        self.register_button.click()
        return unique_email
