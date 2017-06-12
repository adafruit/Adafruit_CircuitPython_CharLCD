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

#  lcd config
lcd_columns = 16
lcd_rows = 2 

#  metro m0 pin assignment
lcd_rs = digitalio.DigitalInOut(D7)
lcd_en = digitalio.DigitalInOut(D8)
lcd_d7 = digitalio.DigitalInOut(D12)
lcd_d6 = digitalio.DigitalInOut(D11)
lcd_d5 = digitalio.DigitalInOut(D10)
lcd_d4 = digitalio.DigitalInOut(D9)

#	init the lcd class
lcd = LCD.cirpyth_char_lcd(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)


#	Demo showing the blinking cursor
lcd.enable_display(True)

"""
lcd.set_cursor(0,1)
lcd.show_cursor(True)
time.sleep(1)
lcd.home()
lcd.show_cursor(True)
"""
lcd.message('hello\ncircuitpython')

#lcd.blink(True)


