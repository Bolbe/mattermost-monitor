import serial
import time
import sys
import os

# Adjust port name!
# Windows: 'COM3'
# Linux: '/dev/ttyACM0'
# macOS: '/dev/tty.usbmodemXXXX'

port = ''
if len(sys.argv) > 1:
    port = sys.argv[1]

if not port:
    for filename in os.listdir('/dev'):
        if ('usbmodem' in filename) or ('ttyACM' in filename) or ('ttyUSB' in filename) or ('COM' in filename):
            port = f'/dev/{filename}'
            break

print(f"Opening serial port {port}")
ser = serial.Serial(port, 115200, timeout=1)
print("Opened.")

while True:
    # Ask the user to press a key to trigger the pico
    print("Press a key to trigger the pico...")
    input()
    print("Sending 0x40")
    ser.write(b'A')  # send raw bytes
    print("Sent.")
