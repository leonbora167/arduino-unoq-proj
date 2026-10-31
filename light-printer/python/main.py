import random
import time

from arduino.app_utils import App, Bridge, Leds

print("Starting light-printer app with DL-ready matrix and 4 RGB LEDs...")


# --- Helper functions for controlling LEDs ---

def set_led1(r: int, g: int, b: int):
    """Controls LED 1 (Linux/MPU side near USB-C). Values: 1 (on) or 0 (off)."""
    Leds.set_led1_color(r, g, b)


def set_led2(r: int, g: int, b: int):
    """Controls LED 2 (Linux/MPU side). Values: 1 (on) or 0 (off)."""
    Leds.set_led2_color(r, g, b)


def set_led3(r: int, g: int, b: int):
    """Controls LED 3 (MCU side) with PWM analog color mixing. Values: 0 to 255."""
    Bridge.call("set_led3_color", r, g, b)


def set_led4(r: bool, g: bool, b: bool):
    """Controls LED 4 (MCU side) digital on/off. Values: True or False."""
    Bridge.call("set_led4_color", r, g, b)


# --- Helper functions for the 8x13 LED matrix ---

def generate_random_matrix(rows: int = 8, cols: int = 13) -> list[int]:
    """
    Generates a random 8x13 matrix of brightness values (0 to 7).
    In your DL/CV scripts, you can replace this with your model's outputs
    (e.g., predicted class, heatmap, or detected feature map).
    """
    return [random.randint(0, 7) for _ in range(rows * cols)]


def display_matrix(pattern: list[int] | bytes):
    """Sends an 8x13 pattern (104 elements) to the microcontroller matrix."""
    Bridge.call("set_frame", bytes(pattern))


def clear_matrix():
    """Turns off all LEDs on the matrix."""
    Bridge.call("clear_matrix")


# --- Main Application Loop ---

def loop():
    """
    Called repeatedly by the App framework.
    Demonstrates:
    - Setting the 3 remaining RGB LEDs (Purple, Light Green, Orange)
    - Generating & displaying random 8x13 matrix patterns
    """
    # 1. Set the remaining 3 RGB LEDs:
    # LED 2 (MPU): Purple (Red + Blue)
    set_led2(1, 0, 1)

    # LED 3 (MCU PWM): Orange (Red=255, Green=60, Blue=0)
    set_led3(255, 60, 0)

    # LED 4 (MCU Digital): Light Green (Green ON)
    set_led4(False, True, False)

    # LED 1 indicates status: Green while displaying pattern
    set_led1(0, 1, 0)

    # 2. Generate and display random 8x13 matrix (simulates DL model output)
    matrix_output = generate_random_matrix()
    display_matrix(matrix_output)
    time.sleep(2)

    # 3. Clear matrix and set LED 1 to Red to indicate refresh interval
    clear_matrix()
    set_led1(1, 0, 0)
    time.sleep(1)


if __name__ == "__main__":
    App.run(user_loop=loop)
