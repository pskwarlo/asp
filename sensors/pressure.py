import Adafruit_DHT
from weather_database import WeatherDatabase


def read_dht(sensor, pin):
    """
    @brief Odczytuje temperaturę i wilgotność z czujnika DHT.

    Funkcja ta odczytuje dane z czujnika DHT, zapisuje je do bazy danych,
    a następnie zwraca odczytane wartości temperatury i wilgotności.

    @param sensor Typ czujnika, może być Adafruit_DHT.DHT11 lub Adafruit_DHT.DHT22.
    @param pin Pin GPIO podłączony do czujnika.

    @returns
    @retval temperature Wartość temperatury w stopniach Celsjusza.
    @retval humidity Wartość wilgotności w procentach.
    """
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Zapisz odczytane dane do bazy danych, jeśli są dostępne
    if humidity is not None and temperature is not None:
        weather_db = WeatherDatabase()
        weather_db.insert_data(temperature, humidity, None, None, None, None)

    return temperature, humidity
