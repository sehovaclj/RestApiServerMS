"""
endpoints.py

This module defines API endpoints for handling battery data within
the FastAPI application. Each endpoint allows for specific operations,
including querying, adding and deleting battery data points in the InfluxDB
database.

The module routes are prefixed with '/battery_data' for clarity.
"""

from fastapi import APIRouter, HTTPException

from pydantic import ValidationError

from src.config.logging import LoggingConfig
from src.services.influx_manager import InfluxManager
from src.models.battery import BatteryData

# initialize the logger
logger = LoggingConfig.get_logger(__name__)

# initialize the api router from fast api
router = APIRouter()

# initialize influx manager
influx_manager = InfluxManager()


# Root endpoint
@router.get("/healthCheck")
async def health_check():
    """
    health check endpoint for checking the API status.
    """
    return {"message": "Battery Data API is running"}


@router.get("/query")
async def query_battery_data(
        battery_id: str,
        start_time: str,
        stop_time: str,
        field: str) -> list[dict]:
    """
    Get battery data for a specified battery_id, time range, and field.

    Parameters:
    - battery_id: (str) - Identifier for the battery.
    - start_time: (str) - Start of the time range, ex. "-2h"
    - stop_time: (str) - End of the time range, ex. "-1m"
    - field: (str) - Field to retrieve.

    Returns:
    - list[dict]: list of data points matching the query.

    Raises:
    - HTTPException:
        - 400 if there is a ValueError, with details about the error.
        - 500 for any other exceptions, with details about the server error.
    """
    try:
        data = influx_manager.query_data(
            battery_id, start_time, stop_time, field
        )
        return [dict(point) for point in data]
    except ValueError as err:
        raise HTTPException(
            status_code=400, detail=f"Value error: {err}") from err

    except Exception as err:
        raise HTTPException(
            status_code=500, detail=f"Server error: {err}") from err


@router.post("/add")
async def add_battery_data(data: BatteryData) -> dict[str, str]:
    """
    Add a new battery data point. FastAPI will automatically validate the
        request message against our BatteryData model in src.models.battery.py

    Parameters:
    - data: (BatteryData) - The battery data payload excluding timestamps.

    Returns:
    - dict[str, str]: A dictionary with a status message {"status": "deleted"}
        if insert is successful.

    Raises:
    - HTTPException:
        - 422 if there is a ValidationError, with details about the error.
        - 500 for any other exceptions, with details about the server error.
    """
    try:
        influx_manager.insert_data(data.model_dump())
        return {"status": "success"}
    except ValidationError as err:
        raise HTTPException(
            status_code=422, detail=f"Validation error: {err}") from err
    except Exception as err:
        raise HTTPException(
            status_code=500, detail=f"Server error: {err}") from err


@router.delete("/remove")
async def remove_battery_data(
        battery_id: str,
        start_time: str,
        stop_time: str) -> dict[str, str]:
    """
    Delete battery data for a specified battery_id and time range.

    Parameters:
    - battery_id: (str) - Identifier for the battery.
    - start_time: (str) - Start of the time range, ex. "-2h"
    - stop_time: (str) - End of the time range, ex. "-1m"

    Returns:
    - dict[str, str]: A dictionary with a status message {"status": "deleted"}
      if deletion is successful.

    Raises:
    - HTTPException:
        - 400 if there is a ValueError, with details about the error.
        - 500 for any other exceptions, with details about the server error.
    """
    try:
        print(battery_id, start_time, stop_time)
        influx_manager.delete_data(
            battery_id, start_time, stop_time
        )
        return {"status": "deleted"}
    except ValueError as err:
        raise HTTPException(
            status_code=400, detail=f"Value error: {err}") from err
    except Exception as err:
        raise HTTPException(
            status_code=500, detail=f"Server error: {err}") from err
