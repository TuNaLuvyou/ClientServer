import unittest

from fastapi.testclient import TestClient

from main import app


class AuthFlowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_admin_can_create_user(self) -> None:
        login_response = self.client.post(
            "/auth/login",
            data={"username": "admin01", "password": "admin123"},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json()["access_token"]

        register_response = self.client.post(
            "/auth/register",
            json={"username": "newwaiter", "password": "waiter123", "role": "waiter"},
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(register_response.status_code, 201)
        self.assertEqual(register_response.json()["username"], "newwaiter")

    def test_non_admin_cannot_create_user(self) -> None:
        login_response = self.client.post(
            "/auth/login",
            data={"username": "waiter01", "password": "waiter123"},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json()["access_token"]

        register_response = self.client.post(
            "/auth/register",
            json={"username": "anotheruser", "password": "pass1234", "role": "waiter"},
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(register_response.status_code, 403)


if __name__ == "__main__":
    unittest.main()
