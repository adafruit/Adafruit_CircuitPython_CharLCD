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
`adafruit_character_lcd.character_lcd_rgb`
====================================================

Character_LCD - module for interfacing with RGB character LCDs

* Author(s):
    -Brent Rubell
    -Asher Lieber
    -Tony DiCola for the original python charLCD library

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
LCD_CURSORON            = const(0x02)
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
LCD_ROW_OFFSETS          = (0x00, 0x40, 0x14, 0x54)

#pylint: enable-msg=bad-whitespace

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


#pylint: disable-msg=too-many-instance-attributes
class Character_LCD_RGB:
    """ Interfaces with a character LCD
        :param ~digitalio.DigitalInOut rs: The reset data line
        :param ~digitalio.DigitalInOut en: The enable data line
        :param ~digitalio.DigitalInOut d4: The data line 4
        :param ~digitalio.DigitalInOut d5: The data line 5
        :param ~digitalio.DigitalInOut d6: The data line 6
        :param ~digitalio.DigitalInOut d7: The data line 7
        :param cols: The columns on the charLCD
        :param lines: The lines on the charLCD
        :param ~pulseio.PWMOut, ~digitalio.DigitalInOut red: Red RGB Anode
        :param ~pulseio.PWMOut, ~digitalio.DigitalInOut green: Green RGB Anode
        :param ~pulseio.PWMOut, ~digitalio.DigitalInOut blue: Blue RGB Anode
        :param ~digitalio.DigitalInOut backlight: The backlight pin, usually the last pin.
            Consult the datasheet.  Note that Pin value 0 means backlight is lit.

    """
    #pylint: disable-msg=too-many-arguments
    def __init__(self, rs, en, d4, d5, d6, d7, cols, lines,
                 red,
                 green,
                 blue,
                 backlight=None
                ):
        self.cols = cols
        self.lines = lines

        # define pin params
        self.reset = rs
        self.enable = en
        self.dl4 = d4
        self.dl5 = d5
        self.dl6 = d6
        self.dl7 = d7

        # define backlight pin
        self.backlight = backlight

        # set all pins as outputs
        for pin in(rs, en, d4, d5, d6, d7):
            pin.direction = digitalio.Direction.OUTPUT

        # setup backlight
        if backlight is not None:
            self.backlight.direction = digitalio.Direction.OUTPUT
            self.backlight.value = 0 # turn backlight on

        # define color params
        self.red = red
        self.green = green
        self.blue = blue
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

        # initialize the display
        self._write8(0x33)
        self._write8(0x32)
        # init. display control
        self.displaycontrol = _LCD_DISPLAYON | _LCD_CURSOROFF | _LCD_BLINKOFF
        # init display function
        self.displayfunction = _LCD_4BITMODE | _LCD_1LINE | _LCD_2LINE | _LCD_5X8DOTS
        # init display mode
        self.displaymode = _LCD_ENTRYLEFT | _LCD_ENTRYSHIFTDECREMENT
        # write to display control
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)
        # write displayfunction
        self._write8(_LCD_FUNCTIONSET | self.displayfunction)
        # set the entry mode
        self._write8(_LCD_ENTRYMODESET | self.displaymode)
        self.clear()
    #pylint: enable-msg=too-many-arguments

    def home(self):
        """Moves the cursor back home pos(1,1)"""
        self._write8(_LCD_RETURNHOME)
        time.sleep(0.003)

    def clear(self):
        """Clears the LCD"""
        self._write8(_LCD_CLEARDISPLAY)
        time.sleep(0.003)

    def show_cursor(self, show):
        """Show or hide the cursor"""
        if show:
            self.displaycontrol |= LCD_CURSORON
        else:
            self.displaycontrol &= ~_LCD_DISPLAYON
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)

    def set_cursor(self, col, row):
        """Sets the cursor to ``row`` and ``col``
            :param col: column location
            :param row: row location
        """
        # Clamp row to the last row of the display
        if row > self.lines:
            row = self.lines - 1
        # Set location
        self._write8(_LCD_SETDDRAMADDR | (col + LCD_ROW_OFFSETS[row]))

    def enable_display(self, enable):
        """Enable or disable the display.
            :param enable: True to enable display, False to disable
        """
        if enable:
            self.displaycontrol |= _LCD_DISPLAYON
        else:
            self.displaycontrol &= ~_LCD_DISPLAYON
        self._write8(_LCD_DISPLAYCONTROL | self.displaycontrol)

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
        """ Set lighton to turn the charLCD backlight on.
            :param lighton: True to turn backlight on, False to turn off
        """
        if lighton:
            self.backlight.value = 0
        else:
            self.backlight.value = 1

    def set_color(self, color):
        """Method to set the duty cycle or the on/off value of the RGB LED
           :param color: list of 3 integers in range(100). ``[R,G,B]`` 0 is no
               color, 100 is maximum color.  If PWM is unavailable, 0 is off and
               non-zero is on.
        """
        for number, pin in enumerate(self.rgb_led):
            if hasattr(pin, 'duty_cycle'):
                # Assume a pulseio.PWMOut or compatible interface and set duty cycle:
                pin.duty_cycle = int(_map(color[number], 0, 100, 65535, 0))
            elif hasattr(pin, 'value'):
                # If we don't have a PWM interface, all we can do is turn each color
                # on / off.  Assume a DigitalInOut (or compatible interface) and write
                # 0 (on) to pin for any value greater than 0, or 1 (off) for 0:
                pin.value = 0 if color[number] > 0 else 1

    def message(self, text):
        """Write text to display, can include \n for newline
            :param text: string to display
        """
        line = 0
        # iterate thru each char
        for char in text:
        # if character is \n, go to next line
            if char == '\n':
                line += 1
                # move to left/right depending on text direction
                col = 0 if self.displaymode & _LCD_ENTRYLEFT > 0 else self.cols-1
                self.set_cursor(col, line)
            # Write character to display
            else:
                self._write8(ord(char), True)

#pylint: enable-msg=too-many-instance-attributes
