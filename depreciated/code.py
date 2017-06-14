"""
'hello_CircuitPython.py' 
=================================================
hello world using 16x2 character lcd
requires: 
- CircuitPython_CharLCD Module
- busio module 
""" 

import time, math, busio, digitalio
import af_lcd as LCD
from board import *

#  Character LCD Config:
lcd_columns = 16
lcd_rows = 2 

#  Metro m0 Pin Config:

lcd_rs = digitalio.DigitalInOut(D7)
lcd_en = digitalio.DigitalInOut(D8)
lcd_d7 = digitalio.DigitalInOut(D12)
lcd_d6 = digitalio.DigitalInOut(D11)
lcd_d5 = digitalio.DigitalInOut(D10)
lcd_d4 = digitalio.DigitalInOut(D9)
lcd_backlight = digitalio.DigitalInOut(D13)

#	init the lcd class
lcd = LCD.cirpyth_char_lcd(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, 
	lcd_d7, lcd_columns, lcd_rows,lcd_backlight)

#	Print a 2x line message 
lcd.message('hello\ncircuitpython')

#	Wait 5s
time.sleep(5)

#	Demo showing cursor 
lcd.clear()
lcd.show_cursor(True)
lcd.message('showing cursor ')

#	Wait 5s
time.sleep(5)

#	Demo showing the blinking cursor
lcd.clear()
lcd.blink(True)
lcd.message('Blinky Cursor!')

#	Wait 5s
time.sleep(5)
lcd.blink(False)

