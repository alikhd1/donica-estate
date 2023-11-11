from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_login_for_access_token():
    # Test with valid credentials
    response = client.post(
        "/token",
        data={"username": "ali", "password": "Alik@1234"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    # Test with invalid credentials
    response = client.post(
        "/token",
        data={"username": "invalid_user", "password": "invalid_password"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()
    assert response.json()["detail"] == "Incorrect username or password"
