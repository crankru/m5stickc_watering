from m5stack import *
from m5stack import lcd

class Menu:
    def __init__(self):
        self.active = False
        self.interval = 60 # min
        self.duration = 10 # sec
        self.active_index = None
        self.print_menu()

        btnA.wasPressed(self.btnA)
        btnB.wasPressed(self.btnB)

    def print_cursor(self, i, active=True):
        top_padding = 20
        font_size = lcd.fontSize()

        x1, y1 = 5, top_padding + font_size[0] * i
        x2, y2 = 13, top_padding + font_size[0] * i + 4
        x3, y3 = 5, top_padding + font_size[0] * i + 8

        color = lcd.WHITE if active else lcd.BLACK
        lcd.triangle(x1, y1, x2, y2, x3, y3, color, color)

    def print_menu(self):
        top_padding = 20
        left_padding = 15
        font_size = lcd.fontSize()

        self.menu_items = [
            'Watering: %s' % self.active,
            'Interval: %dm' % self.interval,
            'Duration: %ds' % self.duration,
        ]

        lcd.clear()

        for i in range(len(self.menu_items)):
            item = self.menu_items[i]
            if i == self.active_index:
                self.print_cursor(i)
                lcd.print(item, left_padding, top_padding + font_size[0] * i)
            else:
                # self.print_cursor(i, False)
                lcd.print(item, left_padding, top_padding + font_size[0] * i)

    def toggleActive(self):
        self.active = not self.active
        self.print_menu()

    def toggleInterval(self):
        self.interval += 10
        if self.interval > 120:
            self.interval = 10

        self.print_menu()

    def toggleDuration(self):
        self.duration += 5
        if self.duration > 60:
            self.duration = 5

        self.print_menu()

    def btnA(self):
        if self.active_index == None:
            print('No item')
            return

        if self.active_index == 0:
            self.toggleActive()
        elif self.active_index == 1:
            self.toggleInterval()
        elif self.active_index == 2:
            self.toggleDuration()
        
        print('Selected %d' % self.active_index)
            

    def btnB(self):
        if self.active_index == None:
            self.active_index = 0
        else:
            self.active_index += 1
            if self.active_index >= len(self.menu_items):
                self.active_index = 0

        print(self.active_index)
        self.print_menu()
