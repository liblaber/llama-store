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

The liblab CLI uses a [config file called `liblab.config.json`](https://developers.liblab.com/cli/config-file-overview) to configure the SDK. This repo has a config file called [`liblab.config.json`](./liblab.config.json) that you can use to generate the SDK. 

This config file reads the local `spec.json` file. If you want to generate an SDK from a running API, you can change this to the URL of that API. SDKs will be generated for Java, Python and TypeScript with a name of `llama-store` (adjust to be language specific, so `llamaStore` in Java and TypeScript). The SDKs will be configured to use bearer tokens for authentication, and will include documentation. The generated SDKs will also be set up with dev containers for VS Code, so you can open the created SDK folder and get going straight away.

To generate the SDKs, run the following command:

```bash
liblab build
```

The SDKs will be created and downloaded to the `output` folder. You can then use these SDKs in your applications.

SDK docs will also be created, and you will be able to access them online, or download them.

### Pre-built SDKs

You can find pre-built SDKs in the following GitHub repos:

| Language   | Repo |
| ---------- | ---- |
| Python     | [llama-store-sdk-python](https://github.com/liblaber/llama-store-sdk-python) |
| Java       | [llama-store-sdk-java](https://github.com/liblaber/llama-store-sdk-java) |
| TypeScript | [llama-store-sdk-typescript](https://github.com/liblaber/llama-store-sdk-typescript) |
| C#         | [llama-store-sdk-csharp](https://github.com/liblaber/llama-store-sdk-csharp) |
| Go         | [llama-store-sdk-go](https://github.com/liblaber/llama-store-sdk-go) |

These are generated by a GitHub action, and are updated whenever the spec changes. You can find the `publish_sdk.yaml` action in the [`.github/workflows`](./.github/workflows) folder.

This is the action:

```yaml
name: Publish SDK

on:
  push:
    paths:
      - 'spec.json'
  workflow_dispatch:

jobs:
  build-and-pr:
    name: Generate SDKs and create PRs
    runs-on: ubuntu-latest
    env:
      LIBLAB_TOKEN: ${{ secrets.LIBLAB_TOKEN }}
      GITHUB_TOKEN: ${{ secrets.LIBLAB_GITHUB_TOKEN }}
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Setup Node.js environment
        uses: actions/setup-node@v3
        with:
          node-version: "18" # Specify the node version you want to use
      - name: Install liblab
        run: npm install -g liblab
      - name: Start Build
        run: liblab build --skip-validation --approve-docs
      - name: Create PRs to GitHub repos
        run: liblab pr
```

You can read more about the process to publish an SDK in an action in our [developer docs](https://developers.liblab.com/cli/cli-overview-publish).

## Run the SDK examples

There are SDK examples for TypeScript and Python in the [`sdk-examples`](./sdk-examples) folder.

Before running these examples, you will need to have the llama store running with a clean database. For best results, use the dev container in this repo:

1. Ensure you have Docker running
1. Ensure you have the VS Code remote development extension pack installed
1. Open this repo in VS Code, and when prompted re-open in the container

This will install everything you need.

Next you will need to build the SDKs:

1. Run `liblab login` to login (the liblab CLI is installed as part of this dev container).
1. Run `liblab build` from the root of this repo. This will build against a saved version of the spec.

Next, you need to launch the Llama store:

1. From a terminal, run:

    ```bash
    ./scripts/start_llama_store.sh
    ```

    This will reset the llama store database, then launch the API on port 8000.

Once you have done this, you can run the examples. You will need to create a new terminal to do this.

### TypeScript

To run the TypeScript examples, navigate to the [`sdk-examples/typescript`](./sdk-examples/typescript) folder.

1. Build the SDK with the following command from that folder:

    ```bash
    npm run setup
    ```
1. Run the get llamas demo with the following command:

    ```bash
    npm run get-llamas
    ```

    This will create a user, generate an API token, and print out a list of llamas. This demo shows the ability to call services on the SDK, set an API token once, and use that for all subsequent calls.
  
1. Run the create llamas demo with the following command:

    ```bash
    npm run create-llamas
    ```

    This will create a user, generate an API token, and create a llama.

1. Run the get llamas demo again with the following command:

    ```bash
    npm run get-llamas
    ```

    You will see the llama you created in the previous step in the list of llamas.

### Python

To run the Python examples, navigate to the [`sdk-examples/python`](./sdk-examples/python) folder.

1. Build and install the Python SDK with the following command from that folder:

    ```bash
    ./setup-python.sh
    ```

    This assumes you are running in a dev container as it doesn't create a virtual environment. If you plan to run this locally, you should create and activate a virtual environment first.
  
1. Run the get llamas demo with the following command:

    ```bash
    python get_llamas.py
    ```

    This will create a user, generate an API token, and print out a list of llamas. It will also download pictures for all the llamas into the `pics` folder. This demo shows the ability to call services on the SDK, set an API token once, and use that for all subsequent calls.

1. Run the create llamas demo with the following command:

    ```bash
    python create_llamas.py
    ```

    This will create a user, generate an API token, and create a llama, uploading a picture.

1. Run the get llamas demo again with the following command:

    ```bash
    python get_llamas.py
    ```

    You will see the llama you created in the previous step in the list of llamas.

### Go

To run the Go examples, you will need to copy the contents of the [`sdk-examples/go`](./sdk-examples/go) folder into the [`output/go/cmd/examples`](./output/go/cmd/examples) folder.

1. Run the get llamas demo with the following command:

    ```bash
    go run get-llamas.go
    ```

    This will create a user, generate an API token, and print out a list of llamas. This demo shows the ability to call services on the SDK, set an API token once, and use that for all subsequent calls.

1. Run the create llamas demo with the following command:

    ```bash
    go run create-llama.go
    ```

    This will create a user, generate an API token, and create a llama, uploading a picture.

1. Run the get llamas demo again with the following command:

    ```bash
    go run get-llamas.go
    ```

    You will see the llama you created in the previous step in the list of llamas.

## OpenAPI spec

The OpenAPI spec for this API is in the [`spec.json`](/spec.json) and [`spec.yaml`](/spec.yaml) files. These need to be generated whenever the spec changes. To do this, run the following command:

```bash
cd scripts
./create_specs.sh
```
