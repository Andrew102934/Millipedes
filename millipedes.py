from gpiozero import Button, OutputDevice
from time import sleep, time
import board
import busio
import adafruit_vl53l0x

# -----------------------------
# Pin setup
# -----------------------------
BUTTON_PIN = 17       # push button input
UV_LIGHT_PIN = 27     # relay or MOSFET controlling UV lights

button = Button(BUTTON_PIN, pull_up=True)
uv_light = OutputDevice(UV_LIGHT_PIN)

# -----------------------------
# VL53L0X distance sensor setup
# -----------------------------
i2c = busio.I2C(board.SCL, board.SDA)
tof = adafruit_vl53l0x.VL53L0X(i2c)

# -----------------------------
# Settings
# -----------------------------
GLOW_TIME = 120            # UV lights stay on for 2 minutes
COOLDOWN_TIME = 30         # extra lockout after lights turn off
DETECTION_DISTANCE = 300   # millimeters (30 cm) - adjust as needed

lights_active = False
last_trigger_time = 0

# Make sure UV starts off
uv_light.off()

def visitor_detected():
    try:
        distance = tof.range
        print(f"Distance: {distance} mm")
        return distance <= DETECTION_DISTANCE
    except Exception as e:
        print("Sensor read error:", e)
        return False

def activate_uv():
    global lights_active, last_trigger_time

    current_time = time()

    # prevent spam presses while active or during cooldown
    if lights_active:
        print("UV lights already active.")
        return

    if current_time - last_trigger_time < COOLDOWN_TIME:
        print("System cooling down. Please wait.")
        return

    # only activate if someone is actually near the exhibit
    if not visitor_detected():
        print("No visitor close enough. UV not activated.")
        return

    print("Visitor detected. Turning on UV lights.")
    lights_active = True
    uv_light.on()

    sleep(GLOW_TIME)

    uv_light.off()
    lights_active = False
    last_trigger_time = time()
    print("UV lights turned off. Cooldown started.")

# -----------------------------
# Main loop
# -----------------------------
print("Millipede exhibit ready.")

while True:
    if button.is_pressed:
        print("Button pressed.")
        activate_uv()

        # wait until button is released so one press doesn't trigger multiple times
        while button.is_pressed:
            sleep(0.1)

    sleep(0.1)


"""1. Comments were very readable and easy to understand. This helped to reduce the cognitive load on me as I didn't have to think so hard on what your code is doing.

2. Clear and consistent variable names. Your variable names allow for clearer understanding and don't add any confusion when it comes to reading your code. 

3. There aren't really any excess functions or functions that are too complicated and complex. This helps to keep the simplicity and doesn't add cognitive load onto the reader
"""
