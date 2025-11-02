import serial
import socket
import time

BT_PORT = "COM5"       # <-- change this to your HC-05 port
BAUD = 9600
UNITY_HOST = "127.0.0.1"
UNITY_PORT = 5055       # must match Unity side

# --- Bluetooth connection ---
bt = serial.Serial(BT_PORT, BAUD, timeout=1)
print(f"[OK] Connected to {BT_PORT}")
time.sleep(2)

# --- TCP socket to Unity ---
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((UNITY_HOST, UNITY_PORT))
s.listen(1)
print("[WAIT] Unity connecting...")

conn, addr = s.accept()
print(f"[CONNECTED] Unity: {addr}")

try:
    while True:
        line = bt.readline().decode('utf-8').strip()
        if line:
            try:
                pitch, roll = map(float, line.split(','))
                msg = f"{pitch:.2f},{roll:.2f}\n"
                conn.sendall(msg.encode('utf-8'))
            except:
                pass
except KeyboardInterrupt:
    pass
finally:
    conn.close()
    s.close()
    bt.close()
