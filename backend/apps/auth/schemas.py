from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator, EmailStr, Field

from settings import config
from apps.auth.utils import verify_email


class UserBase(BaseModel):
    """User base schema"""
    email: EmailStr
    password: str = Field(..., min_length=8)

    @validator('email')
    def check_email(cls, value):
        value = value.lower()
        if not verify_email(value):
            raise ValueError('This email is not valid')
        return value


class UserLogin(UserBase):
    """Log in request schema.
    Email and password inherits from parent"""
    expire_seconds: int = Field(
        config.TOKEN_EXPIRE_SECONDS, ge=1, le=86400
    )


class UserCreate(UserBase):
    """Sign up request schema
    Email and password inherits from parent"""
    name: str


class TokenResponse(BaseModel):
    """Response schema with token details."""
    access_token: str
    expires: datetime
    token_type: Optional[str] = 'Bearer'
