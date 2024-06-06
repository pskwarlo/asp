from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Import funkcji do odczytu danych z różnych czujników pogodowych
from sensors.pressure import read_bmp
from sensors.rain import read_yl83
from sensors.temp import read_dht
from sensors.windDir import read_heading
from sensors.windSpeed import measure_wind_speed


class WeatherData(BaseModel):
    """
    Model danych pogodowych wykorzystujący Pydantic do walidacji.

    Atrybuty:
    - temperature (Optional[float]): Temperatura w stopniach Celsjusza.
    - humidity (Optional[float]): Wilgotność w procentach.
    - pressure (Optional[float]): Ciśnienie w hPa.
    - wind_speed (Optional[float]): Prędkość wiatru w metrach na sekundę.
    - wind_direction (Optional[float]): Kierunek wiatru w stopniach.
    - rainfall (Optional[bool]): Czy pada deszcz (True/False).
    """

    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[float] = None
    rainfall: Optional[bool] = None


@app.get("/weather")
def get_weather_data():
    """
    Endpoint do pobierania danych pogodowych.

    Funkcja ta odczytuje dane z różnych czujników pogodowych i zwraca je
    w formacie JSON jako instancję klasy WeatherData.

    Returns:
    - weather_data (WeatherData): Dane pogodowe zawierające odczyty z różnych czujników.
    """
    # Odczyt danych z czujników
    temperature, humidity = read_dht()
    pressure = read_bmp()
    wind_direction = read_heading()
    rainfall = read_yl83()
    wind_speed = measure_wind_speed()

    # Formatowanie danych
    weather_data = WeatherData(
        temperature=temperature,
        humidity=humidity,
        pressure=pressure,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        rainfall=rainfall,
    )

    return weather_data
