"""
This module defines the DataValidationConfig class, which provides
configuration for validating battery parameters in an IoT setting.

Each attribute in the class represents a parameter with its expected
data type and permissible range of values for validation purposes.
"""


class DataValidationConfig:
    """
    Configuration for data validation of expected battery parameters.
    """

    BATTERY_ID = {"type": int}
    VOLTAGE = {"type": int, "min": 0, "max": 600}
    CURRENT = {"type": int, "min": 0, "max": 200}
    TEMPERATURE = {"type": int, "min": -100, "max": 1000}
    STATE_OF_CHARGE = {"type": int, "min": 0, "max": 100}
    STATE_OF_HEALTH = {"type": int, "min": 0, "max": 100}
