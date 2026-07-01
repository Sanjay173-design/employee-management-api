from datetime import datetime

from app.models.user_model import User
from app.repositories.user_repository import UserRepository

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


class AuthService:

    @staticmethod
    def signup(
        db,
        user_data
    ):

        existing_user = (
            UserRepository.get_user_by_email(
                db,
                user_data.email
            )
        )

        if existing_user:

            raise Exception(
                "Email already registered"
            )

        user = User(
            email=user_data.email,
            hashed_password=hash_password(
                user_data.password
            ),
            role="user",
            created_at=datetime.now()
        )

        return UserRepository.create_user(
            db,
            user
        )

    @staticmethod
    def login(
        db,
        login_data
    ):

        user = UserRepository.get_user_by_email(
            db,
            login_data.email
        )

        if not user:

            raise Exception(
                "Invalid credentials"
            )

        valid_password = verify_password(
            login_data.password,
            user.hashed_password
        )

        if not valid_password:

            raise Exception(
                "Invalid credentials"
            )

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }