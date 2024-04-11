"""
This is a sample API for use with liblab. You should be able to quickly generate an SDK from this API.

To generate an SDK:

Make sure this is running:
    pip install -r requirements.txt
    python main.py

Install liblab:

    npm install -g liblab

Create a liblab config file:

    liblab init

Generate an SDK:

    liblab build

This will create an SDK in the output folder. You can then use the SDK in your project, or see one of the examples.
"""

import functools
import io
import os

from dotenv import load_dotenv

from fastapi import FastAPI, Response
import uvicorn
import yaml

from data import schema
from data.database import engine
from openapi import fix_openapi_spec, OPENAPI_DESCRIPTION
from routers import (
    llama_picture_read,
    llama_picture_write,
    llama_read,
    llama_write,
    token,
    user_debug,
    user_read,
    user_write,
)

# Load the environment variables
load_dotenv()

# Create the database tables
schema.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Llama",
        "description": "Get the llamas",
    },
    {
        "name": "LlamaPicture",
        "description": "Get the llama pictures",
    },
    {
        "name": "User",
        "description": "Register users",
    },
    {
        "name": "Token",
        "description": "Manage API Tokens",
    },
]

app = FastAPI(
    servers=[{"url": "http://localhost:8080", "description": "Prod"}],
    contact={"name": "liblab", "url": "https://liblab.com"},
    description=OPENAPI_DESCRIPTION,
    openapi_tags=tags_metadata,
    version="0.1.7",
    redirect_slashes=True,
    title="Llama Store API",
)

# Get the environment variables to see if we are in debug/write mode
allow_write: bool = os.environ.get("ALLOW_WRITE", "true").lower() == "true"
debug: bool = os.environ.get("DEBUG", "false").lower() == "true"

# Add the routers - do it in this order so that they appear in the OpenAPI spec in this order

# Add the llama routers
# Include the read only production routers
app.include_router(llama_picture_read.router)
app.include_router(llama_read.router)

# Include the write routers if we are in allow write mode
# This is so we can run this in production and not worry about folks
# writing to our database maliciously
if allow_write:
    print("RUNNING IN WRITE MODE")
    app.include_router(llama_picture_write.router)
    app.include_router(llama_write.router)

# Add the token router
app.include_router(token.router)

# Add the user routers
app.include_router(user_read.router)
app.include_router(user_write.router)

# Include the debug routers if we are in debug mode
if debug:
    print("RUNNING IN DEBUG MODE")
    app.include_router(user_debug.router)

# Tweak the OpenAPI spec
fix_openapi_spec(app)


@app.get("/openapi.yaml", include_in_schema=False)
@functools.lru_cache()
def read_openapi_yaml() -> Response:
    """
    Add support for a YAML OpenAPI spec. This will return the OpenAPI spec converted to YAML.

    :return: The OpenAPI spec converted to YAML.
    :rtype: Response
    """
    openapi_json = app.openapi()
    yaml_s = io.StringIO()
    yaml.dump(openapi_json, yaml_s, sort_keys=False)
    return Response(yaml_s.getvalue(), media_type="text/yaml")


# Run the app
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
