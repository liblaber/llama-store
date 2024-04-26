"""
This script gets all the llamas from the llama store and downloads their images using the REST API

It starts by creating a user and then creating an access token for that user. It then uses the access token to get all
the llamas and then downloads their images.

This compares the developer experience of using the REST API directly with the developer experience of using an SDK
"""
import json
import requests

# The URL of the llama store API
BASE_URL = "http://localhost:8080/"

# Build the new user as a JSON object
new_user = {
    "email": "llama@liblab.com",
    "password": "Llama123!",
}

# Send the post request
user_response = requests.post(BASE_URL + "user", json=new_user, timeout=5)

# Show the response
print(f"Response status code: {user_response.status_code}")
print(json.dumps(user_response.json(), indent=2))

# Build the token request as a JSON object
token_request = {
    "email": "llama@liblab.com",
    "password": "Llama123!",
}

# Send the post request
token_response = requests.post(BASE_URL + "token", json=token_request, timeout=5)
token_response_json = token_response.json()

# Get the token from the response
token = token_response_json["accessToken"]
headers = {"Authorization": f"Bearer {token}"}

# Get the llamas
llamas_response = requests.get(BASE_URL + "llama", timeout=5, headers=headers)
llamas_response_json = llamas_response.json()

print(f"Response status code: {llamas_response.status_code}")
print(json.dumps(llamas_response_json, indent=2))

# Download all the llama images
print("\nDownloading llama images:")

# Create a pics directory if it doesn't exist
import os
if not os.path.exists("pics"):
    os.makedirs("pics")
else:
    # delete all the files in the pics directory
    for file in os.listdir("pics"):
        os.remove(f"./pics/{file}")

for llama in llamas_response_json:
    llama_id = llama["llamaId"]

    # Download the image
    llama_picture_response = requests.get(BASE_URL + f"llama/{llama_id}/picture", timeout=5, headers=headers)

    # Save the image
    with open(f"./pics/{llama['name']}.png", "wb") as f:
        f.write(llama_picture_response.content)
        print(f"Downloaded image for {llama['name']}")
