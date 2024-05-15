import math
import time

from weather_database import WeatherDatabase


def write_byte(bus, address, adr, value):
    """
    Procedure to write data to a specific address on the I2C bus.

    Args:
    - bus: I2C bus object.
    - address: Address of the device on the I2C bus.
    - adr: Register address to write data to.
    - value: Data to write to the register.
    """
    bus.write_byte_data(address, adr, value)


def median(lst):
    """
    Calculate median of a list of readings.

    Args:
    - lst: List of readings.

    Returns:
    - Median value of the list.
    """
    sorted_lst = sorted(lst)
    length = len(lst)
    if length < 1:
        return None
    elif length % 2 == 1:
        return sorted_lst[length // 2]
    else:
        return (sorted_lst[length // 2 - 1] + sorted_lst[length // 2]) / 2.0


def get_heading(read_word_2c, x_offset, y_offset, scale):
    """
    Calculate heading of the vane in degrees.

    Args:
    - read_word_2c: Function to read word from a specific address of the I2C device.
    - x_offset: Offset value for x-axis.
    - y_offset: Offset value for y-axis.
    - scale: Scaling factor.

    Returns:
    - Heading of the vane in degrees from 0 to 359.
    """
    x_out = (read_word_2c(0x1E, 3) - x_offset) * scale
    y_out = (read_word_2c(0x1E, 7) - y_offset) * scale
    z_out = (read_word_2c(0x1E, 5)) * scale
    bearing = math.atan2(y_out, x_out)
    if bearing < 0:
        bearing += 2 * math.pi
    if (math.degrees(bearing) + 90) < 360 and (math.degrees(bearing) + 90) > 90:
        heading = math.degrees(bearing) + 90
    elif math.degrees(bearing) + 90 == 360:
        heading = 0
    else:
        heading = math.degrees(bearing) - 270
    return heading


def read_and_smooth_direction(bus, read_word_2c, x_offset, y_offset, scale):
    """
    Read wind direction and smooth the readings.

    Args:
    - bus: I2C bus object.
    - read_word_2c: Function to read word from a specific address of the I2C device.
    - x_offset: Offset value for x-axis.
    - y_offset: Offset value for y-axis.
    - scale: Scaling factor.

    Returns:
    - Smoothed wind direction in degrees.
    """
    readings = []
    for _ in range(500):
        readings.append(get_heading(read_word_2c, x_offset, y_offset, scale))
        time.sleep(0.01)
    direction = median(readings)

    # Zapisz odczytaną kierunek wiatru do bazy danych
    weather_db = WeatherDatabase()
    weather_db.insert_data(None, None, None, None, direction, None)

    return direction
