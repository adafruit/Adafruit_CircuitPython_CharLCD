# The MIT License (MIT)
#
# Copyright (c) 2018 Kattni Rembor for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_character_lcd.character_lcd_i2c`
====================================================

Module for using I2C with I2C/SPI character LCD backpack

* Author(s): Kattni Rembor

Implementation Notes
--------------------

**Hardware:**

"* `I2C / SPI character LCD backpack <https://www.adafruit.com/product/292>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library (when using I2C/SPI):
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

"""

from adafruit_mcp230xx.mcp23008 import MCP23008
from adafruit_character_lcd.character_lcd import Character_LCD_Mono

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CharLCD.git"


class Character_LCD_I2C(Character_LCD_Mono):
    # pylint: disable=too-few-public-methods, too-many-arguments
    """Character LCD connected to I2C/SPI backpack using its I2C connection.
    This is a subclass of Character_LCD and implements all of the same
    functions and functionality.

    To use, import and initialise as follows:

    .. code-block:: python

        import board
        import busio
        from adafruit_character_lcd.character_lcd_i2c import Character_LCD_I2C

        i2c = busio.I2C(board.SCL, board.SDA)
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
