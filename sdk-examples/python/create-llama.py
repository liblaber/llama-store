"""
This script creates a new llama in the llama store, then sets its picture.

It starts by creating a user and then creating an access token for that user. It then uses the access token to
create the llama and upload the picture.

You will need to install the built llama store SDK to run this script.

- Generate the SDK by running liblab build. If you don't have liblab installed, you can install by following
  the instructions in the docs at https://developers.liblab.com
- Install the SDK using the install script in the Python SDK directory
- Ensure the llama store is running
- Run this script

This script will upload a llama picture called llamapoleon-bonaparte.png. This file needs to
be in the same directory as this script.
"""
from typing import List

from llama_store import LlamaStore
from llama_store.net.transport.request_error import RequestError
from llama_store.services.user import User as UserService, UserRegistration
from llama_store.services.token import TokenService, ApiTokenRequest
from llama_store.services.llama import LlamaService, LlamaCreate
from llama_store.services.llama_picture import LlamaPictureService
from llama_store.models.llama_color import LlamaColor

# Create an instance of the llama store SDK
llama_store = LlamaStore(access_token=None)

# Create a user
# For this we can use the user service
user_service: UserService = llama_store.user

# Create the registration object
user_registration = UserRegistration(email="noone@example.com", password="Password123!")
user = None

# Try to register the user. If the user already exists, a 400 will be thrown
try:
    user = user_service.register_user(user_registration)
    print("User created")
except RequestError as e:
    if e.status_code == 400:
        print("User already exists - user won't be created")
    else:
        raise e

# Create an access token
# For this we can use the token service
token_service: TokenService = llama_store.token

# Create the token request using the same credentials as the user registration
token_request = ApiTokenRequest(email=user_registration.email, password=user_registration.password)

# Create the token
token = token_service.create_api_token(token_request)
print("Token created")

# Now we have the token we can set it at the SDK level so we never have to worry about it again
llama_store.set_access_token(token.access_token)

# Create a new llama
# For this we can use the llama service and the llama picture service
llamas: LlamaService = llama_store.llama
llama_picture_service: LlamaPictureService = llama_store.llama_picture

# Define the create llama request
new_llama_request = LlamaCreate(
    name="Llamapoleon Bonaparte",
    age=5, 
    color=LlamaColor.WHITE, 
    rating=4)

# Create the llama
new_llama = llamas.create_llama(new_llama_request)
print(f"Created llama {new_llama.name} with ID {new_llama.llama_id}")

# Upload the llama picture
# Open the llama picture
with open("../create-pics/llamapoleon-bonaparte.png", "rb") as f:
    llama_picture = f.read()

# Upload the picture
llama_picture_service.create_llama_picture(new_llama.llama_id, llama_picture)
print("Uploaded llama picture")
