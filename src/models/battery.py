"""
This module defines data models for handling battery data within the FastAPI application.
The BatteryData model provides structured validation and description for battery-related fields,
enabling the API to enforce data integrity for each operation, including value ranges.
"""

from pydantic import BaseModel, Field

from src.config.validation import DataValidationConfig


class BatteryData(BaseModel):
    """
    Data model for battery information.

    Attributes:
    - battery_id (str): Unique identifier for the battery.
    - voltage (int): Battery voltage in volts,
        constrained between 0 and 600.
    - current (int): Battery current in amperes,
        constrained between 0 and 200.
    - temperature (int): Battery temperature in degrees Celsius,
        constrained between -100 and 1000.
    - state_of_charge (int): Battery's state of charge as a percentage,
        constrained between 0 and 100.
    - state_of_health (int): Battery's state of health as a percentage,
        constrained between 0 and 100.
    """
    battery_id: str = Field(
        ...,
        description="Unique identifier for the battery"
    )
    voltage: int = Field(
        ...,
        ge=DataValidationConfig.VOLTAGE['min'],
        le=DataValidationConfig.VOLTAGE['max'],
        description="Battery voltage in volts (0 to 600)"
    )
    current: int = Field(
        ...,
        ge=DataValidationConfig.CURRENT['min'],
        le=DataValidationConfig.CURRENT['max'],
        description="Battery current in amperes (0 to 200)"
    )
    temperature: int = Field(
        ...,
        ge=DataValidationConfig.TEMPERATURE['min'],
        le=DataValidationConfig.TEMPERATURE['max'],
        description="Battery temperature in Celsius (-100 to 1000)"
    )
    state_of_charge: int = Field(
        ...,
        ge=DataValidationConfig.STATE_OF_CHARGE['min'],
        le=DataValidationConfig.STATE_OF_CHARGE['max'],
        description="Battery's state of charge in percentage (0 to 100)"
    )
    state_of_health: int = Field(
        ...,
        ge=DataValidationConfig.STATE_OF_HEALTH['min'],
        le=DataValidationConfig.STATE_OF_HEALTH['max'],
        description="Battery's state of health in percentage (0 to 100)"
    )
