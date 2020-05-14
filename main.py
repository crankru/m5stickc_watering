from m5stack import *
# from m5ui import *
# from uiflow import *
from m5stack import lcd
import time
import machine

from libs.clock import Clock
from libs.menu import Menu

# import upip
# upip.install("micropython-pystone_lowmem")

lcd.orient(lcd.LANDSCAPE)
# title0 = M5Title(title='Watering', x=4 , fgcolor=0xFFFFFF, bgcolor=0x0000FF)

clock = Clock()
menu = Menu(clock)

# if __name__ == '__main__':
#     print(__name__)