from fastapi import APIRouter, HTTPException, status
from app import utils
from app.dependencies import db_dep, current_user_jwt_dep
from app.models import User
from app.schemas.auth import (
    UserRegister,
    UserRegisterOut,
    UserJWTLogin,
    JWTRefreshIn,
    TokenResponse,
)
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register", response_model=UserRegisterOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: db_dep):
  
    user_exists = db.query(User).filter(User.email == payload.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered."
        )

    hashed_pw = utils.hash_password(payload.password)

    new_user = User(
        email=payload.email,
        hashed_password=hashed_pw,
        is_active=True,
        is_admin=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.post("/jwt/me", response_model=UserRegisterOut)
async def jwt_me(current_user: current_user_jwt_dep):
    return current_user


@router.post("/login", response_model=TokenResponse)
def login(payload: UserJWTLogin, db: db_dep):
    # login with email
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not utils.verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = utils.create_jwt_token(
        data={"sub": user.id, "role": "admin" if user.is_admin else "user"},
        expires_minutes=15
    )

    refresh_token = utils.create_jwt_token(
        data={"sub": user.id, "type": "refresh"},
        expires_minutes=60 * 24 * 7
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )



@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: JWTRefreshIn, db: db_dep):
    try:
        decoded = utils.jwt.decode(
            payload.refresh_token,
            utils.SECRET_KEY,
            algorithms=[utils.ALGORITHM],
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = decoded.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    new_access_token = utils.create_jwt_token(
        data={"sub": user.id, "role": "admin" if user.is_admin else "user"},
        expires_minutes=15
    )

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=payload.refresh_token,
        token_type="bearer"
    )
