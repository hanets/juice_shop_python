import os
import uuid
import pytest

from api import ApiClient, UserFactory


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

