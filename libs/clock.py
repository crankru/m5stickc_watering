from m5stack import lcd
import machine
import usocket as socket
import struct
import utime

class Clock:
    def __init__(self):
        self.rtc = machine.RTC()

        self.do_connect()
        dt = utime.localtime(self.get_datetime())
        self.rtc.datetime((dt[0], dt[1], dt[2], dt[6] + 1, dt[3], dt[4], dt[5], 0))

        self.show()
        t = machine.Timer(0)
        t.init(period=1000, mode=t.PERIODIC, callback=lambda t: self.show())

    def do_connect(self):
        import network
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            import wifiCfg
            wifiCfg.autoConnect(lcdShow=True)
            # wifiCfg.autoConnect()
            # wlan.connect('essid', 'password')
            if not wlan.isconnected():
                raise Exception('Cant not connect to wlan')
        
        lcd.clear()

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