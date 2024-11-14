"""
Unit tests for InfluxDB connection.
"""

import pytest
from src.db.connection import connect_to_influxdb


@pytest.mark.db_connection
def test_connect_to_influxdb_success():
    """
    Unit test to connect to InfluxDB and verify that the Write API is returned.
    """
    connection = connect_to_influxdb()

    # Assert that the InfluxDBClient and Write API were successfully returned
    assert connection is not None, \
        "Failed to connect to InfluxDB and retrieve Write API."

    client, write_api, query_api, delete_api = connection

    # Ensure that the Write API is not None
    assert write_api is not None, "Write API was not initialized."
    assert query_api is not None, "Query API was not initialized."
    assert delete_api is not None, "Delete API was not initialized."

    # Clean up by closing the InfluxDB client connection
    client.close()
