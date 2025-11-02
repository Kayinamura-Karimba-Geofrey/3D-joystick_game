import serial
import time

# Replace with your HC-05 COM port (e.g., "COM5")
BT_PORT = "COM5"
BAUD_RATE = 9600

try:
    bt = serial.Serial(BT_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {BT_PORT}")
    time.sleep(2)

    while True:
        line = bt.readline().decode('utf-8').strip()
        if line:
            try:
                pitch, roll = map(float, line.split(','))
                print(f"Pitch: {pitch:.2f}, Roll: {roll:.2f}")

                # ---- Example game control section ----
                # You can map pitch/roll to control keys or 3D rotations
                # For example:
                # if pitch > 20: move_forward()
                # if roll > 20: turn_right()
                # if roll < -20: turn_left()
                # etc.
                # --------------------------------------

            except ValueError:
                pass

except serial.SerialException:
    print(f"Could not connect to {BT_PORT}. Check pairing and power.")
