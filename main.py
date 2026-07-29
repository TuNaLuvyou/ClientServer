from __future__ import annotations

from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status

from auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user, get_password_hash
from mock_db import fake_users_db, save_user
from schemas import LoginRequest, Token, UserCreate, UserResponse, UserInDB

app = FastAPI(
    title="Cafe Order & Revenue Management API",
    description="Hệ thống Authentication dùng mock data trên RAM cho quán cafe.",
    version="1.0.0",
)

VALID_ROLES = {"admin", "waiter", "bartender", "manager"}


@app.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, current_user: UserInDB = Depends(get_current_user)) -> UserResponse:
    """Chỉ admin mới được tạo tài khoản cho các user khác."""

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ admin mới có quyền tạo tài khoản.",
        )

    if user.role not in VALID_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role không hợp lệ. Chỉ chấp nhận waiter, bartender hoặc manager.",
        )

    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username đã tồn tại.",
        )

    new_user = UserInDB(
        username=user.username,
        password=get_password_hash(user.password),
        role=user.role,
    )
    save_user(new_user)
    return UserResponse(username=new_user.username, role=new_user.role)


@app.post("/auth/login", response_model=Token)
def login(credentials: LoginRequest) -> Token:
    """Đăng nhập bằng username/password và trả về JWT."""

    user = authenticate_user(credentials.username, credentials.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username hoặc password không đúng.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me", response_model=UserResponse)
def read_current_user(current_user: UserInDB = Depends(get_current_user)) -> UserResponse:
    """Lấy thông tin user đang đăng nhập, không trả về password."""

    return UserResponse(username=current_user.username, role=current_user.role)
