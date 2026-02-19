"""Pydantic models for user registration requests and responses."""

from typing import Optional

from .base import CamelModel


class SecurityQuestion(CamelModel):
    id: int
    question: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class RegisterUserRequest(CamelModel):
    email: str
    password: str
    password_repeat: str
    security_question: SecurityQuestion
    security_answer: str


class RegisteredUserData(CamelModel):
    id: Optional[int] = None
    email: Optional[str] = None
    username: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class RegisterUserResponse(CamelModel):
    status: str
    data: RegisteredUserData
