"""
Integration tests for the Llama store API.
These tests test the /llama/{llama_id}/picture endpoint

These tests assume a clean database. Run recreate-database.sh to clean up the database.
They also assume that the User integration tests have been run, so that there is a
valid user and API token.
"""

from io import BytesIO
import pytest


def compare_bytes_to_file(content: bytes, filename: str) -> bool:
    """
    Compare raw bytes with a file

    This is used to test what we get from the endpoint matches what we expect
    """
    bufsize = 1024
    content_reader = BytesIO(content)
    with open(filename, "rb") as file:
        while True:
            content_bytes = content_reader.read(bufsize)
            file_bytes = file.read(bufsize)
            if content_bytes != file_bytes:
                return False
            if not content_bytes:
                return True


class TestLlamaPictureEndpoints:
    """
    Test the llama picture endpoints. Tests in this fixture start at 201.
    """

    @pytest.mark.order(201)
    def test_get_a_llama_picture_without_an_api_token_gives_an_error(self):
        """
        Test that we get an error if we try to get a llama picture without an API token
        """
        response = pytest.client.get("/llama/1/picture")
        assert response.status_code == 403

    @pytest.mark.order(201)
    @pytest.mark.parametrize("llama_id", [1, 2, 3, 4, 5, 6])
    def test_get_a_llama_picture_with_an_api_token_returns_the_picture(self, llama_id: int):
        """
        Test that we get a picture if we get a llama picture with an API token
        """
        response = pytest.client.get(
            f"/llama/{llama_id}/picture", headers={"Authorization": f"Bearer {pytest.api_token}"}
        )
        assert response.status_code == 200

        body = response.content

        # Compare the content with the known file
        assert compare_bytes_to_file(body, f"./db_migrations/llama_pictures/{llama_id}.png")

    @pytest.mark.order(201)
    def test_get_a_llama_picture_with_an_api_for_a_llama_that_doesnt_exist_returns_a_404(self):
        """
        Test that we get a picture if we get a llama picture with an API token
        """
        response = pytest.client.get("/llama/100/picture", headers={"Authorization": f"Bearer {pytest.api_token}"})
        assert response.status_code == 404

    @pytest.mark.order(201)
    def test_creating_llama_picture_without_an_api_token_gives_an_error(self):
        """
        Test that we get an error if we try to create a llama picture without an API token
        """
        response = pytest.client.post("/llama/1/picture")
        assert response.status_code == 403

    @pytest.mark.order(201)
    def test_creating_llama_picture_with_an_api_token_sets_the_picture(self):
        """
        Test that we can set a llama picture
        """
        # Create a new llama
        response = pytest.client.post(
            "/llama",
            json={
                "name": "Picture Llama 1",
                "age": 5,
                "color": "brown",
                "rating": 4,
            },
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        # Get the ID
        llama_id = response.json()["id"]

        # load the bytes for the picture
        with open("./tests/test_images/test_llama_1.png", "rb") as file:
            picture_bytes = file.read()

        response = pytest.client.post(
            f"/llama/{llama_id}/picture",
            content=picture_bytes,
            headers={
                "Authorization": f"Bearer {pytest.api_token}",
            },
        )
        assert response.status_code == 201

        # Verify what we set is what we get
        response = pytest.client.get(
            f"/llama/{llama_id}/picture", headers={"Authorization": f"Bearer {pytest.api_token}"}
        )
        assert response.status_code == 200

        body = response.content

        # Compare the content with the known file
        assert compare_bytes_to_file(body, "./tests/test_images/test_llama_1.png")

    @pytest.mark.order(201)
    def test_creating_llama_picture_with_an_api_token_using_a_jpg_converts_to_a_png(self):
        """
        Test that we can set a llama picture as a jpeg and get a png
        """
        # Create a new llama
        response = pytest.client.post(
            "/llama",
            json={
                "name": "Picture Llama 2",
                "age": 5,
                "color": "brown",
                "rating": 4,
            },
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        # Get the ID
        llama_id = response.json()["id"]

        # load the bytes for the picture
        with open("./tests/test_images/test_llama_2.jpeg", "rb") as file:
            picture_bytes = file.read()

        response = pytest.client.post(
            f"/llama/{llama_id}/picture",
            content=picture_bytes,
            headers={
                "Authorization": f"Bearer {pytest.api_token}",
            },
        )
        assert response.status_code == 201

        # Verify what we set is what we get
        response = pytest.client.get(
            f"/llama/{llama_id}/picture", headers={"Authorization": f"Bearer {pytest.api_token}"}
        )
        assert response.status_code == 200

        body = response.content

        # Compare the content with the known file
        assert compare_bytes_to_file(body, "./tests/test_images/test_llama_2_converted.png")

    @pytest.mark.order(201)
    def test_updating_a_llama_picture_with_an_api_token_updates_the_picture(self):
        """
        Test that we can update a llama picture
        """
        # Create a new llama
        response = pytest.client.post(
            "/llama",
            json={
                "name": "Picture Llama 3",
                "age": 5,
                "color": "brown",
                "rating": 4,
            },
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        # Get the ID
        llama_id = response.json()["id"]

        # load the bytes for the picture
        with open("./tests/test_images/test_llama_1.png", "rb") as file:
            picture_bytes = file.read()

        response = pytest.client.post(
            f"/llama/{llama_id}/picture",
            content=picture_bytes,
            headers={
                "Authorization": f"Bearer {pytest.api_token}",
            },
        )
        assert response.status_code == 201

        # Update to another llama picture
        with open("./tests/test_images/test_llama_3.png", "rb") as file:
            picture_bytes = file.read()

        response = pytest.client.put(
            f"/llama/{llama_id}/picture",
            content=picture_bytes,
            headers={
                "Authorization": f"Bearer {pytest.api_token}",
            },
        )
        assert response.status_code == 200

        # Verify what we set is what we get
        response = pytest.client.get(
            f"/llama/{llama_id}/picture", headers={"Authorization": f"Bearer {pytest.api_token}"}
        )
        assert response.status_code == 200

        body = response.content

        # Compare the content with the known file
        assert compare_bytes_to_file(body, "./tests/test_images/test_llama_3.png")

    @pytest.mark.order(201)
    def test_updating_a_llama_picture_without_an_api_token_gives_an_error(self):
        """
        Test that we can't update a llama picture without an API token
        """
        # Create a new llama
        response = pytest.client.post(
            "/llama",
            json={
                "name": "Picture Llama 4",
                "age": 5,
                "color": "brown",
                "rating": 4,
            },
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        # Get the ID
        llama_id = response.json()["id"]

        # load the bytes for the picture
        with open("./tests/test_images/test_llama_1.png", "rb") as file:
            picture_bytes = file.read()

        response = pytest.client.post(
            f"/llama/{llama_id}/picture",
            content=picture_bytes,
            headers={
                "Authorization": f"Bearer {pytest.api_token}",
            },
        )
        assert response.status_code == 201

        # Update to another llama picture
        with open("./tests/test_images/test_llama_3.png", "rb") as file:
            picture_bytes = file.read()

        response = pytest.client.put(f"/llama/{llama_id}/picture", content=picture_bytes)
        assert response.status_code == 403

        # Verify what we set is what we get
        response = pytest.client.get(
            f"/llama/{llama_id}/picture", headers={"Authorization": f"Bearer {pytest.api_token}"}
        )
        assert response.status_code == 200

        body = response.content

        # Compare the content with the origina; file
        assert compare_bytes_to_file(body, "./tests/test_images/test_llama_1.png")

    @pytest.mark.order(201)
    def test_deleting_a_llama_picture_with_an_api_token_deletes_the_picture(self):
        """
        Test that we can delete a llama picture
        """
        # Create a new llama
        response = pytest.client.post(
            "/llama",
            json={
                "name": "Picture Llama 5",
                "age": 5,
                "color": "brown",
                "rating": 4,
            },
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        # Get the ID
        llama_id = response.json()["id"]

        # load the bytes for the picture
        with open("./tests/test_images/test_llama_1.png", "rb") as file:
            picture_bytes = file.read()

        response = pytest.client.post(
            f"/llama/{llama_id}/picture",
            content=picture_bytes,
            headers={
                "Authorization": f"Bearer {pytest.api_token}",
            },
        )
        assert response.status_code == 201

        # delete the llama picture
        response = pytest.client.delete(
            f"/llama/{llama_id}/picture",
            headers={
                "Authorization": f"Bearer {pytest.api_token}",
            },
        )

        assert response.status_code == 204

        # Verify it's no longer found
        response = pytest.client.get(
            f"/llama/{llama_id}/picture", headers={"Authorization": f"Bearer {pytest.api_token}"}
        )

        assert response.status_code == 404

    @pytest.mark.order(201)
    def test_deleting_a_llama_picture_without_an_api_token_gives_an_error(self):
        """
        Test that we can't delete a llama picture without an API token
        """
        # Create a new llama
        response = pytest.client.post(
            "/llama",
            json={
                "name": "Picture Llama 6",
                "age": 5,
                "color": "brown",
                "rating": 4,
            },
            headers={"Authorization": f"Bearer {pytest.api_token}"},
        )

        # Get the ID
        llama_id = response.json()["id"]

        # load the bytes for the picture
        with open("./tests/test_images/test_llama_1.png", "rb") as file:
            picture_bytes = file.read()

        response = pytest.client.post(
            f"/llama/{llama_id}/picture",
            content=picture_bytes,
            headers={
                "Authorization": f"Bearer {pytest.api_token}",
            },
        )
        assert response.status_code == 201

        # delete the llama picture
        response = pytest.client.delete(f"/llama/{llama_id}/picture")

        assert response.status_code == 403
