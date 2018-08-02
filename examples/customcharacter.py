import digitalio
from board import D7, D8, D9, D10, D11, D12, D13
import adafruit_character_lcd


lcd_columns = 16
lcd_rows = 2
lcd_rs = digitalio.DigitalInOut(D7)
lcd_en = digitalio.DigitalInOut(D8)
lcd_d7 = digitalio.DigitalInOut(D12)
lcd_d6 = digitalio.DigitalInOut(D11)
lcd_d5 = digitalio.DigitalInOut(D10)
lcd_d4 = digitalio.DigitalInOut(D9)
lcd_backlight = digitalio.DigitalInOut(D13)
lcd = adafruit_character_lcd.Character_LCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                           lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
checkmark = bytes([0x0, 0x0, 0x1, 0x3, 0x16, 0x1c, 0x8, 0x0])
lcd.clear()
lcd.message('\x00')
