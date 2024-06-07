import glob
import os

from weather_database import WeatherDatabase


def read_ds18b20():
    """
    Odczytuje temperaturę z DS18B20.

    Funkcja ta lokalizuje plik danych czujnika DS18B20 w systemie plików,
    odczytuje temperaturę, a następnie zapisuje odczytane dane do bazy danych.

    Returns:
    - temperature: Wartość temperatury w stopniach Celsjusza. Jeśli odczyt się nie powiedzie, zwraca None.
    """
    # Ścieżka do folderu zawierającego pliki danych DS18B20
    sensor_folder = "/sys/bus/w1/devices/"

    # Wyszukanie pliku zawierającego dane DS18B20
    try:
        sensor_file = glob.glob(sensor_folder + "28*")[0] + "/w1_slave"
    except IndexError:
        print("Nie znaleziono pliku danych dla czujnika DS18B20.")
        return None

    # Odczyt danych z pliku
    try:
        with open(sensor_file, "r") as file:
            lines = file.readlines()
            # Sprawdzenie, czy odczytano poprawnie dane
            if lines[0].strip()[-3:] == "YES":
                # Wyciągnięcie surowych danych temperatury
                temperature_raw = lines[1].split("=")[-1]
                # Konwersja surowych danych na stopnie Celsjusza
                temperature_celsius = float(temperature_raw) / 1000.0

                # Zapisz odczytaną temperaturę do bazy danych
                weather_db = WeatherDatabase()
                weather_db.insert_data(
                    temperature_celsius, None, None, None, None, None
                )

                return temperature_celsius
            else:
                print("Błąd odczytu danych z czujnika DS18B20.")
                return None
    except FileNotFoundError:
        print(f"Nie znaleziono pliku {sensor_file}.")
        return None
    except Exception as e:
        print("Wystąpił błąd podczas odczytu czujnika DS18B20:", e)
        return None
