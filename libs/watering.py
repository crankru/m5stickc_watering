from m5stack import *
import machine
from machine import I2C

from libs.PCF8574 import PCF8574

class Watering:
    interval = None
    duration = None
    state = False
    active = False

    def __init__(self, interval, duration):
        i2c = I2C(freq=400000, sda=32, scl=33)
        # dev = i2c.scan()
        # print(dev)
        self.pcf = PCF8574(i2c, 32)
        self.set_interval(interval)
        self.set_duration(duration)

        self.init_pcf()

        # t1 = machine.Timer(1)
        # t1.init(period=INTERVAL, mode=t1.PERIODIC, callback=lambda t: self.start())

    def init_pcf(self):
        for p in range(8):
            self.pcf.pin(p, True)

    def set_interval(self, value):
        self.interval = value * 1000

    def set_duration(self, value):
        self.duration = value * 1000

    def start(self):
        M5Led.on()
        self.pcf.pin(0, False)
        self.state = True
        t = machine.Timer(2)
        t.init(period=self.duration, mode=t.ONE_SHOT, callback=lambda t: self.stop())

    def stop(self):
        M5Led.off()
        self.pcf.pin(0, True)
        self.state = False

    def toggle(self):
        if not self.state or self.state == False:
            self.start()
        else:
            self.stop()

    def active(self, state):
        self.active = state