import glob
import os


def read_ds18b20():
    """
    Read temperature from DS18B20 sensor.

    Returns:
    - temperature: Temperature value in Celsius.
    """
    # Ścieżka do folderu zawierającego pliki danych DS18B20
    sensor_folder = "/sys/bus/w1/devices/"

    # Wyszukanie pliku zawierającego dane DS18B20
    sensor_file = glob.glob(sensor_folder + "28*")[0] + "/w1_slave"

    # Odczyt danych z pliku
    try:
        with open(sensor_file, "r") as file:
            lines = file.readlines()
            # Sprawdzenie, czy odczytano poprawnie dane
            if lines[0].strip()[-3:] == "YES":
                # Wyciągnięcie temperatury z danych
                temperature_raw = lines[1].split("=")[-1]
                temperature_celsius = float(temperature_raw) / 1000.0
                return temperature_celsius
            else:
                return None
    except Exception as e:
        print("Error reading DS18B20 sensor:", e)
        return None
