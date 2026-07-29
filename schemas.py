from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

RoleType = Literal["admin", "waiter", "bartender", "manager"]


class UserBase(BaseModel):
    """Thông tin chung của user trong hệ thống."""

    username: str = Field(..., min_length=3, max_length=50)
    role: RoleType


class UserCreate(UserBase):
    """Schema dùng cho API đăng ký."""

    password: str = Field(..., min_length=6, max_length=128)


class UserResponse(UserBase):
    """Schema trả về cho client, không bao gồm mật khẩu."""


class UserInDB(UserBase):
    """Schema nội bộ để lưu trữ user đã hash mật khẩu."""

    password: str


class LoginRequest(BaseModel):
    """Schema dùng cho API đăng nhập theo JSON body."""

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "admin01",
                "password": "admin123",
            }
        }
    }


class Token(BaseModel):
    """Schema phản hồi sau khi đăng nhập thành công."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Payload được đọc từ JWT."""

    username: Optional[str] = None
    role: Optional[RoleType] = None
