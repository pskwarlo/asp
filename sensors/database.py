import sqlite3
import time


class WeatherDatabase:
    """
    Klasa do obsługi przechowywania danych pogodowych w bazie danych SQLite.

    Ta klasa udostępnia metody do tworzenia tabeli danych pogodowych oraz
    wstawiania danych pogodowych do bazy danych SQLite.

    Atrybuty:
        db_file (str): Nazwa pliku bazy danych SQLite.
    """

    def __init__(self, db_file="weather_data.db"):
        """
        Inicjalizuje klasę WeatherDatabase z podanym plikiem bazy danych.

        Args:
            db_file (str): Nazwa pliku bazy danych SQLite. Domyślnie "weather_data.db".
        """
        self.db_file = db_file
        self.create_table()

    def create_table(self):
        """
        Tworzy tabelę do przechowywania danych pogodowych, jeśli jeszcze nie istnieje.
        """
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS weather_data
                     (timestamp INTEGER, temperature REAL, humidity REAL, pressure REAL, wind_speed REAL, wind_direction REAL, rainfall INTEGER)"""
        )
        conn.commit()
        conn.close()

    def insert_data(
        self, temperature, humidity, pressure, wind_speed, wind_direction, rainfall
    ):
        """
        Wstawia dane pogodowe do tabeli weather_data.

        Args:
            temperature (float): Temperatura w stopniach Celsjusza.
            humidity (float): Wilgotność w procentach.
            pressure (float): Ciśnienie w hPa.
            wind_speed (float): Prędkość wiatru w m/s.
            wind_direction (float): Kierunek wiatru w stopniach.
            rainfall (int): Opady deszczu w mm.
        """
        timestamp = int(time.time())
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute(
            """INSERT INTO weather_data VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                timestamp,
                temperature,
                humidity,
                pressure,
                wind_speed,
                wind_direction,
                rainfall,
            ),
        )
        conn.commit()
        conn.close()
