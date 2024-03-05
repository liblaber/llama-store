"""
This script creates a new llama in the llama store, then sets its picture. using the REST API

It starts by creating a user and then creating an access token for that user. It then uses the access token to
create the llama and upload the picture.

This compares the developer experience of using the REST API directly with the developer experience of using an SDK
"""
import json
import requests

# The URL of the llama store API
BASE_URL = "http://localhost:8000/"

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
token = token_response_json["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Create the new llama request
new_llama_request = {
    "name": "Llamapoleon Bonaparte",
    "age": 5,
    "color": "white",
    "rating": 4
}

# Create the llama
llama_response = requests.post(BASE_URL + "llama", json=new_llama_request, timeout=5, headers=headers)
print(f"Response status code: {llama_response.status_code}")
print(json.dumps(llama_response.json(), indent=2))
id = llama_response.json()["id"]

# Upload the llama picture
# Open the llama picture
with open("../create-pics/llamapoleon-bonaparte.png", "rb") as f:
    llama_picture = f.read()

# Upload the picture
llama_picture_response = requests.post(BASE_URL + f"llama/{id}/picture", data=llama_picture, timeout=5, headers=headers)
print("Uploaded llama picture")
