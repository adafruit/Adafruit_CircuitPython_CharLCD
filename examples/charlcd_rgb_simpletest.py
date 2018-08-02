import time
from board import D3, D4, D5, D7, D8, D9, D10, D11, D12, D13
import digitalio
import adafruit_character_lcd
import pulseio

#   Character LCD Config:
#   modify this if you have a different sized charlcd
lcd_columns = 16
lcd_rows = 2

#   Metro m0 Pin Config:
lcd_rs = digitalio.DigitalInOut(D7)
lcd_en = digitalio.DigitalInOut(D8)
lcd_d7 = digitalio.DigitalInOut(D12)
lcd_d6 = digitalio.DigitalInOut(D11)
lcd_d5 = digitalio.DigitalInOut(D10)
lcd_d4 = digitalio.DigitalInOut(D9)
lcd_backlight = digitalio.DigitalInOut(D13)
red = pulseio.PWMOut(D3)
green = pulseio.PWMOut(D4)
blue = pulseio.PWMOut(D5)

#   Init the lcd class
lcd = adafruit_character_lcd.Character_LCD_RGB(lcd_rs, lcd_en, lcd_d4, lcd_d5,
                                               lcd_d6, lcd_d7, lcd_columns, lcd_rows,
                                               red, green, blue, lcd_backlight)

#pylint: disable-msg=bad-whitespace
# only red
RED     = [100, 0,   0]
GREEN   = [0,   100, 0]
BLUE    = [0,   0,   100]
#pylint: enable-msg=bad-whitespace

while True:
    lcd.message('CircuitPython\nRGB Test')
    lcd.set_color(RED)
    time.sleep(1)
    lcd.set_color(GREEN)
    time.sleep(1)
    lcd.set_color(BLUE)
    time.sleep(1)
