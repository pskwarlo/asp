import time

import RPi.GPIO as GPIO
from weather_database import WeatherDatabase


def setup_anemometer(pin):
    """
    Konfiguruje czujnik anemometru.

    Args:
    - pin: Pin GPIO podłączony do czujnika anemometru.
    """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.IN)


def measure_wind_speed(pin, diameter_mm=106, inefficiency_factor=2.5, duration=10):
    """
    Mierzy prędkość wiatru za pomocą czujnika anemometru.

    Args:
    - pin: Pin GPIO podłączony do czujnika.
    - diameter_mm: Średnica łopatek anemometru w milimetrach. Domyślnie 106 mm.
    - inefficiency_factor: Współczynnik anemometru uwzględniający nieefektywność. Domyślnie 2.5.
    - duration: Czas trwania pomiaru w sekundach. Domyślnie 10 sekund.

    Returns:
    - windspeed_mps: Prędkość wiatru w metrach na sekundę.
    """
    # Oblicz obwód łopatki anemometru w metrach
    vane_circ = diameter_mm / 1000 * 3.1415

    # Rozpocznij pomiar prędkości wiatru
    print("Measuring wind speed...")

    rotations = 0
    trigger = 0
    endtime = time.time() + duration
    sensorstart = GPIO.input(pin)

    while time.time() < endtime:
        if GPIO.input(pin) == 1 and trigger == 0:
            rotations += 1
            trigger = 1
        if GPIO.input(pin) == 0:
            trigger = 0
        time.sleep(0.001)

    # Dostosuj wartość obrotów, jeśli to konieczne
    if rotations == 1 and sensorstart == 1:
        rotations = 0

    # Oblicz prędkość wiatru
    rots_per_second = rotations / duration
    windspeed_mps = rots_per_second * vane_circ * inefficiency_factor

    # Zapisz odczytaną prędkość wiatru do bazy danych
    weather_db = WeatherDatabase()
    weather_db.insert_data(None, None, None, windspeed_mps, None, None)

    return windspeed_mps
