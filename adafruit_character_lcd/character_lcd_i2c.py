# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_character_lcd.character_lcd_i2c`
====================================================

Module for using I2C with I2C/SPI character LCD backpack

* Author(s): Kattni Rembor

Implementation Notes
--------------------

**Hardware:**

* `I2C / SPI character LCD backpack
  <https://www.adafruit.com/product/292>`_ (Product ID: 292)

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Bus Device library:
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

"""

from adafruit_mcp230xx.mcp23008 import MCP23008
from adafruit_character_lcd.character_lcd import Character_LCD_Mono

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CharLCD.git"


class Character_LCD_I2C(Character_LCD_Mono):
    # pylint: disable=too-few-public-methods, too-many-arguments
    """Character LCD connected to I2C/SPI backpack using its I2C connection.
    This is a subclass of `Character_LCD_Mono` and implements all of the
    same functions and functionality.

    To use, import and initialise as follows:

    .. code-block:: python

        import board
        from adafruit_character_lcd.character_lcd_i2c import Character_LCD_I2C

        i2c = board.I2C()  # uses board.SCL and board.SDA
        lcd = Character_LCD_I2C(i2c, 16, 2)
    """

    def __init__(self, i2c, columns, lines, address=None, backlight_inverted=False):
        """Initialize character LCD connected to backpack using I2C connection
        on the specified I2C bus with the specified number of columns and
        lines on the display. Optionally specify if backlight is inverted.
        """

        if address:
            mcp = MCP23008(i2c, address=address)
        else:
            mcp = MCP23008(i2c)
        super().__init__(
            mcp.get_pin(1),
            mcp.get_pin(2),
            mcp.get_pin(3),
            mcp.get_pin(4),
            mcp.get_pin(5),
            mcp.get_pin(6),
            columns,
            lines,
            backlight_pin=mcp.get_pin(7),
            backlight_inverted=backlight_inverted,
        )
