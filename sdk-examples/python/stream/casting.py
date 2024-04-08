from typing import List
from llama_store import LlamaStore
from llama_store.net.transport.request_error import RequestError
from llama_store.services.user import User as UserService, UserRegistration
from llama_store.services.token import TokenService, ApiTokenRequest
from llama_store.services.llama import LlamaService

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

# Create the registration object
user_registration_dict = { "email": "someone@example.com", "password": "Password123!"}
user = None

# Try to register the user. If the user already exists, a 400 will be thrown
try:
    user = user_service.register_user(user_registration_dict)
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
# For this we can use the llama service
llamas: LlamaService = llama_store.llama

# Define the create llama request
new_llama_request = {
    "name":"Llama Llama Duck",
    "age":"5", 
    "color":"white", 
    "rating":4
    }

# Create the llama
new_llama = llamas.create_llama(new_llama_request)
print(f"Created llama {new_llama.name} with ID {new_llama.llama_id}")