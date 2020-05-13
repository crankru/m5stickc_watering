from m5stack import *
# from m5ui import *
# from uiflow import *
from machine import I2C
from m5stack import lcd
import time
import machine

from libs.PCF8574 import PCF8574
from libs.clock import Clock
from libs.menu import Menu

# import upip
# upip.install("micropython-pystone_lowmem")

lcd.orient(lcd.LANDSCAPE)
# title0 = M5Title(title='Watering', x=4 , fgcolor=0xFFFFFF, bgcolor=0x0000FF)

def log(text):
    lcd.print(text)

# I2C_HUB_ADDR = 32
# i2c = I2C(freq=400000, sda=32, scl=33)
# dev = i2c.scan()
# j = json.dumps(dev)
# log(j)
        
# PCF = PCF8574(i2c, I2C_HUB_ADDR)

def set_pin(pin, value):
  PCF.pin(0, value)

DURATION = 1000 * 10
INTERVAL = 1000 * 30 + DURATION

def start_watering(t=None):
  M5Led.on()
  set_pin(0, False)
  t = machine.Timer(1)
  t.init(period=DURATION, mode=t.ONE_SHOT, callback=stop_watering)
  
def stop_watering(t=None):
  M5Led.off()
  set_pin(0, True)

# while True:
#     log(json.dumps(rtc.datetime()))
#     time.sleep(1)

# t1 = machine.Timer(0)
# t1.init(period=INTERVAL, mode=t1.PERIODIC, callback=start_watering)

clock = Clock()
menu = Menu()

# if __name__ == '__main__':
#     clock = Clock()