"""
This script gets all the llamas from the llama store and downloads their images

It starts by creating a user and then creating an access token for that user. It then uses the access token to get all
the llamas and then downloads their images.

You will need to install the built llama store SDK to run this script.

- Generate the SDK by running liblab build. If you don't have liblab installed, you can install by following
  the instructions in the docs at https://developers.liblab.com
- Install the SDK using the install script in the Python SDK directory
- Ensure the llama store is running
- Run this script
"""
import os

from typing import List
from llama_store import LlamaStore
from llama_store.net.transport.request_error import RequestError
from llama_store.services.user import User as UserService, UserRegistration
from llama_store.services.token import TokenService, ApiTokenRequest
from llama_store.services.llama import LlamaService, Llama
from llama_store.services.llama_picture import LlamaPictureService

# Create an instance of the llama store SDK
llama_store = LlamaStore()

# Create a user
# For this we can use the user service
user_service: UserService = llama_store.user

# Create the registration object
user_registration = UserRegistration(email="noone@example.com", password="Password123!")

# Try to register the user. If the user already exists, a 400 will be thrown
try:
    user_service.register_user(user_registration)
    print("User created")
except RequestError as e:
    if e.status == 400:
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
print("Access token set")
print(f"Access token: {token.access_token}")

# Get all the llamas
# For this we can use the llama service
llamas: LlamaService = llama_store.llama

# Get the llamas
results: List[Llama] = llamas.get_llamas()

# Print the llama names
print("\nLlama names:")
for llama in results:
    print(llama.name)

# Download all the llama images
llama_picture_service: LlamaPictureService = llama_store.llama_picture

print("\nDownloading llama images:")

# Create a pics directory if it doesn't exist
if not os.path.exists("pics"):
    os.makedirs("pics")

for llama in results:
    # Download the image
    image = llama_picture_service.get_llama_picture_by_llama_id(llama.llama_id)

    # Save the image
    with open(f"./pics/{llama.name}.png", "wb") as f:
        f.write(image)
        print(f"Downloaded image for {llama.name}")
