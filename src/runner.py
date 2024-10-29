import time
from machine import Pin

LED = 25
led = None

RELAYS = [20, 19, 18]
relays = []

SPEED_TEST = 17
speed_test = None

def init():
    global led, relays, speed_test
    print("init")
    led = Pin(LED, Pin.OUT)
    for r in RELAYS:
        relays.append(Pin(r, Pin.OUT))
        relays[-1].value(0)
    speed_test = Pin(SPEED_TEST, Pin.IN, Pin.PULL_UP)

def run():
    init()
