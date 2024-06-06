import Adafruit_DHT
from weather_database import WeatherDatabase


def read_dht(sensor, pin):
    """
    Read temperature and humidity from DHT sensor.

    Args:
    - sensor: Sensor type, either Adafruit_DHT.DHT11 or Adafruit_DHT.DHT22.
    - pin: GPIO pin connected to the sensor.

    Returns:
    - temperature: Temperature value in Celsius.
    - humidity: Humidity value in percentage.
    """
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Zapisz odczytane dane do bazy danych
    if humidity is not None and temperature is not None:
        weather_db = WeatherDatabase()
        weather_db.insert_data(temperature, humidity, None, None, None, None)

    return temperature, humidity
