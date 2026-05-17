import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app import create_app
from app.controllers.user_controller import UserController

BASE_URL = "http://127.0.0.1:5000"
_TEST_CLIENT = None


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


def init_local_client() -> None:
    global _TEST_CLIENT
    if _TEST_CLIENT is not None:
        return

    UserController._service = FakeRouteService()
    app = create_app()
    _TEST_CLIENT = app.test_client()


def request_json(method: str, path: str = "", data: dict | None = None) -> dict:
    try:
        url = f"{BASE_URL}{path}"
        headers = {"Content-Type": "application/json"}
        body = json.dumps(data).encode("utf-8") if data is not None else None
        request = Request(url, data=body, headers=headers, method=method)
        with urlopen(request) as response:
            response_text = response.read().decode("utf-8")
            if response_text:
                return {"status": response.status, "body": json.loads(response_text)}
            return {"status": response.status, "body": {}}
    except HTTPError as error:
        payload = error.read().decode("utf-8")
        try:
            body = json.loads(payload)
        except ValueError:
            body = {"error": payload}
        return {"status": error.code, "body": body}
    except URLError:
        init_local_client()
        response = _TEST_CLIENT.open(path or "/", method=method, json=data)
        return {"status": response.status_code, "body": response.get_json()}


def list_users(limit: int = 100, offset: int = 0) -> dict:
    return request_json("GET", f"/users/?limit={limit}&offset={offset}")


def create_user(name: str, email: str, password: str) -> dict:
    return request_json("POST", "/users/", {"name": name, "email": email, "password": password})


def get_user(user_id: int) -> dict:
    return request_json("GET", f"/users/{user_id}")


def update_user(user_id: int, name: str | None = None, email: str | None = None, password: str | None = None, is_active: bool | None = None) -> dict:
    payload = {}
    if name is not None:
        payload["name"] = name
    if email is not None:
        payload["email"] = email
    if password is not None:
        payload["password"] = password
    if is_active is not None:
        payload["is_active"] = is_active
    return request_json("PUT", f"/users/{user_id}", payload)


def delete_user(user_id: int) -> dict:
    return request_json("DELETE", f"/users/{user_id}")


def main() -> None:
    print("1) Listando usuários")
    print(list_users())

    print("\n2) Criando usuário")
    print(create_user("Ana", "ana@email.com", "Senha123"))

    print("\n3) Buscando usuário 1")
    print(get_user(1))

    print("\n4) Atualizando usuário 1")
    print(update_user(1, name="Ana Silva", email="ana.silva@email.com"))

    print("\n5) Desativando usuário 1")
    print(delete_user(1))

    print("\n6) Lista final")
    print(list_users())


if __name__ == "__main__":
    main()
