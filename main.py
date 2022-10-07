import time
from machine import Pin
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY

import secrets
import network
import urequests

# Initialize hardware components
led = Pin("LED", Pin.OUT, value=0)

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=0)
WIDTH, HEIGHT = display.get_bounds()
display.set_backlight(1.0)
display.set_font("serif")

wlan = network.WLAN(network.STA_IF)

def connect_to_network():
    wlan.active(True)
    wlan.config(pm = 0xa11140)  # Disable power-save mode
    wlan.connect(secrets.SSID, secrets.PASSWORD)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])

def get_web_time(zone, city):
    WD =[ "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" ]
    
    web_time = urequests.get("http://worldtimeapi.org/api/timezone/{z}/{c}".format(z=zone, c=city)).json()
    dt = web_time['datetime']
    new_datetime = '{h:02d}:{m:02d}:{s:02d},{day},{Y:04d}-{M:02d}-{D:02d}'.format(h=int(dt[11]+dt[12]), m=int(dt[14]+dt[15]), s=int(dt[17]+dt[18]), day=WD[int(web_time['day_of_week'])], Y=int(dt[0]+dt[1]+dt[2]+dt[3]), M=int(dt[5]+dt[6]), D=int(dt[8]+dt[9]))

    return new_datetime

def display_datetime(year, month, day, hour, minute, second):
    # Clear datetime
    display.set_pen(0)
    display.rectangle(0, 0, WIDTH, 10)

    # Display current datetime
    display.set_pen(255)
    date_time = "{Y:02d}-{M:02d}-{D:02d}  {H:02d}:{m:02d}:{s:02d}".format(Y=year % 100, M=month, D=day, H=hour, m=minute, s=second)
    display.text(date_time, 47, 5, scale=0.5)

    display.update()

class GRID:
    def __init__(self, display_width, display_height, rows, columns, dX, dY):
        self.rows = rows
        self.columns = columns
        self.dX = dX
        self.dY = dY
        self.width = self.columns * self.dX
        self.height = self.rows * self.dY
        self.x0 = int((display_width - self.width) / 2)
        self.y0 = int((display_height - self.height) / 2) + 7
        self.xMax = self.x0 + self.width
        self.yMax = self.y0 + self.height
    
def draw_grid(grid):
    display.set_pen(255) # White
    # draw vertical lines
    for i in range(grid.columns + 1):
        x = grid.x0 + i*grid.dX
        display.line(x, grid.y0, x, grid.yMax)

    # draw horizontal lines
    for i in range(grid.rows + 1):
        y = grid.y0 + i*grid.dY
        display.line(grid.x0, y, grid.xMax, y)

    # draw horizontal labels
    labels = ['Y','M', 'D', 'H', 'm', 's']
    for i in range(grid.columns-1):
        display.text(labels[i], grid.x0 + (i+1)*grid.dX + 10, grid.y0 + 8, scale = 0.5)

    # draw vertical labels    
    labels = ['32', '16', '08', '04', '02', '01']
    for i in range(grid.rows-1):
        display.text(labels[i], grid.x0 + 6, grid.y0 + (i+1)*grid.dY + 8, scale = 0.5)

def draw_clock(grid, year, month, day, hours, minutes, seconds):
    def draw_elipse(digit, x, y):
        if digit == '1':
            display.circle(x-1, y, 5)
            display.circle(x+1, y, 5)

    # clear elipsies
    display.set_pen(0) # Black
    for i in range(1, grid.columns):
        for j in range(1, grid.rows):
            x = grid.x0 + i*grid.dX + int(grid.dX/2)
            y = grid.y0 + j*grid.dY + int(grid.dY/2)
            draw_elipse('1', x, y)

    # calc binary strings
    year_str    = "{Y:06b}".format(Y=year % 100) # 2 digit year
    month_str   = "{M:06b}".format(M=month)
    day_str     = "{D:06b}".format(D=day)
    hours_str   = "{H:06b}".format(H=hours)
    minutes_str = "{m:06b}".format(m=minutes)
    seconds_str = "{s:06b}".format(s=seconds)
    #print(year_str month_str day_str hours_str minutes_str seconds_str)

    # draw elipsies
    display.set_pen(60) # Green
    for column in range(1, grid.columns):
        for row in reversed(range(grid.rows-1)):
            x = grid.x0 + column*grid.dX + int(grid.dX/2)
            y = grid.y0 + (row+1)*grid.dY + int(grid.dY/2)
            if (column == 6): # Seconds
                draw_elipse(seconds_str[row], x, y)
            elif (column == 5): # Minutes
                draw_elipse(minutes_str[row], x, y)
            elif (column == 4): # Hours
                draw_elipse(hours_str[row], x, y)
            elif (column == 3): # Day
                draw_elipse(day_str[row], x, y)
            elif (column == 2): # Month
                draw_elipse(month_str[row], x, y)
            elif (column == 1): # Seconds
                draw_elipse(year_str[row], x, y)

    display.update()

def get_local_time(current_time):
    the_time = current_time[0:19]
    dt = the_time.split(' ')
    date = dt[0].split('-')
    tm = dt[1].split(':')
    
    return(int(date[0]), int(date[1]), int(date[2]), int(tm[0]), int(tm[1]), int(tm[2]), 0, 0)

def print_date_time(year, month, day, hour, minute, second):
    date_time = "{Y:04d}-{M:02d}-{D:02d} {H:02d}:{m:02d}:{s:02d}".format(Y=year, M=month, D=day, H=hour, m=minute, s=second)
    print(date_time)

def main():
    from ds3231 import ds3231, I2C_PORT, I2C_SCL, I2C_SDA
    
    rtc = ds3231(I2C_PORT, I2C_SCL, I2C_SDA)

    led.on()
    
    try:
        # Try to get current time from intenet
        connect_to_network()
        web_time = get_web_time('Europe', 'London') # Change this to correct location

        print('Setting time to %s' % web_time)
        rtc.set_time(web_time)
        #current_time = rtc.read_time()
        #print('Current time is %s' % current_time)
    except:
        print('Can''t get time from Internet')

    # draw grid amd labels
    grid = GRID(WIDTH, HEIGHT, 7, 7, 30, 15)
    draw_grid(grid)
    
    while True:
        led.on()
        (year, month, day, hour, minute, second, wday, yday) = get_local_time(rtc.read_time())
        display_datetime(year, month, day, hour, minute, second)
        draw_clock(grid, year, month, day, hour, minute, second)

        time.sleep(0.4)
        led.off()
        time.sleep(0.5)

main()