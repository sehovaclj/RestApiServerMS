"""
This module defines the InfluxManager class, which provides methods for
interacting with InfluxDB to manage battery data. It includes operations
for querying, inserting, updating, and deleting data points with
appropriate error handling and type annotations.
"""

from typing import List, Dict, Any
from influxdb_client import Point

from src.config.logging import LoggingConfig
from src.config.db import DbConfig
from src.db.connection import connect_to_influxdb
from src.utils.datetime_utils import utc_now_timestamp, \
    calculate_start_stop_times

# initialize logger for this module
logger = LoggingConfig.get_logger(__name__)


class InfluxManager:
    """
    Provides methods for managing battery data in InfluxDB.

    This class allows querying, inserting, and deleting battery data points
    within an InfluxDB instance. It includes operations for retrieving data
    within specified time ranges, adding new entries, and removing records
    based on a battery ID and time range.

    Attributes:
    - client (InfluxDBClient): The main client connection to InfluxDB.
    - write_api (WriteApi): Interface for writing data points to InfluxDB.
    - query_api (QueryApi): Interface for querying data from InfluxDB.
    - delete_api (DeleteApi): Interface for deleting data in InfluxDB.
    """

    def __init__(self):
        """
        Initializes the InfluxManager instance.

        Establishes connections to the InfluxDB client and sets up the APIs
        required for write, query, and delete operations.
        """
        self.client, self.write_api, self.query_api, self.delete_api = (
            connect_to_influxdb()
        )

    def query_data(self,
                   battery_id: str,
                   start_time: str,
                   stop_time: str,
                   field: str) -> List[Dict[str, Any]]:
        """
        Queries battery data from InfluxDB within a specified
            time range and field.

        Parameters:
        - battery_id (str): The unique identifier for the battery.
        - start_time (str): Start time range for the query, e.g., "-2h"
        - stop_time (str): Stop time range for the query, e.g., "-1m"
        - field (str): The specific data field to retrieve (e.g., "voltage").

        Returns:
        - List[Dict[str, Any]]: A list of dictionaries containing timestamps
          and field values, with each dictionary in the format
            {"time": ..., "value": ...}.
        """
        query = f'''
        from(bucket: "{DbConfig.INFLUX_BUCKET}")
            |> range(start: {start_time}, stop: {stop_time})
            |> filter(fn: (r) => r["_measurement"] == "battery_data" 
                              and r["battery_id"] == "{battery_id}"
                              and r["_field"] == "{field}")
            |> sort(columns: ["_time"], desc: true) 
        '''
        result = self.query_api.query(query)
        return [{"time": record.get_time(), "value": record.get_value()} for
                table in result for record in table.records]

    def insert_data(self, data: Dict[str, Any]) -> None:
        """
        Inserts a new battery data point into InfluxDB.

        Parameters:
        - data (Dict[str, Any]): Dictionary containing the battery data,
          including fields like "battery_id", "voltage", "current",
          "temperature", "state_of_charge", and "state_of_health".

        """
        # set timestamp to now
        utc_now_ts = utc_now_timestamp()
        # create influx db data point
        point = (
            Point("battery_data")
            .tag("battery_id", str(data.get("battery_id")))
            .field("voltage", data.get("voltage"))
            .field("current", data.get("current"))
            .field("temperature", data.get("temperature"))
            .field("state_of_charge", data.get("state_of_charge"))
            .field("state_of_health", data.get("state_of_health"))
            .field("influx_timestamp", utc_now_ts)
            .field("latency_ms", 0)
            .time(utc_now_ts, write_precision="ms")
        )
        self.write_api.write(
            bucket=DbConfig.INFLUX_BUCKET,
            org=DbConfig.INFLUX_ORG,
            record=point
        )
        logger.info("Inserted data point in InfluxDB")

    def delete_data(self,
                    battery_id: str,
                    start_time: str,
                    stop_time: str
                    ) -> None:
        """
        Deletes battery data for a specified battery_id within a
            given time range.

        Parameters:
        - battery_id (str): The unique identifier for the battery.
        - start_range (str): The start time of the range for deletion.
        - stop_range (str): The end time of the range for deletion.
        """
        # Calculate start and stop times using the provided ranges
        start_time, stop_time = calculate_start_stop_times(
            start_time, stop_time
        )
        print(start_time, stop_time)
        # Use the delete API to remove the data within the specified time range
        self.delete_api.delete(
            start=start_time,
            stop=stop_time,
            predicate=f'battery_id="{battery_id}"',
            bucket=DbConfig.INFLUX_BUCKET,
            org=DbConfig.INFLUX_ORG
        )
        logger.info("Deleted data point in InfluxDB")
