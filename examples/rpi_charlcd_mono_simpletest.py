import time
import board
import digitalio
import adafruit_character_lcd

# Character LCD Config:
# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# Raspberry Pi Pin Config:
lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D27)
lcd_d6 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_backlight = digitalio.DigitalInOut(board.D4)

# Init the lcd class
lcd = adafruit_character_lcd.Character_LCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                           lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

# Print a 2x line message
lcd.message('hello\ncircuitpython')
# Wait 5s
time.sleep(5)
# Demo showing cursor
lcd.clear()
lcd.show_cursor(True)
lcd.message('showing cursor ')
# Wait 5s
time.sleep(5)
# Demo showing the blinking cursor
lcd.clear()
lcd.blink(True)
lcd.message('Blinky Cursor!')
# Wait 5s
time.sleep(5)
lcd.blink(False)
# Demo scrolling message LEFT
lcd.clear()
scroll_msg = 'Scroll'
lcd.message(scroll_msg)
# Scroll to the left
for i in range(lcd_columns - len(scroll_msg)):
    time.sleep(0.5)
    lcd.move_left()
# Demo turning backlight off
lcd.clear()
lcd.message("going to sleep\ncya later!")
lcd.set_backlight(False)
time.sleep(2)
