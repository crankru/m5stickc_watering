from m5stack import *
from m5ui import *
from uiflow import *
from machine import I2C
from m5stack import lcd
import utime
import time
import machine
import json
import usocket as socket
import struct

from libs.PCF8574 import PCF8574

# import upip
# upip.install("micropython-pystone_lowmem")

lcd.orient(lcd.LANDSCAPE)
# title0 = M5Title(title='Watering', x=4 , fgcolor=0xFFFFFF, bgcolor=0x0000FF)

def log(text):
  lcd.print(text)

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        import wifiCfg
        wifiCfg.autoConnect(lcdShow=True)
        # wifiCfg.autoConnect()

        # print('connecting to network...')
        # wlan.connect('essid', 'password')
        if not wlan.isconnected():
            log('Cant not connect to wlan')

    
    lcd.clear()
    # print('network config:', wlan.ifconfig())

class Clock:
    def __init__(self):
        self.rtc = machine.RTC()

        do_connect()
        dt = utime.localtime(self.get_datetime())
        self.rtc.datetime((dt[0], dt[1], dt[2], dt[6] + 1, dt[3], dt[4], dt[5], 0))

        self.show()
        t = machine.Timer(0)
        t.init(period=1000, mode=t.PERIODIC, callback=lambda t: self.show())

    def get_datetime(self):
        NTP_DELTA = 3155673600 - (60 * 60 * 3)
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1B
        addr = socket.getaddrinfo('pool.ntp.org', 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.settimeout(1)
            res = s.sendto(NTP_QUERY, addr)
            msg = s.recv(48)
        finally:
            s.close()

        val = struct.unpack("!I", msg[40:44])[0]
        return val - NTP_DELTA

    def get_date(self, dt=None):
        d = self.rtc.datetime()
        return '%02d.%02d.%02s' % (d[2], d[1], str(d[0])[2:])

    def get_time(self, dt=None):
        d = self.rtc.datetime()
        return '%02d:%02d:%02d' % (d[4], d[5], d[6])

    def show(self):
        size = lcd.screensize()
        # log(json.dumps(s))
        lcd.line(0, 15, size[0], 15)
        date = self.get_date()
        time = self.get_time()
        lcd.font(lcd.FONT_Small)
        lcd.print(date + ' ' + time, 4, 0)
        lcd.font(lcd.FONT_Default)
        # lcd.print('%s' % date, 0, 0)
        # log(json.dumps(self.rtc.datetime()))


class Menu:
    def __init__(self):
        self.print_status()

    def print_status(self):
        font_size = lcd.fontSize()
        lcd.print('Watering: ON', 4, 20)
        lcd.print('Interval: 60m', 4, 20 + font_size[0])
        lcd.print('Duration: 10s', 4, 20 + font_size[0] * 2)

    def print_menu(self):
        # lcd.print()
        pass

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

def buttonA_wasPressed():
  start_watering()
  
def buttonB_wasPressed():
  stop_watering()

# while True:
#     log(json.dumps(rtc.datetime()))
#     time.sleep(1)

# t1 = machine.Timer(0)
# t1.init(period=INTERVAL, mode=t1.PERIODIC, callback=start_watering)
  
# btnA.wasPressed(buttonA_wasPressed)
# btnB.wasPressed(buttonB_wasPressed)

clock = Clock()
menu = Menu()

# if __name__ == '__main__':
#     clock = Clock()