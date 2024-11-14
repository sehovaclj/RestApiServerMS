"""
This module defines the `create_app` function, which initializes and
configures the FastAPI application for managing battery data.

The app includes endpoints for interacting with battery data stored in
InfluxDB, allowing users to perform operations such as
querying and deleting data.
"""

from fastapi import FastAPI
from src.api import endpoints


def create_app() -> FastAPI:
    """
    Initializes and configures the FastAPI application.

    The application is set up with a title, description, and version, and
    includes routes for battery data management via the `/battery_data` prefix.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI(
        title="Battery Data API",
        description="API for managing battery data in InfluxDB",
        version="1.0.0"
    )
    app.include_router(endpoints.router, prefix="/batteryData")
    return app
