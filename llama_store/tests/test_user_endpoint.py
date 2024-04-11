"""
Integration tests for the Llama store API.
These tests test the /user and /token endpoints

These tests assume a clean database. Run recreate-database.sh to clean up the database
"""

import pytest


class TestUserEndpoints:
    """
    Test the user endpoints. Tests in this fixture start at 1.
    """

    @pytest.mark.order(1)
    def test_create_new_user(self):
        """
        Test that we can create a new user
        """
        response = pytest.client.post("/user", json={"email": "test_user@example.com", "password": "Password123!"})
        assert response.status_code == 201
        assert response.json() == {"email": "test_user@example.com", "id": 1}

    @pytest.mark.order(1)
    def test_create_user_that_already_exists_gives_an_error(self):
        """
        Test that we get an error if we try to create a user that already exists
        """
        response = pytest.client.post("/user", json={"email": "test_user@example.com", "password": "Password123!"})
        assert response.status_code == 400
        assert response.json() == {"detail": "User already registered"}

    @pytest.mark.order(1)
    def test_create_auth_token(self):
        """
        Test that we can create an auth token
        """
        response = pytest.client.post("/token", json={"email": "test_user@example.com", "password": "Password123!"})
        assert response.status_code == 201
        token_type = response.json()["tokenType"]
        pytest.api_token = response.json()["accessToken"]
        assert token_type == "bearer"
        assert pytest.api_token is not None

    @pytest.mark.order(1)
    def test_create_auth_token_fails_if_email_is_invalid(self):
        """
        Test that creating an auth token fails if the email is invalid
        """
        response = pytest.client.post("/token", json={"email": "wrong_user@example.com", "password": "Password123!"})
        assert response.status_code == 404

    @pytest.mark.order(1)
    def test_create_auth_token_fails_if_password_is_invalid(self):
        """
        Test that creating an auth token fails if the password is invalid
        """
        response = pytest.client.post("/token", json={"email": "test_user@example.com", "password": "WrongPassw0rd!"})
        assert response.status_code == 404

    @pytest.mark.order(1)
    def test_get_user_by_email_should_give_an_error_if_not_authenticated(self):
        """
        Test that we get an error if we try to get a user without an auth token
        """
        response = pytest.client.get("/user/test_user@example.com")
        assert response.status_code == 403

    @pytest.mark.order(1)
    def test_get_user_by_email_should_give_an_error_if_authentication_key_is_wrong(self):
        """
        Test that we get an error if we try to get a user without an auth token
        """
        response = pytest.client.get("/user/test_user@example.com", headers={"Authorization": "Bearer wrong_key"})
        assert response.status_code == 401

    @pytest.mark.order(1)
    def test_get_user_by_email_should_return_the_user_if_authenticated(self):
        """
        Test that we can get a user if we are authenticated
        """
        response = pytest.client.get(
            "/user/test_user@example.com", headers={"Authorization": f"Bearer {pytest.api_token}"}
        )
        assert response.status_code == 200
        assert response.json() == {"email": "test_user@example.com", "id": 1}

    @pytest.mark.order(1)
    def test_create_user_with_an_invalid_email_address_gives_a_validaton_error(self):
        """
        Test that we get an error if we try to create a user with an invalid email address
        """
        response = pytest.client.post("/user", json={"email": "test_userexample.com", "password": "Password123!"})
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "type": "string_pattern_mismatch",
                    "loc": ["body", "email"],
                    "msg": "String should match pattern " "'.+\\@.+\\..+'",
                    "input": "test_userexample.com",
                    "ctx": {"pattern": ".+\\@.+\\..+"},
                    "url": "https://errors.pydantic.dev/2.6/v/string_pattern_mismatch",
                }
            ]
        }

    @pytest.mark.order(1)
    def test_create_user_with_an_invalid_password_gives_a_validaton_error(self):
        """
        Test that we get an error if we try to create a user with an invalid password
        """
        response = pytest.client.post("/user", json={"email": "test_user@example.com", "password": "Password123"})
        assert response.status_code == 422
        print(response.json())
        assert response.json() == {
            "detail": [
                {
                    "type": "assertion_error",
                    "loc": ["body", "password"],
                    "msg": "Assertion failed, Password must be at least 8 characters long, "
                    "and contain at least one letter, one number, and one special character",
                    "input": "Password123",
                    "ctx": {"error": {}},
                    "url": "https://errors.pydantic.dev/2.6/v/assertion_error",
                }
            ]
        }
