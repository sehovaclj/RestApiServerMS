"""
This module provides utility functions for working with date and time.
"""

from datetime import datetime, timezone, timedelta


def utc_now_timestamp() -> int:
    """
    Gets the current UTC time as a timestamp in milliseconds.

    Returns:
        int: The current UTC timestamp in milliseconds since the Unix epoch.
    """
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def parse_relative_time(time_str: str) -> timedelta:
    """
    Parses a relative time string into a `timedelta` object.

    This function converts a time duration string (e.g.,
    "-5m", "-2h", "-3d", "-1mo") into a `timedelta` object for easy
    manipulation of time intervals. Supported units include milliseconds
    ("ms"), seconds ("s"), minutes ("m"), hours ("h"), days ("d"), weeks ("w"),
    months ("mo"), and years ("y"). Note that "mo" and "y" are approximate
    (30 and 365 days, respectively).

    Parameters:
    - time_str (str): A string representing the relative time,
                      where the last character(s) indicate the unit.

    Returns:
    - timedelta: The corresponding `timedelta` object for the parsed time.

    Raises:
    - ValueError: If the provided time unit is unsupported.
    """
    # Mapping of units to timedelta arguments
    unit_mapping = {
        "ms": "milliseconds",
        "s": "seconds",
        "m": "minutes",
        "h": "hours",
        "d": "days",
        "w": "weeks",
        "mo": 30 * 86400,  # 30 days in seconds for approximation
        "y": 365 * 86400  # 365 days in seconds for approximation
    }

    # Extract the unit and amount
    unit = time_str[-2:] if time_str[-2:] in {"mo", "ms"} else time_str[-1]
    amount = int(time_str[1:-len(unit)])

    # Handle approximate units for months and years separately
    if unit in {"mo", "y"}:
        delta = timedelta(seconds=amount * unit_mapping[unit])
    elif unit in unit_mapping:
        delta = timedelta(**{unit_mapping[unit]: amount})
    else:
        raise ValueError("Unsupported time unit")

    return delta


def calculate_start_stop_times(start_time: str,
                               stop_time: str) -> tuple[str, str]:
    """
    Calculates the start and stop times based on relative time strings.

    Args:
        start_time (str): The start time range (e.g., "-2h").
        stop_time (str): The stop time range (e.g., "-1m").

    Returns:
        tuple[str, str]: The calculated start and stop times in
            RFC3339Nano format without timezone effect.
    """
    # Get the current UTC time as a datetime object
    now = datetime.now(timezone.utc)

    # Calculate start and stop times based on relative ranges
    start_time = now - parse_relative_time(start_time)
    stop_time = now - parse_relative_time(stop_time)

    # Format the times as RFC3339Nano (no offset)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    stop_time_str = stop_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    return start_time_str, stop_time_str
