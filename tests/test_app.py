import pytest
from datetime import datetime, timedelta, timezone
from fleet_pulse.auth.jwt_token import jwt_encode
from fleet_pulse.models.user import UserRole


TOKEN_EXPIRATION_TIME = int(
    (datetime.now(tz=timezone.utc) + timedelta(hours=1)).timestamp()
)


def prep_creds(email_prefix: str, password: str) -> dict[str, str]:
    return {"email": f"{email_prefix}@fleetpulse.com", "password": password}


def prep_response(message: str, status: int) -> tuple[dict[str, str], int]:
    return {"message": message}, status


@pytest.mark.parametrize(
    "email_prefix, password, expected_message, expected_status",
    [
        ("admin", "", "Successfully generated token", 200),
        ("admin", "wrong-password", "Invalid credentials", 401),
        ("inactive", "", "Inactive user", 403),
        ("unknown", "", "Invalid credentials", 401),
        ("admin", None, "Malformed request", 400),
    ],
)
def test_login(client, email_prefix, password, expected_message, expected_status):
    body = prep_creds(email_prefix, password)
    expected_json, expected_status = prep_response(expected_message, expected_status)

    response = client.post("/auth/login", json=body)

    assert response.json["message"] == expected_json["message"]
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "payload, expected_message, expected_status",
    [
        (
            {"sub": "user-id", "role": UserRole.ADMIN.value, "exp": -1},
            "Token expired",
            401,
        ),
        (
            {
                "sub": "user-id",
                "role": UserRole.ADMIN.value,
                "exp": TOKEN_EXPIRATION_TIME,
            },
            "Success!",
            200,
        ),
        (
            {
                "sub": "user-id",
                "role": UserRole.DRIVER.value,
                "exp": TOKEN_EXPIRATION_TIME,
            },
            "Unauthorized user",
            401,
        ),
        ({"sub": None, "role": None, "exp": 0}, "Invalid token", 401),
    ],
)
def test_verify_jwt(client, payload, expected_message, expected_status):
    payload["iat"] = 0
    token = jwt_encode(payload) if payload["sub"] is not None else "some-invalid-token"

    response = client.get("/admin/health", headers={"Authorization": f"Bearer {token}"})

    assert response.json["message"] == expected_message
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "email_prefix, password, expected_message, expected_status",
    [
        ("admin", "", "Success!", 200),
        ("dispatcher", "", "Unauthorized user", 401),
        ("driver", "", "Unauthorized user", 401),
    ],
)
def test_admin_health(
    client, email_prefix, password, expected_message, expected_status
):
    body = prep_creds(email_prefix, password)
    response = client.post("/auth/login", json=body)
    token = response.json.get("token")

    response = client.get("/admin/health", headers={"Authorization": f"Bearer {token}"})

    assert response.json["message"] == expected_message
    assert response.status_code == expected_status
