# The MIT License (MIT)
#
# Copyright (c) 2017 Brent Rubell for Adafruit Industries
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

* Author(s): Brent Rubell, Asher Lieber, Tony DiCola (original python charLCD library)

Implementation Notes
--------------------

**Hardware:**

* Adafruit `Character LCDs
  <http://www.adafruit.com/category/63_96>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware (2.2.0+) for the ESP8622 and M0-based boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library (when using I2C/SPI):
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

"""

import time
import digitalio
from micropython import const

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CharLCD.git"

#pylint: disable-msg=bad-whitespace
# Commands
LCD_CLEARDISPLAY        = const(0x01)
LCD_RETURNHOME          = const(0x02)
LCD_ENTRYMODESET        = const(0x04)
LCD_DISPLAYCONTROL      = const(0x08)
LCD_CURSORSHIFT         = const(0x10)
LCD_FUNCTIONSET         = const(0x20)
LCD_SETCGRAMADDR        = const(0x40)
LCD_SETDDRAMADDR        = const(0x80)

# Entry flags
LCD_ENTRYRIGHT          = const(0x00)
LCD_ENTRYLEFT           = const(0x02)
LCD_ENTRYSHIFTINCREMENT = const(0x01)
LCD_ENTRYSHIFTDECREMENT = const(0x00)

# Control flags
LCD_DISPLAYON           = const(0x04)
LCD_DISPLAYOFF          = const(0x00)
LCD_CURSORON            = const(0x02)
LCD_CURSOROFF           = const(0x00)
LCD_BLINKON             = const(0x01)
LCD_BLINKOFF            = const(0x00)

# Move flags
LCD_DISPLAYMOVE         = const(0x08)
LCD_CURSORMOVE          = const(0x00)
LCD_MOVERIGHT           = const(0x04)
LCD_MOVELEFT            = const(0x00)

# Function set flags
LCD_8BITMODE            = const(0x10)
LCD_4BITMODE            = const(0x00)
LCD_2LINE               = const(0x08)
LCD_1LINE               = const(0x00)
LCD_5X10DOTS            = const(0x04)
LCD_5X8DOTS             = const(0x00)

# Offset for up to 4 rows.
LCD_ROW_OFFSETS         = (0x00, 0x40, 0x14, 0x54)

# MCP23008 I2C backpack pin mapping from LCD logical pin to MCP23008 pin.
_MCP23008_LCD_RS         = const(1)
_MCP23008_LCD_EN         = const(2)
_MCP23008_LCD_D4         = const(3)
_MCP23008_LCD_D5         = const(4)
_MCP23008_LCD_D6         = const(5)
_MCP23008_LCD_D7         = const(6)
_MCP23008_LCD_BACKLIGHT  = const(7)

# 74HC595 SPI backpack pin mapping from LCD logical pin to 74HC595 pin.
_74HC595_LCD_RS          = const(1)
_74HC595_LCD_EN          = const(2)
_74HC595_LCD_D4          = const(6)
_74HC595_LCD_D5          = const(5)
_74HC595_LCD_D6          = const(4)
_74HC595_LCD_D7          = const(3)
_74HC595_LCD_BACKLIGHT   = const(7)

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
                 backlight=None #,
                 #enable_pwm = False,
                 #initial_backlight = 1.0
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
        self.backlight = backlight
        # self.pwn_enabled = enable_pwm
        # set all pins as outputs
        for pin in(rs, en, d4, d5, d6, d7):
            pin.direction = digitalio.Direction.OUTPUT
        #  Setup backlight
        if backlight is not None:
            self.backlight.direction = digitalio.Direction.OUTPUT
            self.backlight.value = 0 # turn backlight on
        #  initialize the display
        self._write8(0x33)
        self._write8(0x32)
        #  init. display control
        self.displaycontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
        #  init display function
        self.displayfunction = LCD_4BITMODE | LCD_1LINE | LCD_2LINE | LCD_5X8DOTS
        #  init display mode
        self.displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
        #  write to display control
        self._write8(LCD_DISPLAYCONTROL | self.displaycontrol)
        #  write displayfunction
        self._write8(LCD_FUNCTIONSET | self.displayfunction)
        #  set the entry mode
        self._write8(LCD_ENTRYMODESET | self.displaymode)
        self.clear()
    #pylint: enable-msg=too-many-arguments

    def home(self):
        """Moves the cursor back home pos(1,1)"""
        self._write8(LCD_RETURNHOME)
        time.sleep(0.003)

    def clear(self):
        """Clears the LCD"""
        self._write8(LCD_CLEARDISPLAY)
        time.sleep(0.003)

    def show_cursor(self, show):
        """
        Show or hide the cursor

        :param show: True to show cursor, False to hide

        """
        if show:
            self.displaycontrol |= LCD_CURSORON
        else:
            self.displaycontrol &= ~LCD_DISPLAYON
        self._write8(LCD_DISPLAYCONTROL | self.displaycontrol)

    def set_cursor(self, col, row):
        """
        Sets the cursor to ``row`` and ``col``

        :param col: column location
        :param row: row location

        """
        # Clamp row to the last row of the display
        if row > self.lines:
            row = self.lines - 1
        # Set location
        self._write8(LCD_SETDDRAMADDR | (col + LCD_ROW_OFFSETS[row]))

    def blink(self, blink):
        """
        Blinks the cursor if blink = true.

        :param blink: True to blink, False no blink

        """
        if blink is True:
            self.displaycontrol |= LCD_BLINKON
        else:
            self.displaycontrol &= ~LCD_BLINKON
        self._write8(LCD_DISPLAYCONTROL | self.displaycontrol)

    def move_left(self):
        """Moves display left one position"""
        self._write8(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT)

    def move_right(self):
        """Moves display right one position"""
        self._write8(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)

    def set_left_to_right(self):
        """Set direction of text to read from left to right"""
        self.displaymode |= LCD_ENTRYLEFT
        self._write8(LCD_ENTRYMODESET | self.displaymode)

    def set_right_to_left(self):
        """Set direction of text to read from right to left"""
        self.displaymode |= LCD_ENTRYLEFT
        self._write8(LCD_ENTRYMODESET | self.displaymode)

    def enable_display(self, enable):
        """
        Enable or disable the display.

        :param enable: True to enable display, False to disable

        """
        if enable:
            self.displaycontrol |= LCD_DISPLAYON
        else:
            self.displaycontrol &= ~LCD_DISPLAYON
        self._write8(LCD_DISPLAYCONTROL | self.displaycontrol)

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

    def set_backlight(self, lighton):
        """
        Set lighton to turn the charLCD backlight on.

        :param lighton: True to turn backlight on, False to turn off

        """
        if lighton:
            self.backlight.value = 0
        else:
            self.backlight.value = 1


    def message(self, text):
        """
        Write text to display. Can include ``\\n`` for newline.

        :param text: text string to display
        """
        line = 0
        #  iterate thru each char
        for char in text:
            # if character is \n, go to next line
            if char == '\n':
                line += 1
                #  move to left/right depending on text direction
                col = 0 if self.displaymode & LCD_ENTRYLEFT > 0 else self.cols-1
                self.set_cursor(col, line)
            # Write character to display
            else:
                self._write8(ord(char), True)

    def create_char(self, location, pattern):
        """
        Fill one of the first 8 CGRAM locations with custom characters.
        The location parameter should be between 0 and 7 and pattern should
        provide an array of 8 bytes containing the pattern. E.g. you can easyly
        design your custom character at http://www.quinapalus.com/hd44780udg.html
        To show your custom character use eg. lcd.message('\x01')

        :param location: integer in range(8) to store the created character
        :param ~bytes pattern: len(8) describes created character

        """
        # only position 0..7 are allowed
        location &= 0x7
        self._write8(LCD_SETCGRAMADDR | (location << 3))
        for i in range(8):
            self._write8(pattern[i], char_mode=True)

#pylint: enable-msg=too-many-instance-attributes

class Character_LCD_I2C(Character_LCD):
    """Character LCD connected to I2C/SPI backpack using its I2C connection.
    This is a subclass of Character_LCD and implements all of the same
    functions and functionality.
    """

    def __init__(self, i2c, cols, lines):
        """Initialize character LCD connectedto backpack using I2C connection
        on the specified I2C bus and of the specified number of columns and
        lines on the display.
        """
        # Import the MCP23008 module here when the class is used
        # to keep memory usage low.  If you attempt to import globally at the
        # top of this file you WILL run out of memory on the M0, even with
        # MPY files.  The amount of code and classes implicitly imported
        # by all the SPI and I2C code is too high.  Thus import on demand.
        import adafruit_character_lcd.mcp23008 as mcp23008
        self._mcp = mcp23008.MCP23008(i2c)
        # Setup pins for I2C backpack, see diagram:
        #   https://learn.adafruit.com/assets/35681
        reset = self._mcp.DigitalInOut(_MCP23008_LCD_RS, self._mcp)
        enable = self._mcp.DigitalInOut(_MCP23008_LCD_EN, self._mcp)
        dl4 = self._mcp.DigitalInOut(_MCP23008_LCD_D4, self._mcp)
        dl5 = self._mcp.DigitalInOut(_MCP23008_LCD_D5, self._mcp)
        dl6 = self._mcp.DigitalInOut(_MCP23008_LCD_D6, self._mcp)
        dl7 = self._mcp.DigitalInOut(_MCP23008_LCD_D7, self._mcp)
        backlight = self._mcp.DigitalInOut(_MCP23008_LCD_BACKLIGHT, self._mcp)
        # Call superclass initializer with MCP23008 pins.
        super().__init__(reset, enable, dl4, dl5, dl6, dl7, cols, lines,
                         backlight=backlight)

    def _write8(self, value, char_mode=False):
        # Optimize a command write by changing all GPIO pins at once instead
        # of letting the super class try to set each one invidually (far too
        # slow with overhead of I2C communication).
        gpio = self._mcp.gpio
        # Make sure enable is low.
        gpio = _set_bit(gpio, _MCP23008_LCD_EN, False)
        # Set character/data bit. (charmode = False).
        gpio = _set_bit(gpio, _MCP23008_LCD_RS, char_mode)
        # Set upper 4 bits.
        gpio = _set_bit(gpio, _MCP23008_LCD_D4, ((value >> 4) & 1) > 0)
        gpio = _set_bit(gpio, _MCP23008_LCD_D5, ((value >> 5) & 1) > 0)
        gpio = _set_bit(gpio, _MCP23008_LCD_D6, ((value >> 6) & 1) > 0)
        gpio = _set_bit(gpio, _MCP23008_LCD_D7, ((value >> 7) & 1) > 0)
        self._mcp.gpio = gpio
        # Send command.
        self._pulse_enable()
        # Now repeat for lower 4 bits.
        gpio = self._mcp.gpio
        gpio = _set_bit(gpio, _MCP23008_LCD_EN, False)
        gpio = _set_bit(gpio, _MCP23008_LCD_RS, char_mode)
        gpio = _set_bit(gpio, _MCP23008_LCD_D4, (value & 1) > 0)
        gpio = _set_bit(gpio, _MCP23008_LCD_D5, ((value >> 1) & 1) > 0)
        gpio = _set_bit(gpio, _MCP23008_LCD_D6, ((value >> 2) & 1) > 0)
        gpio = _set_bit(gpio, _MCP23008_LCD_D7, ((value >> 3) & 1) > 0)
        self._mcp.gpio = gpio
        self._pulse_enable()


class Character_LCD_SPI(Character_LCD):
    """Character LCD connected to I2C/SPI backpack using its SPI connection.
    This is a subclass of Character_LCD and implements all of the same
    functions and functionality.
    """

    def __init__(self, spi, latch, cols, lines):
        """Initialize character LCD connectedto backpack using SPI connection
        on the specified SPI bus and latch line with the specified number of
        columns and lines on the display.
        """
        # See comment above on I2C class for why this is imported here:
        import adafruit_character_lcd.shift_reg_74hc595 as shift_reg_74hc595
        self._sr = shift_reg_74hc595.ShiftReg74HC595(spi, latch)
        # Setup pins for SPI backpack, see diagram:
        #   https://learn.adafruit.com/assets/35681
        reset = self._sr.DigitalInOut(_74HC595_LCD_RS, self._sr)
        enable = self._sr.DigitalInOut(_74HC595_LCD_EN, self._sr)
        dl4 = self._sr.DigitalInOut(_74HC595_LCD_D4, self._sr)
        dl5 = self._sr.DigitalInOut(_74HC595_LCD_D5, self._sr)
        dl6 = self._sr.DigitalInOut(_74HC595_LCD_D6, self._sr)
        dl7 = self._sr.DigitalInOut(_74HC595_LCD_D7, self._sr)
        backlight = self._sr.DigitalInOut(_74HC595_LCD_BACKLIGHT, self._sr)
        # Call superclass initializer with shift register pins.
        super().__init__(reset, enable, dl4, dl5, dl6, dl7, cols, lines,
                         backlight=backlight)

    def _write8(self, value, char_mode=False):
        # Optimize a command write by changing all GPIO pins at once instead
        # of letting the super class try to set each one invidually (far too
        # slow with overhead of SPI communication).
        gpio = self._sr.gpio
        # Make sure enable is low.
        gpio = _set_bit(gpio, _74HC595_LCD_EN, False)
        # Set character/data bit. (charmode = False).
        gpio = _set_bit(gpio, _74HC595_LCD_RS, char_mode)
        # Set upper 4 bits.
        gpio = _set_bit(gpio, _74HC595_LCD_D4, ((value >> 4) & 1) > 0)
        gpio = _set_bit(gpio, _74HC595_LCD_D5, ((value >> 5) & 1) > 0)
        gpio = _set_bit(gpio, _74HC595_LCD_D6, ((value >> 6) & 1) > 0)
        gpio = _set_bit(gpio, _74HC595_LCD_D7, ((value >> 7) & 1) > 0)
        self._sr.gpio = gpio
        # Send command.
        self._pulse_enable()
        # Now repeat for lower 4 bits.
        gpio = self._sr.gpio
        gpio = _set_bit(gpio, _74HC595_LCD_EN, False)
        gpio = _set_bit(gpio, _74HC595_LCD_RS, char_mode)
        gpio = _set_bit(gpio, _74HC595_LCD_D4, (value & 1) > 0)
        gpio = _set_bit(gpio, _74HC595_LCD_D5, ((value >> 1) & 1) > 0)
        gpio = _set_bit(gpio, _74HC595_LCD_D6, ((value >> 2) & 1) > 0)
        gpio = _set_bit(gpio, _74HC595_LCD_D7, ((value >> 3) & 1) > 0)
        self._sr.gpio = gpio
        self._pulse_enable()
