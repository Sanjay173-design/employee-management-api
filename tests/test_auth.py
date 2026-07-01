from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_login_invalid_user(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "fake@test.com",
            "password": "wrong"
        }
    )

    assert response.status_code == 401