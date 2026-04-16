from __future__ import annotations

import unittest
from copy import deepcopy
from typing import Any, Dict, List, Optional

from app.services.user_service import UserService


class FakeUserRepository:
    def __init__(self) -> None:
        self._users: List[Dict[str, Any]] = []
        self._next_id = 1

    def create_user(self, name: str, email: str, password_hash: str) -> Dict[str, Any]:
        user = {
            "id": self._next_id,
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "is_active": True,
            "created_at": "2026-04-16T00:00:00",
            "updated_at": "2026-04-16T00:00:00",
            "deleted_at": None,
        }
        self._next_id += 1
        self._users.append(user)
        return deepcopy(user)

    def get_user_by_email(self, email: str, include_inactive: bool = False) -> Optional[Dict[str, Any]]:
        for user in self._users:
            if user["email"] != email:
                continue
            if not include_inactive and (user["deleted_at"] is not None or user["is_active"] is not True):
                continue
            return deepcopy(user)
        return None

    def get_user_by_id(self, user_id: int, include_inactive: bool = False) -> Optional[Dict[str, Any]]:
        for user in self._users:
            if user["id"] != user_id:
                continue
            if not include_inactive and (user["deleted_at"] is not None or user["is_active"] is not True):
                continue
            return deepcopy(user)
        return None

    def list_users(self, limit: int = 100, offset: int = 0, include_inactive: bool = False) -> List[Dict[str, Any]]:
        result = []
        for user in self._users:
            if not include_inactive and (user["deleted_at"] is not None or user["is_active"] is not True):
                continue
            result.append(deepcopy(user))
        return result[offset : offset + limit]

    def update_user(
        self,
        user_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        password_hash: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        for user in self._users:
            if user["id"] != user_id or user["deleted_at"] is not None:
                continue
            if name is not None:
                user["name"] = name
            if email is not None:
                user["email"] = email
            if password_hash is not None:
                user["password_hash"] = password_hash
            if is_active is not None:
                user["is_active"] = is_active
            user["updated_at"] = "2026-04-16T01:00:00"
            return deepcopy(user)
        return None

    def soft_delete_user(self, user_id: int) -> bool:
        for user in self._users:
            if user["id"] != user_id or user["deleted_at"] is not None:
                continue
            user["is_active"] = False
            user["deleted_at"] = "2026-04-16T02:00:00"
            return True
        return False

    def hard_delete_user(self, user_id: int) -> bool:
        original_count = len(self._users)
        self._users = [user for user in self._users if user["id"] != user_id]
        return len(self._users) != original_count


class UserServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeUserRepository()
        self.service = UserService(user_repository=self.repo)

    def test_register_user_normalizes_email_and_hides_password_hash(self) -> None:
        user = self.service.register_user("William", "  WILLIAM@EMAIL.COM  ", "Senha123")

        self.assertEqual(user["email"], "william@email.com")
        self.assertEqual(user["name"], "William")
        self.assertNotIn("password_hash", user)

    def test_register_user_rejects_invalid_email(self) -> None:
        with self.assertRaisesRegex(ValueError, "Email inválido"):
            self.service.register_user("William", "email-invalido", "Senha123")

    def test_register_user_rejects_weak_password(self) -> None:
        with self.assertRaisesRegex(ValueError, "Senha inválida"):
            self.service.register_user("William", "william@email.com", "12345678")

    def test_register_user_rejects_duplicate_email(self) -> None:
        self.service.register_user("William", "william@email.com", "Senha123")

        with self.assertRaisesRegex(ValueError, "Email já cadastrado"):
            self.service.register_user("Outro", "william@email.com", "Senha123")

    def test_update_user_changes_name_and_email(self) -> None:
        created = self.service.register_user("William", "william@email.com", "Senha123")

        updated = self.service.update_user(created["id"], name="Will", email="will@email.com")

        self.assertEqual(updated["name"], "Will")
        self.assertEqual(updated["email"], "will@email.com")

    def test_deactivate_user_removes_user_from_active_listing(self) -> None:
        created = self.service.register_user("William", "william@email.com", "Senha123")

        self.service.deactivate_user(created["id"])
        active_users = self.service.list_users()

        self.assertEqual(active_users, [])


if __name__ == "__main__":
    unittest.main()
