import math
import time

from weather_database import WeatherDatabase


def write_byte(bus, address, adr, value):
    """
    Procedura zapisu danych do określonego adresu na magistrali I2C.

    Args:
    - bus: Obiekt magistrali I2C.
    - address: Adres urządzenia na magistrali I2C.
    - adr: Adres rejestru, do którego mają być zapisane dane.
    - value: Dane do zapisania w rejestrze.
    """
    bus.write_byte_data(address, adr, value)


def median(lst):
    """
    Oblicza medianę z listy odczytów.

    Args:
    - lst: Lista odczytów.

    Returns:
    - Mediana z listy.
    """
    sorted_lst = sorted(lst)
    length = len(lst)
    if length < 1:
        return None
    elif length % 2 == 1:
        return sorted_lst[length // 2]
    else:
        return (sorted_lst[length // 2 - 1] + sorted_lst[length // 2]) / 2.0


def get_heading(read_word_2c, x_offset, y_offset, scale):
    """
    Oblicza kierunek wiatru w stopniach.

    Args:
    - read_word_2c: Funkcja do odczytu słowa z określonego adresu urządzenia I2C.
    - x_offset: Wartość offsetu dla osi x.
    - y_offset: Wartość offsetu dla osi y.
    - scale: Współczynnik skalowania.

    Returns:
    - Kierunek wiatru w stopniach od 0 do 359.
    """
    x_out = (read_word_2c(0x1E, 3) - x_offset) * scale
    y_out = (read_word_2c(0x1E, 7) - y_offset) * scale
    z_out = (read_word_2c(0x1E, 5)) * scale
    bearing = math.atan2(y_out, x_out)
    if bearing < 0:
        bearing += 2 * math.pi
    if (math.degrees(bearing) + 90) < 360 and (math.degrees(bearing) + 90) > 90:
        heading = math.degrees(bearing) + 90
    elif math.degrees(bearing) + 90 == 360:
        heading = 0
    else:
        heading = math.degrees(bearing) - 270
    return heading


def read_and_smooth_direction(bus, read_word_2c, x_offset, y_offset, scale):
    """
    Odczytuje kierunek wiatru.

    Args:
    - bus: Obiekt magistrali I2C.
    - read_word_2c: Funkcja do odczytu słowa z określonego adresu urządzenia I2C.
    - x_offset: Wartość offsetu dla osi x.
    - y_offset: Wartość offsetu dla osi y.
    - scale: Współczynnik skalowania.

    Returns:
    - Wygładzony kierunek wiatru w stopniach.
    """
    readings = []
    for _ in range(500):
        readings.append(get_heading(read_word_2c, x_offset, y_offset, scale))
        time.sleep(0.01)
    direction = median(readings)

    # Zapisz odczytany kierunek wiatru do bazy danych
    weather_db = WeatherDatabase()
    weather_db.insert_data(None, None, None, None, direction, None)

    return direction
