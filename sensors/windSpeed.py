import time

import RPi.GPIO as GPIO


def setup_anemometer(pin):
    """
    Setup anemometer sensor.

    Args:
    - pin: GPIO pin connected to the anemometer sensor.
    """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.IN)


def measure_wind_speed(pin, diameter_mm=106, inefficiency_factor=2.5, duration=10):
    """
    Measure wind speed using anemometer sensor.

    Args:
    - pin: GPIO pin connected to the anemometer sensor.
    - diameter_mm: Diameter of the anemometer vane in millimeters.
    - inefficiency_factor: Anemometer factor to account for inefficiency.
    - duration: Duration of measurement in seconds.

    Returns:
    - windspeed_mps: Wind speed in meters per second.
    """
    # Calculate vane circumference in meters
    vane_circ = diameter_mm / 1000 * 3.1415

    # Start measuring wind speed
    print("Measuring wind speed...")

    rotations = 0
    trigger = 0
    endtime = time.time() + duration
    sensorstart = GPIO.input(pin)

    while time.time() < endtime:
        if GPIO.input(pin) == 1 and trigger == 0:
            rotations += 1
            trigger = 1
        if GPIO.input(pin) == 0:
            trigger = 0
        time.sleep(0.001)

    # Adjust rotations value if needed
    if rotations == 1 and sensorstart == 1:
        rotations = 0

    # Calculate wind speed
    rots_per_second = rotations / duration
    windspeed_mps = rots_per_second * vane_circ * inefficiency_factor

    return windspeed_mps
