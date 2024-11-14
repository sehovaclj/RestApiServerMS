import pytest
from datetime import datetime, timedelta, timezone
from src.utils.datetime_utils import utc_now_timestamp, parse_relative_time, \
    calculate_start_stop_times


@pytest.mark.datetime_utils
def test_utc_now_timestamp():
    # Get the current timestamp
    timestamp = utc_now_timestamp()

    # Assert that the timestamp is an integer
    assert isinstance(timestamp, int), "The timestamp should be an integer."

    # Assert that the timestamp is close to the current UTC time
    current_timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
    tolerance = 1000  # 1 second tolerance in milliseconds
    assert abs(
        current_timestamp - timestamp) < tolerance, \
        "The timestamp should be close to the current UTC time."


@pytest.mark.datetime_utils
@pytest.mark.parametrize("time_str, expected_timedelta", [
    ("-5s", timedelta(seconds=5)),
    ("-10m", timedelta(minutes=10)),
    ("-2h", timedelta(hours=2)),
    ("-3d", timedelta(days=3)),
    ("-1w", timedelta(weeks=1)),
    ("-1mo", timedelta(days=30)),  # Approximate month
    ("-1y", timedelta(days=365)),  # Approximate year
    ("-500ms", timedelta(milliseconds=500)),
])
def test_parse_relative_time(time_str, expected_timedelta):
    # Assert that the parsed timedelta matches the expected value
    result = parse_relative_time(time_str)
    assert result == expected_timedelta, \
        f"Expected {expected_timedelta} for '{time_str}', got {result}"


@pytest.mark.datetime_utils
def test_parse_relative_time_invalid():
    # Assert that an invalid time unit raises a ValueError
    with pytest.raises(ValueError, match="Unsupported time unit"):
        parse_relative_time("-10x")


@pytest.mark.datetime_utils
def test_calculate_start_stop_times():
    # Test with known relative start and stop ranges
    start_range = "-2h"  # 2 hours ago
    stop_range = "-1m"  # 1 minute ago

    # Get the calculated start and stop times as RFC3339Nano strings
    start_time_str, stop_time_str = calculate_start_stop_times(start_range,
                                                               stop_range)

    # Convert the expected start and stop times to datetime for comparison
    now = datetime.now(timezone.utc)
    expected_start_time = now - timedelta(hours=2)
    expected_stop_time = now - timedelta(minutes=1)

    # Parse the RFC3339Nano strings back to datetime objects and make them
    # timezone-aware
    start_time_dt = datetime.strptime(start_time_str,
                                      "%Y-%m-%dT%H:%M:%S.%fZ").replace(
        tzinfo=timezone.utc)
    stop_time_dt = datetime.strptime(stop_time_str,
                                     "%Y-%m-%dT%H:%M:%S.%fZ").replace(
        tzinfo=timezone.utc)

    # Assert that the calculated times are within a 1-second tolerance
    tolerance = timedelta(seconds=1)
    assert abs(start_time_dt - expected_start_time) < tolerance, \
        (
            f"Expected start time close to {expected_start_time}, "
            f"got {start_time_dt}")
    assert abs(stop_time_dt - expected_stop_time) < tolerance, \
        (
            f"Expected stop time close to {expected_stop_time},"
            f" got {stop_time_dt}")
