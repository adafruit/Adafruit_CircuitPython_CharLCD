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

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CharLCD.git"

# pylint: disable-msg=bad-whitespace
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
_LCD_ENTRYLEFT           = const(0x02)
_LCD_ENTRYSHIFTDECREMENT = const(0x00)

# Control flags
_LCD_DISPLAYON           = const(0x04)
_LCD_CURSORON            = const(0x02)
_LCD_CURSOROFF           = const(0x00)
_LCD_BLINKON             = const(0x01)
_LCD_BLINKOFF            = const(0x00)

# Move flags
_LCD_DISPLAYMOVE         = const(0x08)
_LCD_MOVERIGHT           = const(0x04)
_LCD_MOVELEFT            = const(0x00)

# Function set flags
_LCD_4BITMODE            = const(0x00)
_LCD_2LINE               = const(0x08)
_LCD_1LINE               = const(0x00)
_LCD_5X8DOTS             = const(0x00)

# Offset for up to 4 rows.
_LCD_ROW_OFFSETS         = (0x00, 0x40, 0x14, 0x54)

# pylint: enable-msg=bad-whitespace


def _set_bit(byte_value, position, val):
    # Given the specified byte_value set the bit at position to the provided
    # boolean value val and return the modified byte.
    ret = None
    if val:
        ret = byte_value | (1 << position)
    else:
        ret = byte_value & ~(1 << position)
    return ret


