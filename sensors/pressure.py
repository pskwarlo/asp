import Adafruit_DHT


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
    if humidity is not None and temperature is not None:
        return temperature, humidity
    else:
        return None, None
