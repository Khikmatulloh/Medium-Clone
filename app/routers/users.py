# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.user import UserOut, UserUpdate
from app.dependencies import db_dep, current_user_jwt_dep

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/me", response_model=UserOut)
def get_my_profile(current_user: current_user_jwt_dep):
    return current_user


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: db_dep):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/me", response_model=UserOut)
def update_my_profile(
    payload: UserUpdate,
    db: db_dep,
    current_user: current_user_jwt_dep
):
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_account(
    db: db_dep,
    current_user: current_user_jwt_dep
):
    db.delete(current_user)
    db.commit()
    return
