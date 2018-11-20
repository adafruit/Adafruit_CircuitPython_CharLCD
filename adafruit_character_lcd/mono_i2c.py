from adafruit_character_lcd.character_lcd import Character_LCD_Mono


class Character_LCD_I2C(Character_LCD_Mono):
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
        """Initialize character LCD connected to backpack using I2C connection
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
