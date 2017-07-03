import time, math, digitalio
import adafruit_character_lcd as LCD
from board import *
import analogio
lcd_columns = 16
lcd_rows = 2 
lcd_rs = digitalio.DigitalInOut(D7)
lcd_en = digitalio.DigitalInOut(D8)
lcd_d7 = digitalio.DigitalInOut(D12)
lcd_d6 = digitalio.DigitalInOut(D11)
lcd_d5 = digitalio.DigitalInOut(D10)
lcd_d4 = digitalio.DigitalInOut(D9)
lcd_backlight = digitalio.DigitalInOut(D13)
lcd = LCD.cirpyth_char_lcd(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
checkmark = bytes([0x0,0x1,0x3,0x16,0x1c,0x8,0x0])
lcd.message('\x00')



