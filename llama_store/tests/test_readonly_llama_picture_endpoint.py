"""
Integration tests for the Llama store API.
These tests test /llama/{llama_id}/picture endpoint is read only if the environment variable ALLOW_WRITE is not set

These tests assume a clean database. Run recreate_database.sh to clean up the database
"""
import pytest


class TestReadonlyLlamaPictureEndpoints:
    """
    Test the  /llama/{llama_id}/picture endpoints are readonly if ALLOW_WRITE is not set.
    Tests in this fixture start at 2001.
    """

    @pytest.mark.order(2001)
    def test_get_all_llamas_with_an_api_token_returns_the_llamas(self):
        """
        Test that we can get a llama picture with an API token
        """
        response = pytest.readonly_client.get(
            "/llama/1/picture", headers={"Authorization": f"Bearer {pytest.api_token}"}
        )
        assert response.status_code == 200

    @pytest.mark.order(2001)
    def test_create_a_new_llama_with_an_api_key_fails_with_endpoint_not_found(self):
        """
        Test that we can cannot create a new llama in readonly mode
        """
        response = pytest.readonly_client.post(
            "/llama/1/picture",
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        assert response.status_code == 405

    @pytest.mark.order(2001)
    def test_update_a_llama_with_an_api_key_fails_with_endpoint_not_found(self):
        """
        Test that we can cannot update a new llama in readonly mode
        """
        response = pytest.readonly_client.put(
            "/llama/1/picture",
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        assert response.status_code == 405

    @pytest.mark.order(2001)
    def test_delete_a_llama_with_an_api_key_fails_with_endpoint_not_found(self):
        """
        Test that we can cannot delete a new llama in readonly mode
        """
        response = pytest.readonly_client.delete(
            "/llama/1/picture",
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        assert response.status_code == 405
