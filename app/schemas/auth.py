from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "email": "email@example.com",
                "password": "password123",
            }
        },
    }


class UserRegisterOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_admin: bool
    joined_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "email": "realmadrid@example.com",
                "is_active": True,
                "is_superuser": False,
                "joined_at": "2025-01-01T13:00:00.000Z",
            }
        },
    }


class UserJWTLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "johndoe@example.com",
                "password": "secretpass123"
            }
        }
    }


class JWTRefreshIn(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "jwt_access_token_here",
                "refresh_token": "jwt_refresh_token_here",
                "token_type": "bearer",
            }
        }
    }
