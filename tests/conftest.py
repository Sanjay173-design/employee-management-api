import os
import pytest

os.environ["TESTING"] = "True"

from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():

    with TestClient(app) as client:
        yield client

@pytest.fixture
def auth_token(client):

    email = "fixture@example.com"
    password = "password123"

    client.post(
        "/auth/signup",
        json={
            "name": "Fixture User",
            "email": email,
            "password": password,
            "role": "user"
        }
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    token = login_response.json()[
        "access_token"
    ]

    return token        