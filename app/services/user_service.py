from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import user_public
from app.utils.security import create_access_token, hash_password, verify_password
from app.utils.validators import is_valid_email, is_valid_password, normalize_email, required_str


class UserService:
    def __init__(self, user_repository: Optional[UserRepository] = None) -> None:
        self._repo = user_repository or UserRepository()

    def register_user(self, name: str, email: str, password: str) -> Dict[str, Any]:
        name = required_str(name, "Nome")
        email = normalize_email(email)
        if not is_valid_email(email):
            raise ValueError("Email inválido")
        if not is_valid_password(password):
            raise ValueError("Senha inválida")

        existing = self._repo.get_user_by_email(email, include_inactive=True)
        if existing is not None and existing.get("deleted_at") is None:
            raise ValueError("Email já cadastrado")

        password_hash_value = hash_password(password)
        user = self._repo.create_user(name=name, email=email, password_hash=password_hash_value)
        return user_public(user)

    def authenticate_user(self, email: str, password: str) -> Tuple[str, Dict[str, Any]]:
        email = normalize_email(email)
        user = self._repo.get_user_by_email(email, include_inactive=True)
        if not user:
            raise ValueError("Credenciais inválidas")
        if user.get("deleted_at") is not None or user.get("is_active") is not True:
            raise ValueError("Credenciais inválidas")
        if not verify_password(password, user.get("password_hash") or ""):
            raise ValueError("Credenciais inválidas")

        token = create_access_token(str(user["id"]), email=user["email"])
        return token, user_public(user)

    def list_users(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        limit = max(1, min(int(limit), 500))
        offset = max(0, int(offset))
        return self._repo.list_users(limit=limit, offset=offset, include_inactive=False)

    def get_user(self, user_id: int) -> Dict[str, Any]:
        user = self._repo.get_user_by_id(int(user_id), include_inactive=False)
        if user is None:
            raise ValueError("Usuário não encontrado")
        return user_public(user)

    def update_user(
        self,
        user_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> Dict[str, Any]:
        updates: Dict[str, Any] = {}

        if name is not None:
            name = name.strip()
            if not name:
                raise ValueError("Nome inválido")
            updates["name"] = name

        if email is not None:
            email = normalize_email(email)
            if not is_valid_email(email):
                raise ValueError("Email inválido")
            existing = self._repo.get_user_by_email(email, include_inactive=True)
            if existing is not None and int(existing["id"]) != int(user_id) and existing.get("deleted_at") is None:
                raise ValueError("Email já cadastrado")
            updates["email"] = email

        if password is not None:
            if not is_valid_password(password):
                raise ValueError("Senha inválida")
            updates["password_hash"] = hash_password(password)

        if is_active is not None:
            updates["is_active"] = bool(is_active)

        user = self._repo.update_user(user_id=int(user_id), **updates)
        if user is None:
            raise ValueError("Usuário não encontrado")
        return user_public(user)

    def deactivate_user(self, user_id: int) -> None:
        ok = self._repo.soft_delete_user(int(user_id))
        if not ok:
            raise ValueError("Usuário não encontrado")

    def delete_user(self, user_id: int) -> None:
        ok = self._repo.hard_delete_user(int(user_id))
        if not ok:
            raise ValueError("Usuário não encontrado")

