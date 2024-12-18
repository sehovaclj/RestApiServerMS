"""
This module serves as the entry point for running the FastAPI application.

It creates and runs the FastAPI app instance using Uvicorn as the ASGI server.
The application configuration (such as host and port) is set
via `RestApiConfig`.

"""

import uvicorn
from src.config.api import RestApiConfig
from src.api.app import create_app

# initialize our fast api app
app = create_app()

if __name__ == "__main__":
    uvicorn.run("src.main:app",
                host=RestApiConfig.REST_HOST,
                port=RestApiConfig.REST_PORT)
