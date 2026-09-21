def test_create_product_requires_auth(client):
    response = client.post(
        "/api/v1/products",
        json={
            "name": "Keyboard",
            "description": "Mechanical keyboard",
        },
    )

    assert response.status_code in (401, 403)


def create_authenticated_user(client):
    credentials = {
        "email": "product-user@example.com",
        "password": "secret-password",
    }

    client.post(
        "/api/v1/auth/register",
        json=credentials,
    )

    response = client.post(
        "/api/v1/auth/login",
        json=credentials,
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }


def test_authenticated_user_can_create_product(
    client,
):
    headers = create_authenticated_user(client)

    response = client.post(
        "/api/v1/products",
        headers=headers,
        json={
            "name": "Keyboard",
            "description": "Mechanical keyboard",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Keyboard"
    assert data["description"] == ("Mechanical keyboard")
