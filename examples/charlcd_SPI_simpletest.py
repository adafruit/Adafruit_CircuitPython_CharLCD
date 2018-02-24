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

#   Print a 2x line message
lcd.message('hello\ncircuitpython')
# Wait 5s
time.sleep(5)
#   Demo showing cursor
lcd.clear()
lcd.show_cursor(True)
lcd.message('showing cursor ')
#   Wait 5s
time.sleep(5)
#   Demo showing the blinking cursor
lcd.clear()
lcd.blink(True)
lcd.message('Blinky Cursor!')
#   Wait 5s
time.sleep(5)
lcd.blink(False)
#   Demo scrolling message LEFT
lcd.clear()
scroll_msg = 'Scroll'
lcd.message(scroll_msg)
#   Scroll to the left
for i in range(lcd_columns - len(scroll_msg)):
    time.sleep(0.5)
    lcd.move_left()
#   Demo turning backlight off
lcd.clear()
lcd.message("going to sleep\ncya later!")
lcd.set_backlight(False)
time.sleep(2)
