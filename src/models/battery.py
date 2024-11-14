"""
This module defines data models for handling battery data in FastAPI.
The BatteryData model enforces structured validation for battery fields,
helping the API maintain data integrity, including value ranges.

The model uses DataValidationConfig to ensure descriptions and constraints
align with permissible ranges for each attribute.
"""

from pydantic import BaseModel, Field
from src.config.validation import DataValidationConfig


class BatteryData(BaseModel):
    """
    Data model for battery information.

    Attributes:
    - battery_id (str): Unique identifier for the battery.
    - voltage (int): Battery voltage in volts,
        constrained between {DataValidationConfig.VOLTAGE['min']}
        and {DataValidationConfig.VOLTAGE['max']}.
    - current (int): Battery current in amperes,
        constrained between {DataValidationConfig.CURRENT['min']}
        and {DataValidationConfig.CURRENT['max']}.
    - temperature (int): Battery temperature in degrees Celsius,
        constrained between {DataValidationConfig.TEMPERATURE['min']}
        and {DataValidationConfig.TEMPERATURE['max']}.
    - state_of_charge (int): Battery's state of charge as a percentage,
        constrained between {DataValidationConfig.STATE_OF_CHARGE['min']}
        and {DataValidationConfig.STATE_OF_CHARGE['max']}.
    - state_of_health (int): Battery's state of health as a percentage,
        constrained between {DataValidationConfig.STATE_OF_HEALTH['min']}
        and {DataValidationConfig.STATE_OF_HEALTH['max']}.
    """
    battery_id: str = Field(
        ...,
        description="Unique identifier for the battery"
    )
    voltage: int = Field(
        ...,
        ge=DataValidationConfig.VOLTAGE['min'],
        le=DataValidationConfig.VOLTAGE['max'],
        description=f"Battery voltage in volts "
                    f"({DataValidationConfig.VOLTAGE['min']} to "
                    f"{DataValidationConfig.VOLTAGE['max']})"
    )
    current: int = Field(
        ...,
        ge=DataValidationConfig.CURRENT['min'],
        le=DataValidationConfig.CURRENT['max'],
        description=f"Battery current in amperes "
                    f"({DataValidationConfig.CURRENT['min']} to "
                    f"{DataValidationConfig.CURRENT['max']})"
    )
    temperature: int = Field(
        ...,
        ge=DataValidationConfig.TEMPERATURE['min'],
        le=DataValidationConfig.TEMPERATURE['max'],
        description=f"Battery temperature in Celsius "
                    f"({DataValidationConfig.TEMPERATURE['min']} to "
                    f"{DataValidationConfig.TEMPERATURE['max']})"
    )
    state_of_charge: int = Field(
        ...,
        ge=DataValidationConfig.STATE_OF_CHARGE['min'],
        le=DataValidationConfig.STATE_OF_CHARGE['max'],
        description=f"Battery's state of charge in percentage "
                    f"({DataValidationConfig.STATE_OF_CHARGE['min']} to "
                    f"{DataValidationConfig.STATE_OF_CHARGE['max']})"
    )
    state_of_health: int = Field(
        ...,
        ge=DataValidationConfig.STATE_OF_HEALTH['min'],
        le=DataValidationConfig.STATE_OF_HEALTH['max'],
        description=f"Battery's state of health in percentage "
                    f"({DataValidationConfig.STATE_OF_HEALTH['min']} to "
                    f"{DataValidationConfig.STATE_OF_HEALTH['max']})"
    )
