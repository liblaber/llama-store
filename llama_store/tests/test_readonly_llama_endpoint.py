"""
Integration tests for the Llama store API.
These tests test /llama endpoint is read only if the environment variable ALLOW_WRITE is not set

These tests assume a clean database. Run recreate-database.sh to clean up the database
"""

import pytest


class TestReadonlyLlamaEndpoints:
    """
    Test the llama endpoints are readonly if ALLOW_WRITE is not set. Tests in this fixture start at 1001.
    """

    @pytest.mark.order(1001)
    def test_get_all_llamas_with_an_api_token_returns_the_llamas(self):
        """
        Test that we can get all llamas with an API token
        """
        response = pytest.readonly_client.get("/llama", headers={"Authorization": f"Bearer {pytest.api_token}"})
        assert response.status_code == 200

    @pytest.mark.order(1001)
    def test_create_a_new_llama_with_an_api_key_fails_with_endpoint_not_found(self):
        """
        Test that we can cannot create a new llama in readonly mode
        """
        response = pytest.readonly_client.post(
            "/llama",
            json={"name": "Llamageddon", "age": 9, "color": "white", "rating": 4},
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        assert response.status_code == 405

    @pytest.mark.order(1001)
    def test_update_a_llama_with_an_api_key_fails_with_endpoint_not_found(self):
        """
        Test that we can cannot update a new llama in readonly mode
        """
        response = pytest.readonly_client.put(
            "/llama",
            json={"name": "Llamageddon", "age": 9, "color": "white", "rating": 4},
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        assert response.status_code == 405

    @pytest.mark.order(1001)
    def test_delete_a_llama_with_an_api_key_fails_with_endpoint_not_found(self):
        """
        Test that we can cannot delete a new llama in readonly mode
        """
        response = pytest.readonly_client.delete(
            "/llama",
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        assert response.status_code == 405
