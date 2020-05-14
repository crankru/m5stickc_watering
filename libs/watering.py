from m5stack import *
import machine
from machine import I2C

from libs.PCF8574 import PCF8574

class Watering:
    interval = None
    duration = None

    def __init__(self, interval, duration):
        i2c = I2C(freq=400000, sda=32, scl=33)
        # dev = i2c.scan()
        # print(dev)
        self.pcf = PCF8574(i2c, 32)
        self.set_interval(interval)
        self.set_duration(duration)

    def set_interval(self, value):
        self.interval = value

    def set_duration(self, value):
        self.duration = value

    def start(self):
        M5Led.on()
        self.pcf.pin(0, False)
        t = machine.Timer(1)
        t.init(period=self.duration, mode=t.ONE_SHOT, callback=self.stop)

    def stop(self):
        M5Led.off()
        self.pcf.pin(0, True)


# t1 = machine.Timer(0)
# t1.init(period=INTERVAL, mode=t1.PERIODIC, callback=start_watering)