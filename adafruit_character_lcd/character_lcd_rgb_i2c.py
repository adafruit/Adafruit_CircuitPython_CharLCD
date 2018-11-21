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

Module for using I2C with I2C RGB LCD Shield or I2C RGB LCD Pi Plate

* Author(s): Kattni Rembor

Implementation Notes
--------------------

**Hardware:**

"* `RGB LCD Shield Kit w/ 16x2 Character Display - Negative Display
<https://www.adafruit.com/product/714>`_"
"* `RGB LCD Shield Kit w/ 16x2 Character Display - Positive Display
<https://www.adafruit.com/product/716>`_"
"* `Adafruit RGB Negative 16x2 LCD+Keypad Kit for Raspberry Pi
<https://www.adafruit.com/product/1110>`_"
"* `Adafruit RGB Positive 16x2 LCD+Keypad Kit for Raspberry Pi
<https://www.adafruit.com/product/1109>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library (when using I2C/SPI):
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

"""

from adafruit_character_lcd.character_lcd import Character_LCD_RGB

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CharLCD.git"


class Character_LCD_RGB_I2C(Character_LCD_RGB):
    """RGB Character LCD connected to I2C shield or Pi plate using I2C connection.
    This is a subclass of Character_LCD_RGB and implements all of the same
    functions and functionality.

    To use, import and initialise as follows:

    .. code-block:: python

        import board
        import busio
        from adafruit_character_lcd.character_lcd_rgb_i2c import Character_LCD_RGB_I2C

        i2c = busio.I2C(board.SCL, board.SDA)
        lcd = Character_LCD_RGB_I2C(i2c, 16, 2)

    """
    def __init__(self, i2c, columns, lines):
        # pylint: disable=too-many-locals
        """Initialize RGB character LCD connected to shield using I2C connection
        on the specified I2C bus with the specified number of columns and lines
        on the display.
        """
        import adafruit_mcp230xx
        self._mcp = adafruit_mcp230xx.MCP23017(i2c)
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
        super().__init__(reset, enable, db4, db5, db6, db7, columns, lines, red, green, blue,
                         read_write)
