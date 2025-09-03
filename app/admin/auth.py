from datetime import UTC, datetime, timedelta

from fastapi import Request, Response
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette_admin.auth import AuthProvider
from starlette_admin.exceptions import LoginFailed

from app.dependencies import get_db
from app.models import User
from app.utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    verify_password,
)


class AdminAuth(AuthProvider):
    """Custom admin authentication using JWT stored in cookies."""

    async def login(
        self,
        email: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        """Authenticate user and set JWT in cookies."""
        db: Session = next(get_db())
        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise LoginFailed("User not found.")
        if not user.is_admin:
            raise LoginFailed("User is not admin.")
        if not verify_password(password, user.hashed_password):
            raise LoginFailed("Invalid password.")

        # Token create
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": user.email,
            "exp": datetime.now(UTC) + access_token_expires,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        # Set cookie
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            secure=True,
            samesite="lax",
        )
        return response

    async def is_authenticated(self, request: Request) -> User | None:
        """Check if user is authenticated via JWT cookie."""
        token = request.cookies.get("access_token")
        if not token:
            return None

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if not email:
                return None

            db: Session = next(get_db())
            user = db.query(User).filter(User.email == email).first()

            if not user or not user.is_admin:
                return None

            exp = payload.get("exp")
            if exp and exp < datetime.now(UTC).timestamp():
                return None

            return user

        except JWTError:
            return None

    async def logout(self, request: Request, response: Response) -> Response:
        """Remove JWT cookie to logout."""
        response.delete_cookie("access_token")
        return response
