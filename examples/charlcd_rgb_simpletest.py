import time
import board
import digitalio
import adafruit_character_lcd
import pulseio

# Character LCD Config:
# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# Metro M0 Pin Config:
lcd_rs = digitalio.DigitalInOut(board.D7)
lcd_en = digitalio.DigitalInOut(board.D8)
lcd_d7 = digitalio.DigitalInOut(board.D12)
lcd_d6 = digitalio.DigitalInOut(board.D11)
lcd_d5 = digitalio.DigitalInOut(board.D10)
lcd_d4 = digitalio.DigitalInOut(board.D9)
lcd_backlight = digitalio.DigitalInOut(board.D13)
red = pulseio.PWMOut(board.D3)
green = pulseio.PWMOut(board.D4)
blue = pulseio.PWMOut(board.D5)

# Init the LCD class
lcd = adafruit_character_lcd.Character_LCD_RGB(lcd_rs, lcd_en, lcd_d4, lcd_d5,
                                               lcd_d6, lcd_d7, lcd_columns, lcd_rows,
                                               red, green, blue, lcd_backlight)


RED = [100, 0, 0]
GREEN = [0, 100, 0]
BLUE = [0, 0, 100]


while True:
    lcd.message('CircuitPython\nRGB Test')
    lcd.set_color(RED)
    time.sleep(1)
    lcd.set_color(GREEN)
    time.sleep(1)
    lcd.set_color(BLUE)
    time.sleep(1)
