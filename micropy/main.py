
import machine
import esp
import time


pin = machine.Pin(2, machine.Pin.OUT)

while True:
    pin.on()
    time.sleep(1)
    pin.off()
    time.sleep(1)
