"""
Integration tests for the Llama store API.
These tests test the /llama endpoint

These tests assume a clean database. Run recreate-database.sh to clean up the database.
They also assume that the User integration tests have been run, so that there is a
valid user and API token.
"""

import pytest

from db_migrations.versions.first import ALL_LLAMAS


def all_llamas():
    """
    Converts the ALL_LLAMAS array into the right casing for
    external API calls as llama_id is llamaId in JSON
    """
    new_llamas = []
    for llama in ALL_LLAMAS:
        new_llamas.append(
            {
                "llamaId": llama["llama_id"],
                "name": llama["name"],
                "age": llama["age"],
                "color": llama["color"],
                "rating": llama["rating"],
            }
        )
    return new_llamas


class TestLlamaEndpoints:
    """
    Test the llama endpoints. Tests in this fixture start at 101.
    """

    @pytest.mark.order(101)
    def test_get_all_llamas_without_an_api_token_gives_an_error(self):
        """
        Test that we get an error if we try to get all llamas without an API token
        """
        response = pytest.client.get("/llama")
        assert response.status_code == 403

    @pytest.mark.order(101)
    def test_get_all_llamas_with_an_api_token_returns_the_llamas(self):
        """
        Test that we can get all llamas with an API token
        """
        response = pytest.client.get("/llama", headers={"Authorization": f"Bearer {pytest.api_token}"})
        assert response.status_code == 200
        assert response.json() == all_llamas()

    @pytest.mark.order(101)
    def test_get_llama_by_id_without_an_api_token_gives_an_error(self):
        """
        Test that we get an error if we try to get a llama by ID without an API token
        """
        response = pytest.client.get("/llama/1")
        assert response.status_code == 403

    @pytest.mark.order(101)
    @pytest.mark.parametrize("llama_id", [1, 2, 3, 4, 5, 6])
    def test_get_llama_by_id_with_an_api_token_returns_the_llama(self, llama_id: int):
        """
        Test that we can get a llama by ID with an API token
        """
        response = pytest.client.get(f"/llama/{llama_id}", headers={"Authorization": f"Bearer {pytest.api_token}"})
        assert response.status_code == 200
        assert response.json() == all_llamas()[llama_id - 1]

    @pytest.mark.order(101)
    def test_create_a_new_llama_without_an_api_key_fails(self):
        """
        Test that we get an error if we try to create a llama without an API key
        """
        response = pytest.client.post("/llama", json={"name": "Llamageddon", "age": 9, "color": "white", "rating": 4})
        assert response.status_code == 403

    @pytest.mark.order(101)
    def test_create_a_new_llama_with_an_api_key_returns_the_new_llama_with_an_id(self):
        """
        Test that we can create a new llama with an API key and it returns the new llama with an ID set.
        """
        response = pytest.client.post(
            "/llama",
            json={"name": "Llamageddon", "age": 9, "color": "white", "rating": 4},
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )
        assert response.status_code == 201
        assert response.json() == {"llamaId": 7, "name": "Llamageddon", "age": 9, "color": "white", "rating": 4}

    @pytest.mark.order(101)
    def test_create_a_new_llama_with_an_api_key_and_no_name_gives_an_error(self):
        """
        Test that we get an error if we try to create a llama with an API key and no name
        """
        response = pytest.client.post(
            "/llama",
            json={"age": 9, "color": "white", "rating": 4},
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "name"],
                    "msg": "Field required",
                    "input": {"age": 9, "color": "white", "rating": 4},
                    "url": "https://errors.pydantic.dev/2.6/v/missing",
                }
            ]
        }

    @pytest.mark.order(101)
    def test_create_a_new_llama_with_an_api_key_and_no_age_gives_an_error(self):
        """
        Test that we get an error if we try to create a llama with an API key and no age
        """
        response = pytest.client.post(
            "/llama",
            json={"name": "Llamageddon", "color": "white", "rating": 4},
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "age"],
                    "msg": "Field required",
                    "input": {"name": "Llamageddon", "color": "white", "rating": 4},
                    "url": "https://errors.pydantic.dev/2.6/v/missing",
                }
            ]
        }

    @pytest.mark.order(101)
    def test_create_a_new_llama_with_an_api_key_and_no_color_gives_an_error(self):
        """
        Test that we get an error if we try to create a llama with an API key and no color
        """
        response = pytest.client.post(
            "/llama",
            json={"name": "Llamageddon", "age": 9, "rating": 4},
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "color"],
                    "msg": "Field required",
                    "input": {"name": "Llamageddon", "age": 9, "rating": 4},
                    "url": "https://errors.pydantic.dev/2.6/v/missing",
                }
            ]
        }

    @pytest.mark.order(101)
    def test_create_a_new_llama_with_an_api_key_and_no_rating_gives_an_error(self):
        """
        Test that we get an error if we try to create a llama with an API key and no rating
        """
        response = pytest.client.post(
            "/llama",
            json={"name": "Llamageddon", "age": 9, "color": "white"},
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "rating"],
                    "msg": "Field required",
                    "input": {"name": "Llamageddon", "age": 9, "color": "white"},
                    "url": "https://errors.pydantic.dev/2.6/v/missing",
                }
            ]
        }

    @pytest.mark.order(101)
    def test_create_a_new_llama_with_an_api_key_and_and_invalid_color_gives_an_error(self):
        """
        Test that we get an error if we try to create a llama with an API key and an invalid color
        """
        response = pytest.client.post(
            "/llama",
            json={"name": "Llamageddon", "age": 9, "rating": 4, "color": "pink"},
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "type": "enum",
                    "loc": ["body", "color"],
                    "msg": "Input should be 'brown', 'white', 'black' or 'gray'",
                    "input": "pink",
                    "ctx": {"expected": "'brown', 'white', 'black' or 'gray'"},
                }
            ]
        }

    @pytest.mark.order(101)
    def test_create_a_new_llama_with_an_api_key_and_an_existing_name_returns_a_conflict(self):
        """
        Test that we get an error if we create a new llama with an API key and a name
        that already exists
        """
        response = pytest.client.post(
            "/llama",
            json={"name": "Llamageddon", "age": 9, "color": "white", "rating": 4},
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )
        assert response.status_code == 409
        assert response.json() == {"detail": "Llama named Llamageddon already exists"}

    @pytest.mark.order(101)
    def test_create_a_new_llama_with_an_api_key_and_get_that_llama_returns_the_llama(self):
        """
        Test that we can create a new llama with an API key and get that llama
        """
        response = pytest.client.post(
            "/llama",
            json={"name": "LlamaLlama Duck", "age": 10, "color": "black", "rating": 4},
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        llama_id = response.json()["llamaId"]
        response = pytest.client.get(f"/llama/{llama_id}", headers={"Authorization": f"Bearer {pytest.api_token}"})

        assert response.status_code == 200
        assert response.json()["name"] == "LlamaLlama Duck"
        assert response.json()["age"] == 10
        assert response.json()["color"] == "black"
        assert response.json()["rating"] == 4

    @pytest.mark.order(101)
    def test_update_llama_with_api_key_updates_the_llama(self):
        """
        Test if we update a llama without an API key it fails
        """
        response = pytest.client.post(
            "/llama",
            json={"name": "Dali Llama", "age": 10, "color": "black", "rating": 4},
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        llama_id = response.json()["llamaId"]
        response = pytest.client.put(
            f"/llama/{llama_id}",
            json={"name": "Dali Llama", "age": 12, "color": "black", "rating": 4},
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        assert response.status_code == 200

        response = pytest.client.get(f"/llama/{llama_id}", headers={"Authorization": f"Bearer {pytest.api_token}"})

        assert response.json()["name"] == "Dali Llama"
        assert response.json()["age"] == 12
        assert response.json()["color"] == "black"
        assert response.json()["rating"] == 4

    @pytest.mark.order(101)
    def test_update_llama_without_api_key_fails(self):
        """
        Test we can update a llama
        """
        response = pytest.client.post(
            "/llama",
            json={"name": "Bllama Llama", "age": 10, "color": "black", "rating": 4},
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        llama_id = response.json()["llamaId"]
        response = pytest.client.put(
            f"/llama/{llama_id}", json={"name": "Bllama Llama", "age": 12, "color": "black", "rating": 4}
        )

        assert response.status_code == 403

    @pytest.mark.order(101)
    def test_delete_llama_with_api_key_deletes(self):
        """
        Test we can delete a llama
        """
        response = pytest.client.post(
            "/llama",
            json={"name": "ByeBye Llama", "age": 10, "color": "black", "rating": 4},
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        llama_id = response.json()["llamaId"]
        response = pytest.client.delete(f"/llama/{llama_id}", headers={"Authorization": f"Bearer {pytest.api_token}"})

        assert response.status_code == 204

        response = pytest.client.get(f"/llama/{llama_id}", headers={"Authorization": f"Bearer {pytest.api_token}"})

        assert response.status_code == 404

    @pytest.mark.order(101)
    def test_delete_llama_without_api_key_fails(self):
        """
        Test if we delete a llama without an API key it fails
        """
        response = pytest.client.post(
            "/llama",
            json={"name": "Pull My Llama", "age": 10, "color": "black", "rating": 4},
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        llama_id = response.json()["llamaId"]
        response = pytest.client.delete(f"/llama/{llama_id}")

        assert response.status_code == 403
