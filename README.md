# liblab Llama store

![Linting: pylint, Code style: black](https://github.com/liblaber/llama-store/workflows/Lint/badge.svg) ![Test with pytest](https://github.com/liblaber/llama-store/workflows/Run%20pytest/badge.svg)![Check spec](https://github.com/liblaber/llama-store/workflows/Update%20OpenAPI%20specs/badge.svg)

![A llama on a stage by a microphone drawn as a bad cartoon](/img/llama-del-rey.webp)

This is a sample API project to demonstrate how [liblab](https://liblab.com) can generate better SDKs for your APIs. This API has a well-formed OpenAPI spec that generates high quality SDKs.

## Run the API

### Install the dependencies

This API is written in Python using FastAPI. To run it, you'll need Python 3.9 or later. You can install the dependencies using pip, ideally inside a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

This repo also has a devContainer file, so you can also open it using the dev container in VS Code, GitHub codespaces or other compatible IDE. If you do this, the environment will be fully configured for you.

### Prime the database

Before you can run the API you need to configure the SQLite database that is used to store the llamas. This database needs to be primed with some llama data for 6 llamas, as well as creating some pictures. You can create the database using the `recreate_database.sh` script in the [`scripts`](./scripts/) folder:

```bash
cd scripts
./recreate_database.sh
```

This will create a database called `sql_app.db` in the [`llama_store/.appdata`](/llama_store/.appdata) folder. It will add the following tables to this database:

| Table                   | Description |
| ----------------------- | ----------- |
| users                   | Contains the users |
| secrets                 | Contains the secret key used to sign JWT tokens |
| llamas                  | Contains all the llama |
| llama_picture_locations | Contains the locations on disk of the pictures of the llamas |

The script will also create a folder called [`llama_store/.appdata/llama_store_data/pictures`](/llama_store/.appdata/llama_store_data/pictures) and populate it with pictures of the initial llamas.

> If you use the dev container, then this step will be run for your automatically.

### Launch the API app

To run the API, navigate to the `llama_store` folder and run the `main.py` file:

```bash
cd llama_store
python main.py
```

You can also run this from the command line using the `uvicorn` command:

```bash
uvicorn main:app --reload
```

Either way will launch the API on localhost on port 8000. You can then navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to see the Swagger UI for the API. You can change the port number by passing the `--port` parameter to `uvicorn`:
  
```bash
uvicorn main:app --reload --port 80
```

### Run the endpoint as readonly

If you want to run this endpoint with the llamas as readonly (for example when hosting publicly and you don't want nefarious members of the public uploading pictures of llamas), you can set the `ALLOW_WRITE` environment variable to `false`.

### Debug endpoints

This API also can also support GETs on the `/user` endpoint to list the users when debugging. To turn this on, set the `DEBUG` environment variable to `true`. **DO NOT** do this in production.

## Run the API in a Docker container

The API can also be run in a Docker container. To do this, you need to build the container image. On x86/x64 platforms run:

```bash
docker buildx build -t llama-store .
```

On ARM64 (such as macOS on Apple Silicon), run the following:

```bash
docker buildx build --platform=linux/arm64 -t llama-store .
```

You can then run the container. On x86/x64 platforms run:

```bash
docker run -p 80:8000 llama-store
```

On ARM64 (such as macOS on Apple Silicon), run the following:

```bash
docker run --platform=linux/arm64 -p 8000:80 llama-store
```

This will run on port 8000. Change the port number if you want to run it on a different port. The Docker container exposes port 80, but this run command maps it to port 8000 on the host to be consistent with the default `uvicorn` command.

## API end points

This API has the following end points:

| Endpoint                     | Description |
| ---------------------------- | ----------- |
| `/openapi.json`              | The OpenAPI spec for the API as a JSON document |
| `/openapi.yaml`              | The OpenAPI spec for the API as a YAML document |
| `/docs`                      | The Swagger UI for the API |
| `/redoc`                     | The ReDoc UI for the API |
| `/user`                      | Register and get a user. You need an access token to get your user. |
| `/token`                     | Get a JWT token for a user |
| `/llama`                     | Create, read, update, or delete llamas. You need an access token to use this endpoint. |
| `/llama/{llama_id}/pictures` | Create, read, update, or delete a picture for a llama. You need an access token to use this endpoint. |

You can read more about each endpoint in the Swagger UI or ReDoc UI by accessing the `/docs` or `/redoc` endpoints from your browser.

## Register and create an access tokens

To access the API, you need to have a valid user, and an access token. This API uses JWT tokens, signed with a secret key. The secret key is stored in the database, and is created when the database is created. The secret key is not exposed by the API. These tokens are valid for 30 minutes, and are bearer tokens passed in the `Authorization` header, with the value `Bearer <access_token>`.

To create a user, send a POST request to the `/user` endpoint, passing in a JSON body with the following format:

```json
{
  "email": "string",
  "password": "string"
}
```

The email is validated to ensure it is a valid email address, and the password must be at least 8 characters long, with one upper case letter, one lower case letter, one number, and one special character.

This endpoint does not require an access token.

Once your user has been created, you can request an access token by sending a POST request to the `/token` endpoint, passing in a JSON body with the following format:

```json
{
  "email": "string",
  "password": "string"
}
```

This needs to match the user you created. If the user is valid, you will get a response with a JSON body with the following format:

```json
{
  "access_token": "string",
  "token_type": "string"
}
```

Once you have the access token, you can use it to access the other endpoints. To do this, you need to pass the access token in the `Authorization` header, with the value `Bearer <access_token>`.

## Generate an SDK

Once your API is running, you can generate an SDK. Start by installing liblab:

```bash
npm install -g liblab
```

You will need to register or login using:

```bash
liblab login
```

If you don't have an account - [join our beta](https://liblab.com/join).

You can learn more about how to use liblab from our [developer docs](https://developers.liblab.com).

The liblab CLI uses a [config file called `liblab.config.json`](https://developers.liblab.com/cli/config-file-overview) to configure the SDK. This repo has a config file called [`liblab.config.json`](./liblab.config.json) that you can use to generate the SDK. This config file has the following settings:

```json
{
  "sdkName": "llama-store",
  "specFilePath": "spec.json",
  "languages": [
    "python",
    "java",
    "typescript"
  ],
  "auth": [
    "bearer"
  ],
  "createDocs": true,
  "customizations": {
    "devContainer": true,
    "license": {
      "type": "MIT"
    }
  },
  "languageOptions": {
    "typescript": {
      "githubRepoName": "llama-store-sdk-typescript",
      "sdkVersion": "0.0.1"
    },
    "python": {
      "pypiPackageName": "LlamaStore",
      "githubRepoName": "llama-store-sdk-python",
      "sdkVersion": "0.0.1"
    },
    "java": {
      "groupId": "com.liblab",
      "githubRepoName": "llama-store-sdk-java",
      "sdkVersion": "0.0.1"
    }
  },
  "publishing": {
    "githubOrg": "liblaber"
  }
}
```

This config file reads the local `spec.json` file. If you want to generate an SDK from a running API, you can change this to the URL of that API. SDKs will be generated for Java, Python and TypeScript with a name of `llama-store` (adjust to be language specific, so `llamaStore` in Java and TypeScript). The SDKs will be configured to use bearer tokens for authentication, and will include documentation. The generated SDKs will also be set up with dev containers for VS Code, so you can open the created SDK folder and get going straight away.

To generate the SDKs, run the following command:

```bash
liblab build
```

The SDKs will be created and downloaded to the `output` folder. You can then use these SDKs in your applications.

SDK docs will also be created, and you will be able to access them online, or download them.

## Build your first app

Once you have the SDK ready, you can write an app against it! For example, for a simple Python app that creates a user, gets an access token, then lists all the llamas by name, use the following code:

```python
from http_exceptions.client_exceptions import BadRequestException

from llamastore import Llamastore
from llamastore.services.user import User as UserService, UserRegistrationModel
from llamastore.services.token import Token as TokenService, ApiTokenRequestModel
from llamastore.services.llama import Llama as LlamaService, GetLlamasResponseModel
from llamastore.services.llama_picture import LlamaPicture as LlamaPictureService

# Create an instance of the llama store SDK
llama_store = Llamastore()

# Create a user
# For this we can use the user service
user_service: UserService = llama_store.user

# Create the registration object
user_registration = UserRegistrationModel(email="noone@example.com", password="Password123!")
user = None

# Try to register the user. If the user already exists, a 400 will be thrown
try:
    user = user_service.register_user(user_registration)
    print("User created")
except BadRequestException as e:
    if e.status_code == 400:
        print("User already exists - user won't be created")
    else:
        raise e

# Create an access token
# For this we can use the token service
token_service: TokenService = llama_store.token

# Create the token request using the same credentials as the user registration
token_request = ApiTokenRequestModel(email=user_registration.email, password=user_registration.password)

# Create the token
token = token_service.create_api_token(token_request)
print("Token created")

# Now we have the token we can set it at the SDK level so we never have to worry about it again
llama_store.set_access_token(token.access_token)

# Get all the llamas
# For this we can use the llama service
llamas: LlamaService = llama_store.llama

# Get the llamas
results: GetLlamasResponseModel = llamas.get_llamas()

# Print the llama names
print("\nLlama names:")
for llama in results:
    print(llama.name)

# Download all the llama images
llama_picture_service: LlamaPictureService = llama_store.llama_picture

print("\nDownloading llama images:")
for llama in results:
    # Download the image
    image = llama_picture_service.get_llama_picture_by_llama_id(llama.id)

    # Save the image
    with open(f"{llama.name}.png", "wb") as f:
        f.write(image.content)
        print(f"Downloaded image for {llama.name}")
```

You can find this and more examples in the [`sdk-examples`](/sdk-examples) folder.

## OpenAPI spec

The OpenAPI spec for this API is in the [`spec.json`](/spec.json) and [`spec.yaml`](/spec.yaml) files. These need to be generated whenever the spec changes. To do this, run the following command:

```bash
cd scripts
./create_specs.sh
```
