"""
`adafruit_character_lcd.character_lcd_i2c_sainsmart`
====================================================
Module for using I2C with I2C Sainsmart LCD and LED

Implementation Notes
--------------------

**Hardware:**

"* `16x2 I2C IIC Interface RGB LED Screen + Keypad For Raspberry Pi
<https://www.sainsmart.com/products/16x2-i2c-iic-interface-rgb-led-screen-keypad-for-raspberry-pi>`_"

**Software and Dependencies:**
* Adafruit CircuitPython firmware:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library (when using I2C/SPI):
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

"""

import digitalio
from adafruit_character_lcd.character_lcd import Character_LCD_RGB

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CharLCD.git"

class Character_LCD_RGB_I2C_Sainsmart(Character_LCD_RGB):
    """
    RGB Character with Sainsmart LCD and LED connected to I2C shield or Pi plate
    using I2C connection. This is a subclass of Character_LCD_RGB and implements
    all of the same functions and functionality.
    """
    def __init__(self, i2c, columns, lines, backlight_on=True):
        # pylint: disable=too-many-locals
        """Initialize RGB character LCD connected to shield using I2C connection
        on the specified I2C bus with the specified number of columns and lines
        on the display. Backlight will switch ON by default
        """
        import adafruit_mcp230xx
        self._mcp = adafruit_mcp230xx.MCP23017(i2c)

        # The backlight is connected to GPA5, which is the 6th bit of port A.
        # We need to set this to 0. Port start from 0 to 7, so 6th bit is 5
        self._mcp.iodira = Character_LCD_RGB_I2C_Sainsmart.modify_bit(self._mcp.iodira, 5, 0)

        reset = self._mcp.get_pin(15)
        read_write = self._mcp.get_pin(14)
        enable = self._mcp.get_pin(13)
        db4 = self._mcp.get_pin(12)
        db5 = self._mcp.get_pin(11)
        db6 = self._mcp.get_pin(10)
        db7 = self._mcp.get_pin(9)
        red = self._mcp.get_pin(6)
        green = self._mcp.get_pin(7)
        blue = self._mcp.get_pin(8)
        self._left_button = self._mcp.get_pin(4)
        self._up_button = self._mcp.get_pin(3)
        self._down_button = self._mcp.get_pin(2)
        self._right_button = self._mcp.get_pin(1)
        self._select_button = self._mcp.get_pin(0)

        self._buttons = [self._left_button, self._up_button, self._down_button, self._right_button,
                         self._select_button]

        for pin in self._buttons:
            pin.switch_to_input(pull=digitalio.Pull.UP)

        super().__init__(reset, enable, db4, db5, db6, db7, columns, lines, red, green, blue,
                         read_write)

        if backlight_on:
            self.backlight_on()

    @staticmethod
    def modify_bit(value, position, bit_value):
        """Modify given integer value at position bit value.
        """
        mask = 1 << position
        return (value & ~mask) | ((bit_value << position) & mask)

    def backlight_on(self, clear_led=True):
        """Turning on backlight. LED will become purple, clear the LED by default.
        """
        self._mcp.gpioa = Character_LCD_RGB_I2C_Sainsmart.modify_bit(self._mcp.gpioa, 5, 0)
        if clear_led:
            self.color = [0, 0, 0]

    def backlight_off(self, clear_led=True):
        """Turning off backlight. LED will also be clear by default.
        """
        self._mcp.gpioa = Character_LCD_RGB_I2C_Sainsmart.modify_bit(self._mcp.gpioa, 5, 1)
        if clear_led:
            self.color = [0, 0, 0]

    @property
    def left_button(self):
        """The left button on the RGB Character LCD I2C Shield or Pi plate.
        """
        return not self._left_button.value

    @property
    def up_button(self):
        """The up button on the RGB Character LCD I2C Shield or Pi plate.
        """
        return not self._up_button.value

    @property
    def down_button(self):
        """The down button on the RGB Character LCD I2C Shield or Pi plate.
        """
        return not self._down_button.value

    @property
    def right_button(self):
        """The down button on the RGB Character LCD I2C Shield or Pi plate.
        """
        return not self._right_button.value

    @property
    def select_button(self):
        """The select button on the RGB Character LCD I2C Shield or Pi plate.
        """
        return not self._select_button.value
