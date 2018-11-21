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

"* `Adafruit Character LCDs <http://www.adafruit.com/category/63_96>`_"

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


def _map(xval, in_min, in_max, out_min, out_max):
    # Affine transfer/map with constrained output.
    outrange = float(out_max - out_min)
    inrange = float(in_max - in_min)
    ret = (xval - in_min) * (outrange / inrange) + out_min
    if out_max > out_min:
        ret = max(min(ret, out_max), out_min)
    else:
        ret = max(min(ret, out_min), out_max)
    return ret


# pylint: disable-msg=too-many-instance-attributes
class Character_LCD:
    """Base class for character LCD.

    :param ~digitalio.DigitalInOut rs: The reset data line
    :param ~digitalio.DigitalInOut en: The enable data line
    :param ~digitalio.DigitalInOut d4: The data line 4
    :param ~digitalio.DigitalInOut d5: The data line 5
    :param ~digitalio.DigitalInOut d6: The data line 6
    :param ~digitalio.DigitalInOut d7: The data line 7
    :param columns: The columns on the charLCD
    :param lines: The lines on the charLCD

    """
    LEFT_TO_RIGHT = const(0)
    RIGHT_TO_LEFT = const(1)

    # pylint: disable-msg=too-many-arguments
    def __init__(self, rs, en, d4, d5, d6, d7, columns, lines
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

        # set all pins as outputs
        for pin in(rs, en, d4, d5, d6, d7):
            pin.direction = digitalio.Direction.OUTPUT

        # Initialise the display
        self._write8(0x33)
        self._write8(0x32)
        # Initialise display control
        self.displaycontrol = _LCD_DISPLAYON | _LCD_CURSOROFF | _LCD_BLINKOFF
        # Initialise display function
        self.displayfunction = _LCD_4BITMODE | _LCD_1LINE | _LCD_2LINE | _LCD_5X8DOTS
        # Initialise display mode
        self.displaymode = _LCD_ENTRYLEFT | _LCD_ENTRYSHIFTDECREMENT
        # Write to displaycontrol
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)
        # Write to displayfunction
        self._write8(_LCD_FUNCTIONSET | self.displayfunction)
        # Set entry mode
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
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

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
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

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
        if row >= self.lines:
            row = self.lines - 1
        # Clamp to last column of display
        if column >= self.columns:
            column = self.columns - 1
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
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

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
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

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
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

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
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

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
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

            i2c = busio.I2C(board.SCL, board.SDA)
            lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

            scroll_message = "Scroll -->"
            lcd.message = scroll_message
            time.sleep(2)
            for i in range(len(scroll_message) + 16):
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
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

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


