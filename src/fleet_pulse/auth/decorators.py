from functools import wraps
from flask import request, g, jsonify
from .jwt_token import verify_jwt, JWTInvalidTokenError, JWTExpiredTokenError
from ..models.user import UserRole


def requires_roles(roles: list[UserRole]):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if auth_header is None:
                return jsonify({"message": "Missing Authorization header"}), 401

            try:
                _, token = auth_header.split()
                payload = verify_jwt(token)
                g.user_id = payload["sub"]
                g.user_role = payload["role"]
                user_role = UserRole(payload["role"])
            except (KeyError, ValueError, JWTInvalidTokenError):
                return jsonify({"message": "Invalid token"}), 401
            except JWTExpiredTokenError:
                return jsonify({"message": "Token expired"}), 401

            if user_role in roles:
                return func(*args, **kwargs)
            else:
                return jsonify({"message": "Unauthorized user"}), 401

        return wrapped

    return decorator
