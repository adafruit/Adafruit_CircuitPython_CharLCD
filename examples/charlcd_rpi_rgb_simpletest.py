"""Simple test for RGB character LCD on Raspberry Pi"""
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# Raspberry Pi Pin Config:
lcd_rs = digitalio.DigitalInOut(board.D26)  # LCD pin 4
lcd_en = digitalio.DigitalInOut(board.D19)  # LCD pin 6
lcd_d7 = digitalio.DigitalInOut(board.D27)  # LCD pin 14
lcd_d6 = digitalio.DigitalInOut(board.D22)  # LCD pin 13
lcd_d5 = digitalio.DigitalInOut(board.D24)  # LCD pin 12
lcd_d4 = digitalio.DigitalInOut(board.D25)  # LCD pin 11
lcd_rw = digitalio.DigitalInOut(board.D4)   # LCD pin 5.  Determines whether to read to or write from the display. Not necessary if only writing to the display. Used on shield.

red = digitalio.DigitalInOut(board.D21)
green = digitalio.DigitalInOut(board.D12)
blue = digitalio.DigitalInOut(board.D18)

# Initialize the LCD class
# The lcd_rw parameter is optional.  You can omit the line below if you're only writing to the display.
lcd = characterlcd.Character_LCD_RGB(
    lcd_rs,
    lcd_en,
    lcd_d4,
    lcd_d5,
    lcd_d6,
    lcd_d7,
    lcd_columns,
    lcd_rows,
    red,
    green,
    blue,
    lcd_rw,
)

RED = [1, 0, 0]
GREEN = [0, 1, 0]
BLUE = [0, 0, 1]

while True:
    lcd.clear()
    lcd.message = "CircuitPython\nRGB Test: RED"
    lcd.color = RED
    time.sleep(1)

    lcd.clear()
    lcd.message = "CircuitPython\nRGB Test: GREEN"
    lcd.color = GREEN
    time.sleep(1)

    lcd.clear()
    lcd.message = "CircuitPython\nRGB Test: BLUE"
    lcd.color = BLUE
    time.sleep(1)
