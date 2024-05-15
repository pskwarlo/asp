import RPi.GPIO as GPIO
from weather_database import WeatherDatabase


def setup_yl83(pin):
    """
    Setup YL-83 rain sensor.

    Args:
    - pin: GPIO pin connected to the YL-83 sensor.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)


def read_yl83(pin):
    """
    Read status of YL-83 rain sensor.

    Args:
    - pin: GPIO pin connected to the YL-83 sensor.

    Returns:
    - is_raining: True if rain is detected, False otherwise.
    """
    is_raining = GPIO.input(pin) == GPIO.HIGH

    # Zapisz status opadów do bazy danych
    weather_db = WeatherDatabase()
    weather_db.insert_data(None, None, None, None, None, int(is_raining))

    return is_raining
