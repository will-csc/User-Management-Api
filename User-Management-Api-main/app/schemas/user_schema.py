from __future__ import annotations

from typing import Any, Dict


def user_public(user: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in user.items() if k != "password_hash"}

