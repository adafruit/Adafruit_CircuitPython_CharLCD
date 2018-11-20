from adafruit_character_lcd.character_lcd import Character_LCD_RGB


class Character_LCD_I2C_RGB(Character_LCD_RGB):
    """RGB Character LCD connected to I2C shield using I2C connection.
    This is a subclass of Character_LCD_RGB and implements all of the same
    functions and functionality.

    To use, import and initialise as follows:

    .. code-block:: python

    import board
    import busio
    import adafruit_character_lcd.character_lcd_rgb as character_lcd

    i2c = busio.I2C(board.SCL, board.SDA)
    lcd = character_lcd.Character_LCD_I2C_RGB(i2c, 16, 2)
    """
    def __init__(self, i2c, columns, lines):
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
