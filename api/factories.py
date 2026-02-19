"""Factory for creating test users."""

from .models import RegisterUserRequest, SecurityQuestion


class UserFactory:
    """Factory for building user request objects with sensible defaults."""

    @staticmethod
    def register_user_request(
        email: str,
        password: str = "123456",
        security_question_id: int = 1,
        security_answer: str = "answer",
    ) -> RegisterUserRequest:
        """Create a RegisterUserRequest with defaults.

        Args:
            email: user email address
            password: user password (default: "123456")
            security_question_id: ID of security question (default: 1)
            security_answer: user's security answer (default: "answer")

        Returns:
            RegisterUserRequest ready to pass to ApiClient.register_user()
        """
        security_question = SecurityQuestion(id=security_question_id)
        return RegisterUserRequest(
            email=email,
            password=password,
            password_repeat=password,
            security_question=security_question,
            security_answer=security_answer,
        )
