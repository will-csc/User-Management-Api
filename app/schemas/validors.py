from __future__ import annotations

import re


EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def required_str(value: object, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} inválido")

    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} inválido")
    return normalized


def normalize_email(email: object) -> str:
    return required_str(email, "Email").lower()


def is_valid_email(email: object) -> bool:
    if not isinstance(email, str):
        return False
    return bool(EMAIL_PATTERN.fullmatch(email.strip()))


def is_valid_password(password: object) -> bool:
    if not isinstance(password, str):
        return False
    if len(password) < 8:
        return False

    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    return has_upper and has_lower and has_digit
