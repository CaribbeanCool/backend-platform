from app.security import hash_password, verify_password


def test_hash_password_does_not_store_plaintext():
    password = "super-secret-password"

    hashed = hash_password(password)

    assert hashed != password


def test_verify_password_accepts_correct_password():
    password = "super-secret-password"

    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_rejects_wrong_password():
    hashed = hash_password("correct-password")

    assert (
        verify_password(
            "wrong-password",
            hashed,
        )
        is False
    )
