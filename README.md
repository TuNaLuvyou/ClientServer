# ClientServer

Backend FastAPI nhỏ cho chức năng đăng nhập, đăng ký và quản lý user bằng dữ liệu giả lưu trong bộ nhớ.

## Chức năng

- Đăng ký user theo role
- Đăng nhập bằng JSON body và nhận JWT access token
- Lấy thông tin user hiện tại từ token
- Lưu dữ liệu hoàn toàn trong RAM (`mock_db.py`)

## Công nghệ sử dụng

- FastAPI
- Uvicorn
- Passlib + bcrypt
- python-jose

## Cài đặt môi trường

Tạo môi trường ảo và cài dependency:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Chạy server

Từ thư mục project, chạy:

```bash
cd /Users/trantu/Documents/Python/ClientServer
source venv/bin/activate
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Mở Swagger docs tại:

```text
http://127.0.0.1:8000/docs
```

## Tài khoản admin mặc định

Mock database đã có sẵn tài khoản admin:

- username: `admin01`
- password: `admin123`

Bạn đăng nhập bằng tài khoản này trước, sau đó mới tạo các user khác.

## Luồng API

### 1. Đăng nhập

`POST /auth/login`

Request body:

```json
{
  "username": "admin01",
  "password": "admin123"
}
```

Response:

```json
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

### 2. Tạo user mới

`POST /auth/register`

Headers:

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

Request body:

```json
{
  "username": "waiter02",
  "password": "waiter123",
  "role": "waiter"
}
```

Chỉ user có role `admin` mới được phép tạo tài khoản mới.

### 3. Lấy user hiện tại

`GET /users/me`

Headers:

```http
Authorization: Bearer <access_token>
```

## Thunder Client

1. Gửi `POST /auth/login` với body JSON.
2. Copy `access_token` trả về.
3. Gửi `POST /auth/register` kèm header `Authorization: Bearer <access_token>`.
4. Body của user mới vẫn để dạng JSON.

## Ghi chú

- Login hiện dùng JSON body, không phải OAuth2 form data.
- Dữ liệu chỉ lưu trong bộ nhớ nên khi restart server, toàn bộ user sẽ mất.
- Nếu thay đổi dependency, nên giữ `bcrypt<5` để tương thích với Passlib.
