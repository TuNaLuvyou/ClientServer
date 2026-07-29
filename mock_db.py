from __future__ import annotations

from passlib.context import CryptContext

from schemas import UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mock database lưu trên RAM.
# Cấu trúc: {"username": {"username": str, "password": str, "role": str}}
def _build_user(username: str, password: str, role: str) -> dict[str, str]:
    return {
        "username": username,
        "password": pwd_context.hash(password),
        "role": role,
    }


fake_users_db: dict[str, dict[str, str]] = {
    "admin01": _build_user("admin01", "admin123", "admin"),
    "waiter01": _build_user("waiter01", "waiter123", "waiter"),
    "bartender01": _build_user("bartender01", "bartender123", "bartender"),
    "manager01": _build_user("manager01", "manager123", "manager"),
}


def get_user(username: str) -> UserInDB | None:
    """Lấy user từ mock database theo username."""

    user_data = fake_users_db.get(username)
    if user_data is None:
        return None
    return UserInDB(**user_data)


def save_user(user: UserInDB) -> UserInDB:
    """Lưu hoặc cập nhật user vào mock database."""

    fake_users_db[user.username] = user.model_dump()
    return user
