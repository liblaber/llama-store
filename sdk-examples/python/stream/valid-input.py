from llama_store import LlamaStore
from llama_store.net.transport.request_error import RequestError
from llama_store.services.user import User as UserService, UserRegistration

# Create an instance of the llama store SDK
llama_store = LlamaStore(access_token=None)

# Create a user
# For this we can use the user service
user_service: UserService = llama_store.user

# Create the registration object
try:
    user_registration = UserRegistration(email="anyone", password="Password123!")
except ValueError as e:
    print("Format is wrong")


user_registration_dict = { "email": "anyone", "password": "Password123!"}
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
except ValueError as e:
    print("Format is wrong")