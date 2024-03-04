from fastapi import Header

from . import jwt
from .exceptions import AccessDenied


def ensure_current_user(x_jwt_payload: str = Header(...)):
    payload = jwt.decode_payload(x_jwt_payload)

    if not payload:
        raise AccessDenied("Access denied")

    return payload
