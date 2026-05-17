from __future__ import annotations

import os
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence
from urllib.parse import quote_plus

try:
    import psycopg
    from psycopg.rows import dict_row

    _DRIVER = "psycopg"
except Exception:
    psycopg = None
    dict_row = None
    _DRIVER = "psycopg2"

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except Exception:
    psycopg2 = None
    RealDictCursor = None


def _load_dotenv(env_path: Path) -> None:
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_load_dotenv(_PROJECT_ROOT / ".env")


@dataclass(frozen=True, slots=True)
class Settings:
    environment: str
    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str
    secret_key: str
    access_token_expires_in_seconds: int

    @property
    def database_url(self) -> str:
        user = quote_plus(self.database_user)
        password = quote_plus(self.database_password)
        return f"postgresql://{user}:{password}@{self.database_host}:{self.database_port}/{self.database_name}"


_SETTINGS: Optional[Settings] = None


def get_settings() -> Settings:
    global _SETTINGS
    if _SETTINGS is not None:
        return _SETTINGS

    def _env(name: str, default: Optional[str] = None) -> str:
        value = os.getenv(name, default)
        if value is None or value == "":
            raise RuntimeError(f"Variável de ambiente obrigatória não definida: {name}")
        return value

    _SETTINGS = Settings(
        environment=os.getenv("ENVIRONMENT", "development"),
        database_host=os.getenv("DB_HOST", "localhost"),
        database_port=int(os.getenv("DB_PORT", "5432")),
        database_name=_env("DB_NAME", "user_management"),
        database_user=_env("DB_USER", "postgres"),
        database_password=_env("DB_PASSWORD", "postgres"),
        secret_key=_env("SECRET_KEY", "change-me"),
        access_token_expires_in_seconds=int(os.getenv("ACCESS_TOKEN_EXPIRES_IN", "3600")),
    )
    return _SETTINGS


def _ensure_driver_available() -> None:
    if _DRIVER == "psycopg":
        if psycopg is None:
            raise RuntimeError("Driver psycopg não está disponível")
        return
    if psycopg2 is None:
        raise RuntimeError("Instale um driver PostgreSQL: psycopg (v3) ou psycopg2")


def connect():
    _ensure_driver_available()
    settings = get_settings()
    if _DRIVER == "psycopg":
        return psycopg.connect(  # type: ignore[union-attr]
            settings.database_url,
            autocommit=False,
            row_factory=dict_row,
        )
    return psycopg2.connect(  # type: ignore[union-attr]
        settings.database_url,
        cursor_factory=RealDictCursor,
    )


@contextmanager
def get_connection():
    conn = connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def fetch_one(query: str, params: Optional[Sequence[Any]] = None) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            row = cur.fetchone()
            if row is None:
                return None
            return dict(row)


def fetch_all(query: str, params: Optional[Sequence[Any]] = None) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            rows = cur.fetchall()
            return [dict(r) for r in rows]


def execute(query: str, params: Optional[Sequence[Any]] = None) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.rowcount


def init_db(schema_path: Optional[Path] = None) -> None:
    if schema_path is None:
        schema_path = _PROJECT_ROOT / "docs" / "schema.sql"

    sql = schema_path.read_text(encoding="utf-8")
    statements = [s.strip() for s in sql.split(";") if s.strip()]
    with get_connection() as conn:
        with conn.cursor() as cur:
            for stmt in statements:
                cur.execute(stmt)