# pylint: disable-msg=too-many-instance-attributes
class Character_LCD:
    """Base class for character LCD."""
    LEFT_TO_RIGHT = const(0)
    RIGHT_TO_LEFT = const(1)
    """
    Interfaces with a character LCD
    :param ~digitalio.DigitalInOut rs: The reset data line
    :param ~digitalio.DigitalInOut en: The enable data line
    :param ~digitalio.DigitalInOut d4: The data line 4
    :param ~digitalio.DigitalInOut d5: The data line 5
    :param ~digitalio.DigitalInOut d6: The data line 6
    :param ~digitalio.DigitalInOut d7: The data line 7
    :param columns: The columns on the charLCD
    :param lines: The lines on the charLCD
    :param ~digitalio.DigitalInOut backlight_pin: The backlight pin, usually
    the last pin. Check with your datasheet
    :param bool backlight_inverted: False if LCD is not inverted, i.e. backlight pin is connected
    to common anode. True if LCD is inverted i.e. backlight pin is connected to common cathode.

    """
    # pylint: disable-msg=too-many-arguments
    def __init__(self, rs, en, d4, d5, d6, d7, columns, lines,
                 backlight_pin=None,
                 backlight_inverted=False
                ):

        self.columns = columns
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
        self._direction = None
    # pylint: enable-msg=too-many-arguments

    def home(self):
        """Moves the cursor "home" to position (1, 1)."""
        self._write8(_LCD_RETURNHOME)
        time.sleep(0.003)

    def clear(self):
        """Clears everything displayed on the LCD.

        The following example displays, "Hello, world!", then clears the LCD.

        .. code-block:: python

            import time
            import board
            import busio
            import adafruit_character_lcd.character_lcd_mono as character_lcd

            i2c = busio.I2C(board.SCL, board.SDA)

            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            lcd.message = "Hello, world!"
            time.sleep(5)
            lcd.clear()
        """
        self._write8(_LCD_CLEARDISPLAY)
        time.sleep(0.003)

    @property
    def cursor(self):
        """True if cursor is visible. False to stop displaying the cursor.

        The following example shows the cursor after a displayed message:

        .. code-block:: python

            import time
            import board
            import busio
            import adafruit_character_lcd.character_lcd_mono as character_lcd

            i2c = busio.I2C(board.SCL, board.SDA)

            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            lcd.cursor = True
            lcd.message = "Cursor! "
            time.sleep(5)

        """
        return self.displaycontrol & _LCD_CURSORON == _LCD_CURSORON

    @cursor.setter
    def cursor(self, show):
        if show:
            self.displaycontrol |= _LCD_CURSORON
        else:
            self.displaycontrol &= ~_LCD_CURSORON
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)

    def cursor_position(self, column, row):
        """Move the cursor to position ``column``, ``row``

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
        """
        Blink the cursor. True to blink the cursor. False to stop blinking.

        The following example shows a message followed by a blinking cursor for five seconds.

        .. code-block:: python

            import time
            import board
            import busio
            import adafruit_character_lcd.character_lcd_mono as character_lcd

            i2c = busio.I2C(board.SCL, board.SDA)

            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            lcd.blink = True
            lcd.message = "Blinky cursor!"
            time.sleep(5)
            lcd.blink = False
        """
        return self.displaycontrol & _LCD_BLINKON == _LCD_BLINKON

    @blink.setter
    def blink(self, blink):
        if blink:
            self.displaycontrol |= _LCD_BLINKON
        else:
            self.displaycontrol &= ~_LCD_BLINKON
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)

    @property
    def display(self):
        """
        Enable or disable the display. True to enable the display. False to disable the display.

        The following example displays, "Hello, world!" on the LCD and then turns the display off.

        .. code-block:: python

            import time
            import board
            import busio
            import adafruit_character_lcd.character_lcd_mono as character_lcd

            i2c = busio.I2C(board.SCL, board.SDA)

            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            lcd.message = "Hello, world!"
            time.sleep(5)
            lcd.display = False
        """
        return self.displaycontrol & _LCD_DISPLAYON == _LCD_DISPLAYON

    @display.setter
    def display(self, enable):
        if enable:
            self.displaycontrol |= _LCD_DISPLAYON
        else:
            self.displaycontrol &= ~_LCD_DISPLAYON
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)

    @property
    def message(self):
        """Display a string of text on the character LCD.

        The following example displays, "Hello, world!" on the LCD.

        .. code-block:: python

            import time
            import board
            import busio
            import adafruit_character_lcd.character_lcd_mono as character_lcd

            i2c = busio.I2C(board.SCL, board.SDA)

            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            lcd.message = "Hello, world!"
            time.sleep(5)
        """
        return self._message

    @message.setter
    def message(self, message):
        self._message = message
        line = 0
        # Track times through iteration, to act on the initial character of the message
        initial_character = 0
        # iterate through each character
        for character in message:
            # If this is the first character in the string:
            if initial_character == 0:
                # Start at (1, 1) unless direction is set right to left, in which case start
                # on the opposite side of the display.
                col = 0 if self.displaymode & _LCD_ENTRYLEFT > 0 else self.columns - 1
                self.cursor_position(col, line)
                initial_character += 1
            # If character is \n, go to next line
            if character == '\n':
                line += 1
                # Start the second line at (1, 1) unless direction is set right to left in which
                # case start on the opposite side of the display.
                col = 0 if self.displaymode & _LCD_ENTRYLEFT > 0 else self.columns - 1
                self.cursor_position(col, line)
            # Write string to display
            else:
                self._write8(ord(character), True)

    def move_left(self):
        """Moves displayed text left one column.

        The following example scrolls a message to the left off the screen.

        .. code-block:: python

            import time
            import board
            import busio
            import adafruit_character_lcd.character_lcd_mono as character_lcd

            i2c = busio.I2C(board.SCL, board.SDA)

            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            scroll_message = "<-- Scroll"
            lcd.message = scroll_message
            time.sleep(2)
            for i in range(len(scroll_message)):
                lcd.move_left()
                time.sleep(0.5)
        """
        self._write8(_LCD_CURSORSHIFT | _LCD_DISPLAYMOVE | _LCD_MOVELEFT)

    def move_right(self):
        """Moves displayed text right one column.

        The following example scrolls a message to the right off the screen.

        .. code-block:: python

            import time
            import board
            import busio
            import adafruit_character_lcd.character_lcd_mono as character_lcd

            i2c = busio.I2C(board.SCL, board.SDA)

            lcd_columns = 16
            lcd_rows = 2

            lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)

            scroll_message = "Scroll -->"
            lcd.message = scroll_message
            time.sleep(2)
            for i in range(len(scroll_message) + lcd_columns):
                lcd.move_right()
                time.sleep(0.5)
        """
        self._write8(_LCD_CURSORSHIFT | _LCD_DISPLAYMOVE | _LCD_MOVERIGHT)

    @property
    def text_direction(self):
        """The direction the text is displayed. To display the text left to right beginning on the
        left side of the LCD, set ``text_direction = LEFT_TO_RIGHT``. To display the text right
        to left beginning on the right size of the LCD, set ``text_direction = RIGHT_TO_LEFT``.
        Text defaults to displaying from left to right.

        The following example displays "Hello, world!" from right to left.

        .. code-block:: python

            import time
            import board
            import busio
            import adafruit_character_lcd.character_lcd_mono as character_lcd

            i2c = busio.I2C(board.SCL, board.SDA)

            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            lcd.text_direction = lcd.RIGHT_TO_LEFT
            lcd.message = "Hello, world!"
            time.sleep(5)
        """
        return self._direction

    @text_direction.setter
    def text_direction(self, direction):
        self._direction = direction
        if direction == self.LEFT_TO_RIGHT:
            self._left_to_right()
        elif direction == self.RIGHT_TO_LEFT:
            self._right_to_left()

    def _left_to_right(self):
        # Displays text from left to right on the LCD.
        self.displaymode |= _LCD_ENTRYLEFT
        self._write8(_LCD_ENTRYMODESET | self.displaymode)

    def _right_to_left(self):
        # Displays text from right to left on the LCD.
        self.displaymode &= ~_LCD_ENTRYLEFT
        self._write8(_LCD_ENTRYMODESET | self.displaymode)

    @property
    def backlight(self):
        """Enable or disable backlight. True if backlight is on. False if backlight is off.

        The following example turns the backlight off, then displays, "Hello, world?", then turns
        the backlight on and displays, "Hello, world!"

        .. code-block:: python

            import time
            import board
            import busio
            import adafruit_character_lcd.character_lcd_mono as character_lcd

            i2c = busio.I2C(board.SCL, board.SDA)

            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            lcd.backlight = False
            lcd.message = "Hello, world?"
            time.sleep(5)
            lcd.backlight = True
            lcd.message = "Hello, world!"
            time.sleep(5)

        """
        return self._enable

    @backlight.setter
    def backlight(self, enable):
        self._enable = enable
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
        To show your custom character use, for example, ``lcd.message = "\x01"``

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
    """Character LCD connected to I2C/SPI backpack using its I2C connection.
    This is a subclass of Character_LCD and implements all of the same
    functions and functionality.

    To use, import and initialise as follows:

    .. code-block:: python

    import board
    import busio
    import adafruit_character_lcd.character_lcd_mono as character_lcd

    i2c = busio.I2C(board.SCL, board.SDA)
    lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)
    """
    def __init__(self, i2c, columns, lines, backlight_inverted=False):
        """Initialize character LCD connectedto backpack using I2C connection
        on the specified I2C bus with the specified number of columns and
        lines on the display. Optionally specify if backlight is inverted.
        """
        import adafruit_mcp230xx
        self._mcp = adafruit_mcp230xx.MCP23008(i2c)
        reset = self._mcp.get_pin(1)
        enable = self._mcp.get_pin(2)
        db4 = self._mcp.get_pin(3)
        db5 = self._mcp.get_pin(4)
        db6 = self._mcp.get_pin(5)
        db7 = self._mcp.get_pin(6)
        backlight_pin = self._mcp.get_pin(7)
        self.backlight_inverted = backlight_inverted
        super().__init__(reset, enable, db4, db5, db6, db7, columns, lines,
                         backlight_pin=backlight_pin, backlight_inverted=backlight_inverted)


class Character_LCD_SPI(Character_LCD):
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
        import adafruit_74hc595
        self._shift_register = adafruit_74hc595.ShiftRegister74HC595(spi, latch)
        reset = self._shift_register.get_pin(1)
        enable = self._shift_register.get_pin(2)
        db4 = self._shift_register.get_pin(6)
        db5 = self._shift_register.get_pin(5)
        db6 = self._shift_register.get_pin(4)
        db7 = self._shift_register.get_pin(3)
        backlight_pin = self._shift_register.get_pin(7)
        self.backlight_inverted = backlight_inverted
        super().__init__(reset, enable, db4, db5, db6, db7, columns, lines,
                         backlight_pin=backlight_pin, backlight_inverted=backlight_inverted)
