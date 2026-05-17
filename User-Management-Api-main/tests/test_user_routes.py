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
        self._next_id = 2

    def list_users(self, limit: int = 100, offset: int = 0):
        active_users = [user for user in self.users if user["is_active"] and user["deleted_at"] is None]
        return active_users[offset : offset + limit]

    def get_user(self, user_id: int):
        for user in self.users:
            if user["id"] == user_id:
                return user
        raise ValueError("Usuário não encontrado")

    def register_user(self, name: str, email: str, password: str):
        if not name or not email or not password:
            raise ValueError("Dados obrigatórios ausentes")

        user = {
            "id": self._next_id,
            "name": name,
            "email": email,
            "is_active": True,
            "created_at": "2026-04-16T00:00:00",
            "updated_at": "2026-04-16T00:00:00",
            "deleted_at": None,
        }
        self._next_id += 1
        self.users.append(user)
        return user

    def update_user(self, user_id: int, **kwargs):
        for user in self.users:
            if user["id"] != user_id:
                continue
            if user["deleted_at"] is not None:
                raise ValueError("Usuário não encontrado")
            for key, value in kwargs.items():
                if value is not None:
                    if key == "password":
                        continue
                    user[key] = value
            user["updated_at"] = "2026-04-16T01:00:00"
            return user
        raise ValueError("Usuário não encontrado")

    def deactivate_user(self, user_id: int):
        for user in self.users:
            if user["id"] != user_id:
                continue
            if user["deleted_at"] is not None:
                raise ValueError("Usuário não encontrado")
            user["is_active"] = False
            user["deleted_at"] = "2026-04-16T02:00:00"
            return
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

    def test_api_full_user_flow_is_usable(self) -> None:
        create_response = self.client.post(
            "/users/",
            json={"name": "Ana", "email": "ana@email.com", "password": "Senha123"},
        )
        created_user = create_response.get_json()

        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(created_user["name"], "Ana")
        self.assertEqual(created_user["email"], "ana@email.com")

        user_id = created_user["id"]

        get_response = self.client.get(f"/users/{user_id}")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.get_json()["id"], user_id)

        update_response = self.client.put(
            f"/users/{user_id}",
            json={"name": "Ana Silva", "email": "ana.silva@email.com"},
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.get_json()["name"], "Ana Silva")

        delete_response = self.client.delete(f"/users/{user_id}")
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_response.get_json()["message"], "Usuário desativado com sucesso")

        list_response = self.client.get("/users/")
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.get_json()), 1)


if __name__ == "__main__":
    unittest.main()
