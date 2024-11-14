"""
Configures the REST API parameters using environment variables.

Reads from a `.env` file to set REST API parameters.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class RestApiConfig:
    """
    Configuration class for REST API settings.

    This class loads the REST API configuration from environment variables.
    """
    # REST API configuration
    REST_HOST = os.getenv('REST_HOST')
    REST_PORT = int(os.getenv('REST_PORT'))
