from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.security import hash_password, verify_password


class AuthService:
    @staticmethod
    def register(
        db: Session,
        payload: UserCreate,
    ):
        existing_user = UserRepository.get_by_email(
            db,
            payload.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        hashed_password = hash_password(
            payload.password,
        )

        return UserRepository.create(
            db,
            payload.email,
            hashed_password,
        )

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str,
    ):
        user = UserRepository.get_by_email(
            db,
            email,
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if not verify_password(
            password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )

        access_token = create_access_token(user.id)

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
