from functools import wraps
from flask import request, jsonify
from .jwt_token import verify_jwt
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
                request.user_id = payload["sub"]
                request.user_role = payload["role"]
                user_role = UserRole(payload["role"])
            except KeyError:
                return jsonify({"message": "Invalid token"}), 403

            if user_role in roles:
                return func(*args, **kwargs)
            else:
                return jsonify({"Message": "Unauthorized user"}), 403

        return wrapped

    return decorator
