"""Simple test for keypad on I2C RGB character LCD Shield or Pi Plate kits"""
import time
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

# Modify this if you have a different sized Character LCD
lcd_columns = 16
lcd_rows = 2

# Initialise I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Initialise the LCD class
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

lcd.clear()
lcd.color = [100, 0, 0]
while True:
    if lcd.left_button:
        print("Left!")
        lcd.message = "Left!"

    elif lcd.up_button:
        print("Up!")
        lcd.message = "Up!"

    elif lcd.down_button:
        print("Down!")
        lcd.message = "Down!"

    elif lcd.right_button:
        print("Right!")
        lcd.message = "Right!"

    elif lcd.select_button:
        print("Select!")
        lcd.message = "Select!"

    else:
        time.sleep(0.1)
        lcd.clear()
