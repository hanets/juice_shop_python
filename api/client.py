"""Juice Shop API client using Playwright APIRequestContext."""

from typing import Any

from playwright.sync_api import APIRequestContext

from .models import RegisterUserRequest


class ApiClient:
    """HTTP client for Juice Shop API endpoints."""

    def __init__(self, request_context: APIRequestContext):
        """Create client with a Playwright `APIRequestContext`.

        Args:
            request_context: an instance of Playwright's APIRequestContext.
        """
        self.request = request_context

    def register_user(self, req: RegisterUserRequest) -> Any:
        """Register a user via POST to `/api/Users/`.

        Args:
            req: a RegisterUserRequest instance (use UserFactory.register_user_request() to create).

        Returns:
            Playwright Response object with status and response data.
        """
        payload = req.model_dump(by_alias=True)
        return self.request.post("/api/Users/", data=payload)

    def login_user(self, email: str, password: str) -> Any:
        """Log in a user via POST to `/rest/user/login`.

        Args:
            email: user email
            password: user password

        Returns:
            Playwright Response object so callers can extract tokens or response data.
        """
        payload = {"email": email, "password": password}
        return self.request.post("/rest/user/login", data=payload)
