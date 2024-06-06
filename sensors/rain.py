import RPi.GPIO as GPIO
from weather_database import WeatherDatabase


def setup_yl83(pin):
    """
    Konfiguruje czujnik deszczu YL-83.

    Args:
    - pin: Pin GPIO podłączony do czujnika YL-83.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)


def read_yl83(pin):
    """
    Odczytuje status czujnika deszczu YL-83.

    Args:
    - pin: Pin GPIO podłączony do czujnika YL-83.

    Returns:
    - is_raining: True jeśli wykryto deszcz, False w przeciwnym razie.
    """
    is_raining = GPIO.input(pin) == GPIO.HIGH

    # Zapisz status opadów do bazy danych
    weather_db = WeatherDatabase()
    weather_db.insert_data(None, None, None, None, None, int(is_raining))

    return is_raining
