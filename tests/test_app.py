import pytest


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
