"""
Methods for interacting with files. Llama pictures are stored on the file system, not in the database.
"""
import io
import os

from PIL import Image


# The root path for all the llama pictures
ROOT_PATH = ".appdata/llama_store_data/pictures"


def create_root_folder_if_not_exists() -> None:
    """
    Creates a folder if it does not already exist.
    """
    if not os.path.exists(ROOT_PATH):
        os.makedirs(ROOT_PATH)


def write_llama_picture_to_file(llama_id: int, body: bytes) -> str:
    """
    Writes a llama picture to a file with the name <llama_id>.png.

    If the image is not a PNG, it is converted.

    :param llama_id: The ID of the llama.
    :param body: The body of the request.
    :return: The file name.
    :rtype: str
    """
    create_root_folder_if_not_exists()

    # Open the image with PIL to check it is a valid image, and to get the file extension
    image = Image.open(io.BytesIO(body))

    # Verify the image - this will raise an exception if the image is not valid
    image.verify()

    # Reopen the image after verifying
    image = Image.open(io.BytesIO(body))

    # Save the image to a file as a png
    file_name = f"{ROOT_PATH}/{llama_id}.png"
    image.save(file_name)

    # Return the file name
    return file_name


def delete_llama_picture_file(image_file_location: str) -> None:
    """
    Deletes a llama picture from the file system.

    :param image_file_location: The location of the image file.
    """
    create_root_folder_if_not_exists()

    if os.path.exists(image_file_location):
        os.remove(image_file_location)
