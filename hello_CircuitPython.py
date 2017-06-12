"""
'hello_CircuitPython.py' 
=================================================
hello world using 16x2 character lcd
requires: 
- CircuitPython_CharLCD Module
- busio module 
""" 

import time, math, busio, digitalio
import cirpyth_char_lcd
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

#  init the lcd class
lcd = CircuitPython_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

#  print a oneline message
lcd.message('hello')
# wait five seconds
time.sleep(5)

