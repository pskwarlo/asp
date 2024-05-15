from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

from sensors.pressure import read_bmp
from sensors.rain import read_yl83

# Import funkcji do odczytu danych pogodowych
from sensors.temp import read_dht
from sensors.windDir import read_heading
from sensors.windSpeed import measure_wind_speed


class WeatherData(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[float] = None
    rainfall: Optional[bool] = None


@app.get("/weather")
def get_weather_data():
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
