"""Simple test for RGB character LCD on Raspberry Pi"""
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# Raspberry Pi Pin Config:
lcd_rs = digitalio.DigitalInOut(board.D26)  # pin 4
lcd_en = digitalio.DigitalInOut(board.D19)  # pin 6
lcd_d7 = digitalio.DigitalInOut(board.D27)  # pin 14
lcd_d6 = digitalio.DigitalInOut(board.D22)  # pin 13
lcd_d5 = digitalio.DigitalInOut(board.D24)  # pin 12
lcd_d4 = digitalio.DigitalInOut(board.D25)  # pin 11
lcd_backlight = digitalio.DigitalInOut(board.D4)

red = digitalio.DigitalInOut(board.D21)
green = digitalio.DigitalInOut(board.D12)
blue = digitalio.DigitalInOut(board.D18)

# Initialise the LCD class
lcd = characterlcd.Character_LCD_RGB(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns,
                                     lcd_rows, red, green, blue, lcd_backlight)

RED = [1, 0, 0]
GREEN = [0, 1, 0]
BLUE = [0, 0, 1]

while True:
    lcd.clear()
    lcd.message = 'CircuitPython\nRGB Test: RED'
    lcd.color = RED
    time.sleep(1)

    lcd.clear()
    lcd.message = 'CircuitPython\nRGB Test: GREEN'
    lcd.color = GREEN
    time.sleep(1)

    lcd.clear()
    lcd.message = 'CircuitPython\nRGB Test: BLUE'
    lcd.color = BLUE
    time.sleep(1)
