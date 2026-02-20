import os
import uuid
import pytest
import allure

from playwright.sync_api import Page
from pytest import FixtureRequest

from api import ApiClient, UserFactory


# ── Failure attachments ────────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store the test outcome on the item so fixtures can read it."""
    outcome = yield
    report = outcome.get_result()
    # expose call-phase result as item.rep_call
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def attach_on_failure(request: FixtureRequest, page: Page):
    """Attach screenshot, full-page screenshot, HTML and console log on failure."""
    # Collect browser console messages during the test
    console_messages: list[str] = []
    page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))

    yield  # run the test

    # Only attach artifacts when the test itself failed
    rep = getattr(request.node, "rep_call", None)
    if rep is None or not rep.failed:
        return

    test_name = request.node.name

    # 1. Screenshot (viewport)
    try:
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name=f"{test_name} — screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        pass

    # 2. Full-page screenshot
    try:
        full_screenshot = page.screenshot(full_page=True)
        if not screenshot or len(full_screenshot) != len(screenshot):
            allure.attach(
                full_screenshot,
                name=f"{test_name} — full-page screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
    except Exception:
        pass

    # 3. Page HTML source
    try:
        html_source = page.content()
        allure.attach(
            html_source,
            name=f"{test_name} — page source",
            attachment_type=allure.attachment_type.XML,
        )
    except Exception:
        pass

    # 4. Browser console log
    if console_messages:
        allure.attach(
            "\n".join(console_messages),
            name=f"{test_name} — console log",
            attachment_type=allure.attachment_type.TEXT,
        )


# ── Session fixtures ───────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def base_url():
    """Base URL for the Juice Shop instance. Can be overridden with env var.

    Default: http://localhost:3000
    """
    return os.getenv("JUICE_SHOP_BASE_URL", "http://localhost:3000")


@pytest.fixture(scope="session")
def api_request_context(playwright, base_url):
    """Create a Playwright API request context for the test session."""
    ctx = playwright.request.new_context(base_url=base_url)
    yield ctx
    ctx.dispose()


@pytest.fixture
def api_client(api_request_context):
    """Return an `ApiClient` bound to the session request context."""
    return ApiClient(api_request_context)


@pytest.fixture
def api_user(api_client):
    """Register and log in a fresh test user via API.

    Returns a dict with `email`, `password` and `login_response` (Playwright Response).
    The fixture asserts that registration and login responses are successful.
    """
    email = f"test_user_{uuid.uuid4().hex[:8]}@example.com"
    password = "123456"

    # Register using UserFactory
    req = UserFactory.register_user_request(email, password)
    reg_resp = api_client.register_user(req)
    assert reg_resp.status == 201 or reg_resp.status == 200, (
        f"Registration failed ({reg_resp.status}): {reg_resp.text()}")

    # Login
    login_resp = api_client.login_user(email, password)
    assert login_resp.status in (200, 201), (
        f"Login failed ({login_resp.status}): {login_resp.text()}")

    return {"email": email, "password": password, "login_response": login_resp}
