# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_character_lcd.character_lcd_rgb_i2c`
====================================================

Module for using I2C with I2C RGB LCD Shield or I2C RGB LCD Pi Plate

* Author(s): Kattni Rembor

Implementation Notes
--------------------

**Hardware:**

* `RGB LCD Shield Kit w/ 16x2 Character Display - Negative Display
  <https://www.adafruit.com/product/714>`_ (Product ID: 714)

* `RGB LCD Shield Kit w/ 16x2 Character Display - Positive Display
  <https://www.adafruit.com/product/716>`_ (Product ID: 716)

* `Adafruit RGB Negative 16x2 LCD+Keypad Kit for Raspberry Pi
  <https://www.adafruit.com/product/1110>`_ (Product ID: 1110)

* `Adafruit RGB Positive 16x2 LCD+Keypad Kit for Raspberry Pi
  <https://www.adafruit.com/product/1109>`_ (Product ID: 1109)

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Bus Device library:
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

"""
try:
    from typing import Optional
    import busio
except ImportError:
    pass

import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017
from adafruit_character_lcd.character_lcd import Character_LCD_RGB

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CharLCD.git"


class Character_LCD_RGB_I2C(Character_LCD_RGB):
    """RGB Character LCD connected to I2C shield or Pi plate using I2C connection.
    This is a subclass of `Character_LCD_RGB` and implements all of the same
    functions and functionality.

    To use, import and initialise as follows:

    .. code-block:: python

        import board
        from adafruit_character_lcd.character_lcd_rgb_i2c import Character_LCD_RGB_I2C

        i2c = board.I2C()  # uses board.SCL and board.SDA
        lcd = Character_LCD_RGB_I2C(i2c, 16, 2)

    """

    def __init__(
        self, i2c: busio.I2C, columns: int, lines: int, address: Optional[int] = None
    ):
        # pylint: disable=too-many-locals
        """Initialize RGB character LCD connected to shield using I2C connection
        on the specified I2C bus with the specified number of columns and lines
        on the display.
        """

        if address:
            mcp = MCP23017(i2c, address=address)
        else:
            mcp = MCP23017(i2c)

        self._left_button = mcp.get_pin(4)
        self._up_button = mcp.get_pin(3)
        self._down_button = mcp.get_pin(2)
        self._right_button = mcp.get_pin(1)
        self._select_button = mcp.get_pin(0)

        self._buttons = [
            self._left_button,
            self._up_button,
            self._down_button,
            self._right_button,
            self._select_button,
        ]

        for pin in self._buttons:
            pin.switch_to_input(pull=digitalio.Pull.UP)

        super().__init__(
            mcp.get_pin(15),
            mcp.get_pin(13),
            mcp.get_pin(12),
            mcp.get_pin(11),
            mcp.get_pin(10),
            mcp.get_pin(9),
            columns,
            lines,
            mcp.get_pin(6),
            mcp.get_pin(7),
            mcp.get_pin(8),
            mcp.get_pin(14),
        )

    @property
    def left_button(self) -> bool:
        """The left button on the RGB Character LCD I2C Shield or Pi plate.

        The following example prints "Left!" to the LCD when the left button is pressed:

        .. code-block:: python

            import board
            from adafruit_character_lcd.character_lcd_rgb_i2c import Character_LCD_RGB_I2C

            i2c = board.I2C()  # uses board.SCL and board.SDA
            lcd = Character_LCD_RGB_I2C(i2c, 16, 2)

            while True:
                if lcd.left_button:
                    lcd.message = "Left!"

        """
        return not self._left_button.value

    @property
    def up_button(self) -> bool:
        """The up button on the RGB Character LCD I2C Shield or Pi plate.

        The following example prints "Up!" to the LCD when the up button is pressed:

        .. code-block:: python

            import board
            from adafruit_character_lcd.character_lcd_rgb_i2c import Character_LCD_RGB_I2C

            i2c = board.I2C()  # uses board.SCL and board.SDA
            lcd = Character_LCD_RGB_I2C(i2c, 16, 2)

            while True:
                if lcd.up_button:
                    lcd.message = "Up!"

        """
        return not self._up_button.value

    @property
    def down_button(self) -> bool:
        """The down button on the RGB Character LCD I2C Shield or Pi plate.

        The following example prints "Down!" to the LCD when the down button is pressed:

        .. code-block:: python

            import board
            from adafruit_character_lcd.character_lcd_rgb_i2c import Character_LCD_RGB_I2C

            i2c = board.I2C()  # uses board.SCL and board.SDA
            lcd = Character_LCD_RGB_I2C(i2c, 16, 2)

            while True:
                if lcd.down_button:
                    lcd.message = "Down!"

        """
        return not self._down_button.value

    @property
    def right_button(self) -> bool:
        """The right button on the RGB Character LCD I2C Shield or Pi plate.

        The following example prints "Right!" to the LCD when the right button is pressed:

        .. code-block:: python

            import board
            from adafruit_character_lcd.character_lcd_rgb_i2c import Character_LCD_RGB_I2C

            i2c = board.I2C()  # uses board.SCL and board.SDA
            lcd = Character_LCD_RGB_I2C(i2c, 16, 2)

            while True:
                if lcd.right_button:
                    lcd.message = "Right!"

        """
        return not self._right_button.value

    @property
    def select_button(self) -> bool:
        """The select button on the RGB Character LCD I2C Shield or Pi plate.

        The following example prints "Select!" to the LCD when the select button is pressed:

        .. code-block:: python

            import board
            from adafruit_character_lcd.character_lcd_rgb_i2c import Character_LCD_RGB_I2C

            i2c = board.I2C()  # uses board.SCL and board.SDA
            lcd = Character_LCD_RGB_I2C(i2c, 16, 2)

            while True:
                if lcd.select_button:
                    lcd.message = "Select!"

        """
        return not self._select_button.value
