from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.config.database import execute, fetch_all, fetch_one


class UserRepository:
    def create_user(self, name: str, email: str, password_hash: str) -> Dict[str, Any]:
        row = fetch_one(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING id, name, email, is_active, created_at, updated_at, deleted_at
            """,
            (name, email, password_hash),
        )
        if row is None:
            raise RuntimeError("Falha ao criar usuário")
        return row

    def get_user_by_id(self, user_id: int, include_inactive: bool = False) -> Optional[Dict[str, Any]]:
        if include_inactive:
            return fetch_one(
                """
                SELECT id, name, email, is_active, created_at, updated_at, deleted_at
                FROM users
                WHERE id = %s
                """,
                (user_id,),
            )
        return fetch_one(
            """
            SELECT id, name, email, is_active, created_at, updated_at, deleted_at
            FROM users
            WHERE id = %s AND deleted_at IS NULL AND is_active = TRUE
            """,
            (user_id,),
        )

    def get_user_by_email(self, email: str, include_inactive: bool = False) -> Optional[Dict[str, Any]]:
        if include_inactive:
            return fetch_one(
                """
                SELECT id, name, email, password_hash, is_active, created_at, updated_at, deleted_at
                FROM users
                WHERE email = %s
                """,
                (email,),
            )
        return fetch_one(
            """
            SELECT id, name, email, password_hash, is_active, created_at, updated_at, deleted_at
            FROM users
            WHERE email = %s AND deleted_at IS NULL AND is_active = TRUE
            """,
            (email,),
        )

    def list_users(self, limit: int = 100, offset: int = 0, include_inactive: bool = False) -> List[Dict[str, Any]]:
        if include_inactive:
            return fetch_all(
                """
                SELECT id, name, email, is_active, created_at, updated_at, deleted_at
                FROM users
                ORDER BY id ASC
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
        return fetch_all(
            """
            SELECT id, name, email, is_active, created_at, updated_at, deleted_at
            FROM users
            WHERE deleted_at IS NULL AND is_active = TRUE
            ORDER BY id ASC
            LIMIT %s OFFSET %s
            """,
            (limit, offset),
        )

    def update_user(
        self,
        user_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        password_hash: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        fields = []
        params = []

        if name is not None:
            fields.append("name = %s")
            params.append(name)
        if email is not None:
            fields.append("email = %s")
            params.append(email)
        if password_hash is not None:
            fields.append("password_hash = %s")
            params.append(password_hash)
        if is_active is not None:
            fields.append("is_active = %s")
            params.append(is_active)

        if not fields:
            return self.get_user_by_id(user_id, include_inactive=True)

        params.append(user_id)
        sql = f"""
            UPDATE users
            SET {", ".join(fields)}, updated_at = NOW()
            WHERE id = %s AND deleted_at IS NULL
            RETURNING id, name, email, is_active, created_at, updated_at, deleted_at
        """
        return fetch_one(sql, tuple(params))

    def soft_delete_user(self, user_id: int) -> bool:
        affected = execute(
            """
            UPDATE users
            SET is_active = FALSE, deleted_at = NOW(), updated_at = NOW()
            WHERE id = %s AND deleted_at IS NULL
            """,
            (user_id,),
        )
        return affected > 0

    def hard_delete_user(self, user_id: int) -> bool:
        affected = execute("DELETE FROM users WHERE id = %s", (user_id,))
        return affected > 0

