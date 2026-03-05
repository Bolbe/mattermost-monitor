import sys
import time
import machine

pico_led = machine.Pin("LED", machine.Pin.OUT)
pico_led.on()
time.sleep(2)  # give USB time to connect
pico_led.off()

gyro = machine.Pin(15, machine.Pin.OUT)
gyro.off()

button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    c = sys.stdin.buffer.read(1)
    gyro.on()
    while button.value()!=0:
        time.sleep(0.2)
    gyro.off()
    