# pylint: disable-msg=too-many-instance-attributes
class Character_LCD_Mono(Character_LCD):
    """Interfaces with monochromatic character LCDs.

        :param ~digitalio.DigitalInOut rs: The reset data line
        :param ~digitalio.DigitalInOut en: The enable data line
        :param ~digitalio.DigitalInOut d4: The data line 4
        :param ~digitalio.DigitalInOut d5: The data line 5
        :param ~digitalio.DigitalInOut d6: The data line 6
        :param ~digitalio.DigitalInOut d7: The data line 7
        :param columns: The columns on the charLCD
        :param lines: The lines on the charLCD
        :param ~digitalio.DigitalInOut backlight_pin: The backlight pin
        :param bool backlight_inverted: ``False`` if LCD is not inverted, i.e. backlight pin is
            connected to common anode. ``True`` if LCD is inverted i.e. backlight pin is connected
            to common cathode.

    """
    # pylint: disable-msg=too-many-arguments
    def __init__(self, rs, en, db4, db5, db6, db7, columns, lines,
                 backlight_pin=None, backlight_inverted=False):

        # Backlight pin and inversion
        self.backlight_pin = backlight_pin
        self.backlight_inverted = backlight_inverted

        #  Setup backlight
        if backlight_pin is not None:
            self.backlight_pin.direction = digitalio.Direction.OUTPUT
            self.backlight = True
        super().__init__(rs, en, db4, db5, db6, db7, columns, lines)
    # pylint: enable-msg=too-many-arguments

    @property
    def backlight(self):
        """Enable or disable backlight. True if backlight is on. False if backlight is off.

        The following example turns the backlight off, then displays, "Hello, world?", then turns
        the backlight on and displays, "Hello, world!"

        .. code-block:: python

            import time
            import board
            import busio
            import adafruit_character_lcd.character_lcd_i2c as character_lcd

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
        if enable:
            self.backlight_pin.value = not self.backlight_inverted
        else:
            self.backlight_pin.value = self.backlight_inverted


class Character_LCD_RGB(Character_LCD):
    """Interfaces with RGB character LCDs.

        :param ~digitalio.DigitalInOut rs: The reset data line
        :param ~digitalio.DigitalInOut en: The enable data line
        :param ~digitalio.DigitalInOut db4: The data line 4
        :param ~digitalio.DigitalInOut db5: The data line 5
        :param ~digitalio.DigitalInOut db6: The data line 6
        :param ~digitalio.DigitalInOut db7: The data line 7
        :param columns: The columns on the charLCD
        :param lines: The lines on the charLCD
        :param ~pulseio.PWMOut, ~digitalio.DigitalInOut red: Red RGB Anode
        :param ~pulseio.PWMOut, ~digitalio.DigitalInOut green: Green RGB Anode
        :param ~pulseio.PWMOut, ~digitalio.DigitalInOut blue: Blue RGB Anode
        :param ~digitalio.DigitalInOut read_write: The rw pin. Determines whether to read to or
            write from the display. Not necessary if only writing to the display. Used on shield.

    """
    # pylint: disable-msg=too-many-arguments
    def __init__(self, rs, en, db4, db5, db6, db7, columns, lines,
                 red, green, blue, read_write=None):

        # Define read_write (rw) pin
        self.read_write = read_write

        # Setup rw pin if used
        if read_write is not None:
            self.read_write.direction = digitalio.Direction.OUTPUT

        # define color params
        self.rgb_led = [red, green, blue]

        for pin in self.rgb_led:
            if hasattr(pin, 'direction'):
                # Assume a digitalio.DigitalInOut or compatible interface:
                pin.direction = digitalio.Direction.OUTPUT
            elif not hasattr(pin, 'duty_cycle'):
                raise TypeError(
                    'RGB LED objects must be instances of digitalio.DigitalInOut'
                    ' or pulseio.PWMOut, or provide a compatible interface.'
                )

        self._color = [0, 0, 0]
        super().__init__(rs, en, db4, db5, db6, db7, columns, lines)

    @property
    def color(self):
        """
        The color of the display. Provide a list of three integers ranging 0 - 100, ``[R, G, B]``.
        ``0`` is no color, or "off". ``100`` is maximum color. For example, the brightest red would
        be ``[100, 0, 0]``, and a half-bright purple would be, ``[50, 0, 50]``.

        If PWM is unavailable, ``0`` is off, and non-zero is on. For example, ``[1, 0, 0]`` would
        be red.

        The following example turns the LCD red and displays, "Hello, world!".

        .. code-block:: python

            import time
            import board
            import busio
            import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

            i2c = busio.I2C(board.SCL, board.SDA)

            lcd = character_lcd.Character_LCD_RGB_I2C(i2c, 16, 2)

            lcd.color = [100, 0, 0]
            lcd.message = "Hello, world!"
            time.sleep(5)
        """
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        for number, pin in enumerate(self.rgb_led):
            if hasattr(pin, 'duty_cycle'):
                # Assume a pulseio.PWMOut or compatible interface and set duty cycle:
                pin.duty_cycle = int(_map(color[number], 0, 100, 65535, 0))
            elif hasattr(pin, 'value'):
                # If we don't have a PWM interface, all we can do is turn each color
                # on / off.  Assume a DigitalInOut (or compatible interface) and write
                # 0 (on) to pin for any value greater than 0, or 1 (off) for 0:
                pin.value = not color[number] > 1
