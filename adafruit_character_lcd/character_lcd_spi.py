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
`adafruit_character_lcd.character_lcd_spi`
====================================================

Module for using SPI with I2C/SPI character LCD backpack

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

import adafruit_74hc595
from adafruit_character_lcd.character_lcd import Character_LCD_Mono

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CharLCD.git"


class Character_LCD_SPI(Character_LCD_Mono):  # pylint: disable=too-few-public-methods
    """Character LCD connected to I2C/SPI backpack using its SPI connection.
    This is a subclass of Character_LCD and implements all of the same
    functions and functionality.

    To use, import and initialise as follows:

    .. code-block:: python

        import board
        import busio
        import digitalio
        import adafruit_character_lcd.character_lcd_mono as character_lcd

        spi = busio.SPI(board.SCK, MOSI=board.MOSI)
        latch = digitalio.DigitalInOut(board.D5)
        lcd = character_lcd.Character_LCD_SPI(spi, latch, 16, 2)
    """

    def __init__(self, spi, latch, columns, lines, backlight_inverted=False):
        # pylint: disable=too-many-arguments
        """Initialize character LCD connected to backpack using SPI connection
        on the specified SPI bus and latch line with the specified number of
        columns and lines on the display. Optionally specify if backlight is
        inverted.
        """
        # pylint: enable=too-many-arguments

        self._shift_register = adafruit_74hc595.ShiftRegister74HC595(spi, latch)
        reset = self._shift_register.get_pin(1)
        enable = self._shift_register.get_pin(2)
        db4 = self._shift_register.get_pin(6)
        db5 = self._shift_register.get_pin(5)
        db6 = self._shift_register.get_pin(4)
        db7 = self._shift_register.get_pin(3)
        backlight_pin = self._shift_register.get_pin(7)
        super().__init__(
            reset,
            enable,
            db4,
            db5,
            db6,
            db7,
            columns,
            lines,
            backlight_pin=backlight_pin,
            backlight_inverted=backlight_inverted,
        )
