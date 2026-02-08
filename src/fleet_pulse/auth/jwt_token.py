import os
import dotenv
import base64
import json
import hmac
import hashlib
from datetime import datetime, timezone

dotenv.load_dotenv()
SECRET_KEY = os.getenv("AUTH_SECRET_KEY").encode("utf-8")


class JWTInvalidTokenError(Exception):
    pass

class JWTExpiredTokenError(Exception):
    pass

def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def base64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def jwt_encode(payload: dict[str, str]):
    header = {"alg": "HS256", "typ": "JWT"}

    header_json = json.dumps(header, separators=(",", ":")).encode("utf-8")
    payload_json = json.dumps(payload, separators=(",", ":")).encode("utf-8")

    header_b64 = base64url_encode(header_json)
    payload_b64 = base64url_encode(payload_json)

    message = f"{header_b64}.{payload_b64}"

    signature = hmac.new(SECRET_KEY, message.encode("utf-8"), hashlib.sha256).digest()
    signature_b64 = base64url_encode(signature)

    jwt_token = f"{message}.{signature_b64}"

    return jwt_token


def verify_jwt(token: str) -> dict:
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError:
        raise JWTInvalidTokenError("Invalid token")

    message = f"{header_b64}.{payload_b64}"

    expected_signature = hmac.new(
        SECRET_KEY, message.encode("utf-8"), hashlib.sha256
    ).digest()

    if not hmac.compare_digest(base64url_encode(expected_signature), signature_b64):
        raise JWTInvalidTokenError("Invalid signature")

    payload_json = base64url_decode(payload_b64)
    payload = json.loads(payload_json)

    now = int(datetime.now(tz=timezone.utc).timestamp())
    if payload.get("exp") and now > payload["exp"]:
        raise JWTExpiredTokenError("Token expired")

    return payload
