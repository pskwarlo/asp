import sqlite3
import time


class WeatherDatabase:
    def __init__(self, db_file="weather_data.db"):
        self.db_file = db_file
        self.create_table()

    def create_table(self):
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
