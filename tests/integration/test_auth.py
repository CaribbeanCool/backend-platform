def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "secret-password",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "test@example.com"
    assert data["is_active"] is True

    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client):
    payload = {
        "email": "duplicate@example.com",
        "password": "secret-password",
    }

    first = client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    second = client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert first.status_code == 201
    assert second.status_code == 409


def test_login_returns_access_token(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "password": "secret-password",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@example.com",
            "password": "secret-password",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
