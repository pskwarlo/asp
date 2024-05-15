import time

import RPi.GPIO as GPIO


def setup_yl83(pin):
    """
    Setup YL-83 rain sensor.

    Args:
    - pin: GPIO pin connected to the YL-83 sensor.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)


def read_yl83(pin):
    """
    Read status of YL-83 rain sensor.

    Args:
    - pin: GPIO pin connected to the YL-83 sensor.

    Returns:
    - is_raining: True if rain is detected, False otherwise.
    """
    if GPIO.input(pin) == GPIO.HIGH:
        return True
    else:
        return False
