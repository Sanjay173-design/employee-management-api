def test_get_employees_authenticated(client):

    signup_response = client.post(
        "/auth/signup",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "password123",
            "role": "admin"
        }
    )

    print("\nSIGNUP STATUS:", signup_response.status_code)
    print("SIGNUP BODY:", signup_response.text)

    login_response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "password123"
        }
    )

    print("\nLOGIN STATUS:", login_response.status_code)
    print("LOGIN BODY:", login_response.text)

    assert login_response.status_code == 200