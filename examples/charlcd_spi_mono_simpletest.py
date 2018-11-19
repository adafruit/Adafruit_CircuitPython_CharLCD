# Hello World using 16x2 character lcd and an 74LS595 SPI LCD backpack.
import time

import board
import busio
import digitalio

import adafruit_character_lcd


#   Character LCD Config:
#   modify this if you have a different sized charlcd
lcd_columns = 16
lcd_rows = 2

#   Backpack connection configuration:
clk = board.SCK    # Pin connected to backpack CLK.
data = board.MOSI   # Pin connected to backpack DAT/data.
latch = board.D5     # Pin connected to backpack LAT/latch.

#   Initialize SPI bus.
spi = busio.SPI(clk, MOSI=data)

#   Init the lcd class
latch = digitalio.DigitalInOut(latch)
lcd = adafruit_character_lcd.Character_LCD_SPI(spi, latch, lcd_columns, lcd_rows)

# Turn on backlight
lcd.backlight = True
# Print a two line message
lcd.message = "Hello\nCircuitPython"
# Wait 5s
time.sleep(5)
lcd.clear()
# Print two line message right to left
lcd.text_direction = lcd.RIGHT_TO_LEFT
lcd.message = "Hello\nCircuitPython"
# Wait 5s
time.sleep(5)
# Return text direction to left to right
lcd.text_direction = lcd.LEFT_TO_RIGHT
# Demo showing cursor
lcd.clear()
lcd.cursor = True
lcd.message = "Cursor! "
# Wait 5s
time.sleep(5)
# Demo showing the blinking cursor
lcd.clear()
lcd.blink = True
lcd.message = "Blinky Cursor!"
# Wait 5s
time.sleep(5)
lcd.blink = False
# Demo scrolling message LEFT
lcd.clear()
scroll_msg = '<-- Scroll'
lcd.message = scroll_msg
# Scroll to the left
for i in range(len(scroll_msg)):
    time.sleep(0.5)
    lcd.move_left()
lcd.clear()
lcd.message = "Going to sleep\nCya later!"
# Demo turning backlight off
lcd.backlight = False
time.sleep(2)
