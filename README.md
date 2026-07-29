# ClientServer

A small FastAPI backend for authentication and user management using in-memory mock data.

## Features

- Register users with role-based access control
- Login with JSON request body and receive a JWT access token
- Get the current authenticated user from the token
- Store data in memory only (`mock_db.py`)

## Tech Stack

- FastAPI
- Uvicorn
- Passlib + bcrypt
- python-jose

## Requirements

Install the project dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the server

From the project folder:

```bash
cd /Users/trantu/Documents/Python/ClientServer
source venv/bin/activate
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Open the Swagger docs:

```text
http://127.0.0.1:8000/docs
```

## Default admin account

The mock database already contains an admin account:

- username: `admin01`
- password: `admin123`

Use this account to log in first, then create other users.

## API Flow

### 1. Login

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

### 2. Create a new user

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

Only users with role `admin` can create new accounts.

### 3. Get current user

`GET /users/me`

Headers:

```http
Authorization: Bearer <access_token>
```

## Thunder Client

1. Send `POST /auth/login` with a JSON body.
2. Copy the returned `access_token`.
3. Send `POST /auth/register` with the `Authorization: Bearer <access_token>` header.
4. Use JSON body for the new user payload.

## Notes

- Login uses a JSON body, not OAuth2 form data.
- The app stores data only in memory, so all users are lost when the server restarts.
- If you change dependencies, keep `bcrypt<5` for compatibility with Passlib.
