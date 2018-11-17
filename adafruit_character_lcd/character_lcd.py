# The MIT License (MIT)
#
# Copyright (c) 2017 Brent Rubell for Adafruit Industries
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
`adafruit_character_lcd.character_lcd`
====================================================

Module for interfacing with monochromatic character LCDs

* Author(s): Kattni Rembor, Brent Rubell, Asher Lieber,
  Tony DiCola (original python charLCD library)

Implementation Notes
--------------------

**Hardware:**

* Adafruit `Character LCDs
  <http://www.adafruit.com/category/63_96>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library (when using I2C/SPI):
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

"""

import time
import digitalio
from micropython import const
import adafruit_mcp230xx
import adafruit_74hc595

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CharLCD.git"

#pylint: disable-msg=bad-whitespace
# Commands
_LCD_CLEARDISPLAY        = const(0x01)
_LCD_RETURNHOME          = const(0x02)
_LCD_ENTRYMODESET        = const(0x04)
_LCD_DISPLAYCONTROL      = const(0x08)
_LCD_CURSORSHIFT         = const(0x10)
_LCD_FUNCTIONSET         = const(0x20)
_LCD_SETCGRAMADDR        = const(0x40)
_LCD_SETDDRAMADDR        = const(0x80)

# Entry flags
_LCD_ENTRYRIGHT          = const(0x00)
_LCD_ENTRYLEFT           = const(0x02)
_LCD_ENTRYSHIFTINCREMENT = const(0x01)
_LCD_ENTRYSHIFTDECREMENT = const(0x00)

# Control flags
_LCD_DISPLAYON           = const(0x04)
_LCD_DISPLAYOFF          = const(0x00)
_LCD_CURSORON            = const(0x02)
_LCD_CURSOROFF           = const(0x00)
_LCD_BLINKON             = const(0x01)
_LCD_BLINKOFF            = const(0x00)

# Move flags
_LCD_DISPLAYMOVE         = const(0x08)
_LCD_CURSORMOVE          = const(0x00)
_LCD_MOVERIGHT           = const(0x04)
_LCD_MOVELEFT            = const(0x00)

# Function set flags
_LCD_8BITMODE            = const(0x10)
_LCD_4BITMODE            = const(0x00)
_LCD_2LINE               = const(0x08)
_LCD_1LINE               = const(0x00)
_LCD_5X10DOTS            = const(0x04)
_LCD_5X8DOTS             = const(0x00)

# Offset for up to 4 rows.
_LCD_ROW_OFFSETS         = (0x00, 0x40, 0x14, 0x54)

#pylint: enable-msg=bad-whitespace

def _set_bit(byte_value, position, val):
    # Given the specified byte_value set the bit at position to the provided
    # boolean value val and return the modified byte.
    ret = None
    if val:
        ret = byte_value | (1 << position)
    else:
        ret = byte_value & ~(1 << position)

    return ret

#pylint: disable-msg=too-many-instance-attributes
class Character_LCD(object):
    """
    Interfaces with a character LCD
    :param ~digitalio.DigitalInOut rs: The reset data line
    :param ~digitalio.DigitalInOut en: The enable data line
    :param ~digitalio.DigitalInOut d4: The data line 4
    :param ~digitalio.DigitalInOut d5: The data line 5
    :param ~digitalio.DigitalInOut d6: The data line 6
    :param ~digitalio.DigitalInOut d7: The data line 7
    :param cols: The columns on the charLCD
    :param lines: The lines on the charLCD
    :param ~digitalio.DigitalInOut backlight: The backlight pin, usually
    the last pin. Check with your datasheet

    """
    #pylint: disable-msg=too-many-arguments
    def __init__(self, rs, en, d4, d5, d6, d7, cols, lines,
                 backlight_pin=None,
                 backlight_inverted=False
                ):

        self.cols = cols
        self.lines = lines
        #  save pin numbers
        self.reset = rs
        self.enable = en
        self.dl4 = d4
        self.dl5 = d5
        self.dl6 = d6
        self.dl7 = d7
        # backlight pin
        self.backlight_pin = backlight_pin
        self.backlight_inverted = backlight_inverted
        # self.pwn_enabled = enable_pwm
        # set all pins as outputs
        for pin in(rs, en, d4, d5, d6, d7):
            pin.direction = digitalio.Direction.OUTPUT
        #  Setup backlight
        if backlight_pin is not None:
            self.backlight_pin.direction = digitalio.Direction.OUTPUT
            if backlight_inverted:
                self.backlight_pin.value = 0  # turn backlight on
            else:
                self.backlight_pin.value = 1  # turn backlight on
        #  initialize the display
        self._write8(0x33)
        self._write8(0x32)
        #  init. display control
        self.displaycontrol = _LCD_DISPLAYON | _LCD_CURSOROFF | _LCD_BLINKOFF
        #  init display function
        self.displayfunction = _LCD_4BITMODE | _LCD_1LINE | _LCD_2LINE | _LCD_5X8DOTS
        #  init display mode
        self.displaymode = _LCD_ENTRYLEFT | _LCD_ENTRYSHIFTDECREMENT
        #  write to display control
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)
        #  write displayfunction
        self._write8(_LCD_FUNCTIONSET | self.displayfunction)
        #  set the entry mode
        self._write8(_LCD_ENTRYMODESET | self.displaymode)
        self.clear()

        self._message = None
        self._enable = None
    #pylint: enable-msg=too-many-arguments

    def home(self):
        """Moves the cursor back home pos(1,1)"""
        self._write8(_LCD_RETURNHOME)
        time.sleep(0.003)

    def clear(self):
        """Clears the LCD"""
        self._write8(_LCD_CLEARDISPLAY)
        time.sleep(0.003)

    @property
    def cursor(self):
        """True if cursor is visible, otherwise False."""
        return self.displaycontrol & _LCD_CURSORON == _LCD_CURSORON

    @cursor.setter
    def cursor(self, show):
        """True if cursor is visible, otherwise False."""
        if show:
            self.displaycontrol |= _LCD_CURSORON
        else:
            self.displaycontrol &= ~_LCD_CURSORON
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)

    def cursor_position(self, column, row):
        """Move the cursor to position ``column`` and ``row``
            :param column: column location
            :param row: row location
        """
        # Clamp row to the last row of the display
        if row > self.lines:
            row = self.lines - 1
        # Set location
        self._write8(_LCD_SETDDRAMADDR | (column + _LCD_ROW_OFFSETS[row]))

    @property
    def blink(self):
        return self.displaycontrol & _LCD_BLINKON == _LCD_BLINKON

    @blink.setter
    def blink(self, blink):
        """
        Blinks the cursor if blink = true.

        :param blink: True to blink, False no blink

        """
        if blink:
            self.displaycontrol |= _LCD_BLINKON
        else:
            self.displaycontrol &= ~_LCD_BLINKON
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)

    @property
    def display(self):
        return self.displaycontrol & _LCD_DISPLAYON == _LCD_DISPLAYON

    @display.setter
    def display(self, enable):
        """
        Enable or disable the display.

        :param enable: True to enable display, False to disable

        """
        if enable:
            self.displaycontrol |= _LCD_DISPLAYON
        else:
            self.displaycontrol &= ~_LCD_DISPLAYON
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        """Write text to display, can include \n for newline
            :param message: string to display
        """
        self._message = message
        line = 0
        # Track times through iteration, to act on the initial character of the message
        initial_character = 0
        # iterate through each character
        for character in message:
            if initial_character == 0:
                col = 0 if self.displaymode & _LCD_ENTRYLEFT > 0 else self.cols - 1
                self.cursor_position(col, line)
                initial_character += 1
            # if character is \n, go to next line
            if character == '\n':
                line += 1
                # move to left/right depending on text direction
                col = 0 if self.displaymode & _LCD_ENTRYLEFT > 0 else self.cols - 1
                self.cursor_position(col, line)
            # Write character to display
            else:
                self._write8(ord(character), True)

    def move_left(self):
        """Moves display left one position"""
        self._write8(_LCD_CURSORSHIFT | _LCD_DISPLAYMOVE | _LCD_MOVELEFT)

    def move_right(self):
        """Moves display right one position"""
        self._write8(_LCD_CURSORSHIFT | _LCD_DISPLAYMOVE | _LCD_MOVERIGHT)

    @property
    def left_to_right(self):
        return self.displaymode & _LCD_ENTRYLEFT == _LCD_ENTRYLEFT

    @left_to_right.setter
    def left_to_right(self, left_to_right):
        """Direction of text to read from left to right"""
        if left_to_right:
            self.displaymode |= _LCD_ENTRYLEFT
            self._write8(_LCD_ENTRYMODESET | self.displaymode)

    @property
    def right_to_left(self):
        return self.displaymode & _LCD_ENTRYLEFT != _LCD_ENTRYLEFT

    @right_to_left.setter
    def right_to_left(self, right_to_left):
        """Direction of text to read from right to left"""
        if right_to_left:
            self.displaymode &= ~_LCD_ENTRYLEFT
            self._write8(_LCD_ENTRYMODESET | self.displaymode)

    @property
    def backlight(self):
        return self._enable

    @backlight.setter
    def backlight(self, enable):
        self._enable = enable
        """
        Set lighton to turn the charLCD backlight on.

        :param enable: True to turn backlight on, False to turn off

        """
        if enable and not self.backlight_inverted or not enable and self.backlight_inverted:
            self.backlight_pin.value = 1
        if enable and self.backlight_inverted or not enable and not self.backlight_inverted:
            self.backlight_pin.value = 0

    def create_char(self, location, pattern):
        """
        Fill one of the first 8 CGRAM locations with custom characters.
        The location parameter should be between 0 and 7 and pattern should
        provide an array of 8 bytes containing the pattern. E.g. you can easily
        design your custom character at http://www.quinapalus.com/hd44780udg.html
        To show your custom character use eg. lcd.message = "\x01"

        :param location: integer in range(8) to store the created character
        :param ~bytes pattern: len(8) describes created character

        """
        # only position 0..7 are allowed
        location &= 0x7
        self._write8(_LCD_SETCGRAMADDR | (location << 3))
        for i in range(8):
            self._write8(pattern[i], char_mode=True)

    def _write8(self, value, char_mode=False):
        # Sends 8b ``value`` in ``char_mode``.
        # :param value: bytes
        # :param char_mode: character/data mode selector. False (default) for
        # data only, True for character bits.
        #  one ms delay to prevent writing too quickly.
        time.sleep(0.001)
        #  set character/data bit. (charmode = False)
        self.reset.value = char_mode
        # WRITE upper 4 bits
        self.dl4.value = ((value >> 4) & 1) > 0
        self.dl5.value = ((value >> 5) & 1) > 0
        self.dl6.value = ((value >> 6) & 1) > 0
        self.dl7.value = ((value >> 7) & 1) > 0
        #  send command
        self._pulse_enable()
        # WRITE lower 4 bits
        self.dl4.value = (value & 1) > 0
        self.dl5.value = ((value >> 1) & 1) > 0
        self.dl6.value = ((value >> 2) & 1) > 0
        self.dl7.value = ((value >> 3) & 1) > 0
        self._pulse_enable()

    def _pulse_enable(self):
        # Pulses (lo->hi->lo) to send commands.
        self.enable.value = False
        # 1microsec pause
        time.sleep(0.0000001)
        self.enable.value = True
        time.sleep(0.0000001)
        self.enable.value = False
        time.sleep(0.0000001)
# pylint: enable-msg=too-many-instance-attributes


class Character_LCD_I2C(Character_LCD):
    def __init__(self, i2c, cols, lines):
        self._mcp = adafruit_mcp230xx.MCP23008(i2c)
        reset = self._mcp.get_pin(1)
        enable = self._mcp.get_pin(2)
        d4 = self._mcp.get_pin(3)
        d5 = self._mcp.get_pin(4)
        d6 = self._mcp.get_pin(5)
        d7 = self._mcp.get_pin(6)
        backlight_pin = self._mcp.get_pin(7)
        super().__init__(reset, enable, d4, d5, d6, d7, cols, lines,
                         backlight_pin=backlight_pin)


class Character_LCD_SPI(Character_LCD):
    """Character LCD connected to I2C/SPI backpack using its SPI connection.
    This is a subclass of Character_LCD and implements all of the same
    functions and functionality.
    """

    def __init__(self, spi, latch, cols, lines, backlight_inverted=False):
        """Initialize character LCD connectedto backpack using SPI connection
        on the specified SPI bus and latch line with the specified number of
        columns and lines on the display.
        """
        # See comment above on I2C class for why this is imported here:
        self._shift_register = adafruit_74hc595.ShiftRegister74HC595(spi, latch)
        # Setup pins for SPI backpack, see diagram:
        #   https://learn.adafruit.com/assets/35681
        reset = self._shift_register.get_pin(1)
        enable = self._shift_register.get_pin(2)
        d4 = self._shift_register.get_pin(6)
        d5 = self._shift_register.get_pin(5)
        d6 = self._shift_register.get_pin(4)
        d7 = self._shift_register.get_pin(3)
        backlight_pin = self._shift_register.get_pin(7)
        self.backlight_inverted = backlight_inverted
        super().__init__(reset, enable, d4, d5, d6, d7, cols, lines,
                         backlight_pin=backlight_pin, backlight_inverted=backlight_inverted)
