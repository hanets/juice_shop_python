"""Models for Juice Shop API requests and responses."""

from .base import CamelModel
from .register import (
    RegisterUserRequest,
    RegisterUserResponse,
    SecurityQuestion,
)

__all__ = [
    "CamelModel",
    "SecurityQuestion",
    "RegisterUserRequest",
    "RegisterUserResponse",
]
