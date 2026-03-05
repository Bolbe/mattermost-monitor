import serial
import time
import sys

# Adjust port name!
# Windows: 'COM3'
# Linux: '/dev/ttyACM0'
# macOS: '/dev/tty.usbmodemXXXX'
port = '/dev/tty.usbmodem311401'  # Change this to your Pico's serial port
if len(sys.argv) > 1:
    port = sys.argv[1]
print(f"Opening serial port {port}")
ser = serial.Serial(port, 115200, timeout=1)
print("Opened.")

while True:
    # Ask the user to press a key to trigger the pico
    print("Press a key to trigger the pico...")
    input()
    print("Sending \x65...")
    ser.write(b'\x65')  # send raw bytes
    print("Sent.")
