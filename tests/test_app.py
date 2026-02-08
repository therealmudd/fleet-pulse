import pytest


user_credentials_cases = [
    (
        {"email": "admin@pulsefleet.com", "password": ""},
        {"message": "Successfully generated token"},
        200,
    ),
    (
        {"email": "admin@pulsefleet.com", "password": "wrong-password"},
        {"message": "Invalid credentials"},
        401,
    ),
    (
        {"email": "inactive@pulsefleet.com", "password": ""},
        {"message": "Inactive user"},
        403,
    ),
    (
        {"email": "unknown@pulsefleet.com", "password": ""},
        {"message": "Invalid credentials"},
        401,
    ),
    ({}, {"message": "Malformed request"}, 400),
]


@pytest.mark.parametrize("body, expected_json, expected_status", user_credentials_cases)
def test_login(client, body, expected_json, expected_status):
    response = client.post("/auth/login", json=body)

    assert response.json["message"] == expected_json["message"]
    assert response.status_code == expected_status
