def test_get_employees(
    client,
    auth_token
):

    response = client.get(
        "/employees/",
        headers={
            "Authorization":
            f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 200