from __future__ import annotations

import unittest

from app import create_app
from app.controllers.user_controller import UserController


class FakeRouteService:
    def __init__(self) -> None:
        self.users = [
            {
                "id": 1,
                "name": "William",
                "email": "william@email.com",
                "is_active": True,
                "created_at": "2026-04-16T00:00:00",
                "updated_at": "2026-04-16T00:00:00",
                "deleted_at": None,
            }
        ]

    def list_users(self, limit: int = 100, offset: int = 0):
        return self.users[offset : offset + limit]

    def get_user(self, user_id: int):
        if user_id != 1:
            raise ValueError("Usuário não encontrado")
        return self.users[0]

    def register_user(self, name: str, email: str, password: str):
        if not name or not email or not password:
            raise ValueError("Dados obrigatórios ausentes")
        return {
            "id": 2,
            "name": name,
            "email": email,
            "is_active": True,
            "created_at": "2026-04-16T00:00:00",
            "updated_at": "2026-04-16T00:00:00",
            "deleted_at": None,
        }

    def update_user(self, user_id: int, **kwargs):
        if user_id != 1:
            raise ValueError("Usuário não encontrado")
        user = dict(self.users[0])
        user.update({k: v for k, v in kwargs.items() if v is not None})
        return user

    def deactivate_user(self, user_id: int):
        if user_id != 1:
            raise ValueError("Usuário não encontrado")


class UserRoutesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.original_service = UserController._service
        UserController._service = FakeRouteService()
        self.app = create_app()
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        UserController._service = self.original_service

    def test_get_users_returns_success(self) -> None:
        response = self.client.get("/users/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_post_users_returns_created(self) -> None:
        response = self.client.post(
            "/users/",
            json={"name": "Ana", "email": "ana@email.com", "password": "Senha123"},
        )

        body = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(body["name"], "Ana")

    def test_post_users_with_empty_payload_returns_bad_request(self) -> None:
        response = self.client.post("/users/", json={})

        body = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(body["message"], "Dados obrigatórios ausentes")

    def test_get_unknown_user_returns_not_found(self) -> None:
        response = self.client.get("/users/999")

        body = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(body["message"], "Usuário não encontrado")


if __name__ == "__main__":
    unittest.main()
