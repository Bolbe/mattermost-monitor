import serial
import time

# Adjust port name!
# Windows: 'COM3'
# Linux: '/dev/ttyACM0'
# macOS: '/dev/tty.usbmodemXXXX'
print("Opening serial port...")
ser = serial.Serial('/dev/tty.usbmodem311101', 115200, timeout=1)
print("Opened.")

while True:
    # Ask the user to press a key to trigger the pico
    print("Press a key to trigger the pico...")
    input()
    print("Sending \x65...")
    ser.write(b'\x65')  # send raw bytes
    print("Sent.")
