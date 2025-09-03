from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.utils import parse_jwt_header, parse_admin_cookie


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dep = Annotated[Session, Depends(get_db)]


def get_current_user_from_jwt(db: db_dep, request: Request) -> User:
    """Bearer JWT orqali foydalanuvchini olish"""
    user = parse_jwt_header(request, db)
    return user


current_user_jwt_dep = Annotated[User, Depends(get_current_user_from_jwt)]


def get_current_admin_from_cookie(db: db_dep, request: Request) -> User:
    """Admin cookie orqali foydalanuvchini olish"""
    user = parse_admin_cookie(request, db)
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user


current_admin_cookie_dep = Annotated[User, Depends(get_current_admin_from_cookie)]
