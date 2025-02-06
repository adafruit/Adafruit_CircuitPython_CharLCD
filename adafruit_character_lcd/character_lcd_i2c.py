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
import time

try:
    from typing import Optional
    import busio
except ImportError:
    pass

from adafruit_mcp230xx.mcp23008 import MCP23008
from adafruit_pcf8574 import PCF8574
from adafruit_character_lcd.character_lcd import Character_LCD_Mono

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CharLCD.git"


class I2C_Expander:
    # pylint: disable=too-few-public-methods
    """
    I2C Expander ICs
    """

    MCP23008 = "MCP23008"
    PCF8574 = "PCF8574"


class Character_LCD_I2C(Character_LCD_Mono):
    # pylint: disable=too-few-public-methods
    """Character LCD connected to I2C/SPI backpack using its I2C connection.
    This is a subclass of `Character_LCD_Mono` and implements all the same
    functions and functionality.

    To use, import and initialise as follows:

    .. code-block:: python

        import board
        from adafruit_character_lcd.character_lcd_i2c import Character_LCD_I2C

        i2c = board.I2C()  # uses board.SCL and board.SDA
        lcd = Character_LCD_I2C(i2c, 16, 2)
    """

    # pylint: disable=too-many-positional-arguments
    def __init__(
        self,
        i2c: busio.I2C,
        columns: int,
        lines: int,
        address: Optional[int] = None,
        backlight_inverted: bool = False,
        expander: I2C_Expander = I2C_Expander.MCP23008,
    ) -> None:
        """Initialize character LCD connected to backpack using I2C connection
        on the specified I2C bus with the specified number of columns and
        lines on the display. Optionally specify if backlight is inverted.
        """

        if expander == I2C_Expander.MCP23008:
            if address:
                self.expander = MCP23008(i2c, address=address)
            else:
                self.expander = MCP23008(i2c)

            super().__init__(
                self.expander.get_pin(1),  # reset
                self.expander.get_pin(2),  # enable
                self.expander.get_pin(3),  # data line 4
                self.expander.get_pin(4),  # data line 5
                self.expander.get_pin(5),  # data line 6
                self.expander.get_pin(6),  # data line 7
                columns,
                lines,
                backlight_pin=self.expander.get_pin(7),
                backlight_inverted=backlight_inverted,
            )

        elif expander == I2C_Expander.PCF8574:
            if address:
                self.expander = PCF8574(i2c, address=address)
            else:
                self.expander = PCF8574(i2c)

            super().__init__(
                self.expander.get_pin(0),  # reset
                self.expander.get_pin(2),  # enable
                self.expander.get_pin(4),  # data line 4
                self.expander.get_pin(5),  # data line 5
                self.expander.get_pin(6),  # data line 6
                self.expander.get_pin(7),  # data line 7
                columns,
                lines,
                backlight_pin=self.expander.get_pin(3),
                backlight_inverted=backlight_inverted,
            )

    def _write8(self, value: int, char_mode: bool = False) -> None:
        if not isinstance(self.expander, MCP23008):
            super()._write8(value, char_mode)
            return

        # Sends 8b ``value`` in ``char_mode``.
        # :param value: bytes
        # :param char_mode: character/data mode selector. False (default) for
        # data only, True for character bits.
        #  one ms delay to prevent writing too quickly.
        time.sleep(0.001)

        # bits are, MSB (7) to LSB (0)
        # backlight:   bit 7
        # data line 7: bit 6
        # data line 6: bit 5
        # data line 5: bit 4
        # data line 4: bit 3
        # enable:      bit 2
        # reset:       bit 1
        # (unused):    bit 0

        reset_bit = int(char_mode) << 1
        backlight_bit = int(self.backlight ^ self.backlight_inverted) << 7

        # Write char_mode and upper 4 bits of data, shifted to the correct position.
        self.expander.gpio = reset_bit | backlight_bit | ((value & 0xF0) >> 1)

        #  do command
        self._pulse_enable()

        # Write char_mode and lower 4 bits of data, shifted to the correct position.
        self.expander.gpio = reset_bit | backlight_bit | ((value & 0x0F) << 3)

        # do command
        self._pulse_enable()
