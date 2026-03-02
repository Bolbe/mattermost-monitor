import sys
import time
import machine

pico_led = machine.Pin("LED", machine.Pin.OUT)
pico_led.on()
time.sleep(2)  # give USB time to connect
pico_led.off()

gyro = machine.Pin(16, machine.Pin.OUT)

while True:
    c = sys.stdin.buffer.read(1)
    gyro.value(1)
    for i in range(3):
        pico_led.on()
        time.sleep(0.25)
        pico_led.off()
        time.sleep(0.10)
    time.sleep(5)
    gyro.value(0)
    
        