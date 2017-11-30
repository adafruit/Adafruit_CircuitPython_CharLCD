
Introduction
============

This library is compatible with standard Character LCDs such as:
* [Adafruit Standard LCD 16x2](https://www.adafruit.com/product/181)
* [Adafruit RGB backlight negative LCD 16x2](https://www.adafruit.com/product/399)
* [Adafruit RGB backlight negative LCD 20x4](https://www.adafruit.com/product/498)

Compatible with CircuitPython Versions: 2.x

Dependencies
=============
This driver depends on:

* [Adafruit CircuitPython](https://github.com/adafruit/circuitpython "CircuitPython")


Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
[the Adafruit library and driver bundle.](https://github.com/adafruit/Adafruit_CircuitPython_Bundle)

Usage Example
=============

The ``Character_LCD`` class interfaces a predefined Character LCD display with CircuitPython.

    import adafruit_character_lcd

You must define the data pins (``RS``, ``EN``, ``D4``, ``D5``, ``D6``, ``D7``) in your code before using the ``Character_LCD`` class.
If you want to have on/off ``backlight`` functionality, you can also define your backlight as ``lcd_backlight``. Otherwise, the backlight will always remain on. An example of this is below

    lcd_rs = digitalio.DigitalInOut(D7)
    lcd_en = digitalio.DigitalInOut(D8)
    lcd_d7 = digitalio.DigitalInOut(D12)
    lcd_d6 = digitalio.DigitalInOut(D11)
    lcd_d5 = digitalio.DigitalInOut(D10)
    lcd_d4 = digitalio.DigitalInOut(D9)
    lcd_backlight = digitalio.DigitalInOut(D13)

You must also define the size of the CharLCD by specifying its ``lcd_columns`` and ``lcd_rows``:

    lcd_columns = 16
    lcd_rows = 2

After you have set up your LCD, we can make the device by calling it

    lcd = adafruit_character_lcd.Character_LCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)


To verify that your pins are correct, print a hello message to the CharLCD:

    lcd.message('hello\ncircuitpython')


Custom character example with create_char() is provided within /examples/


Contributing
============

Contributions are welcome! Please read our [Code of Conduct](https://github.com/adafruit/Adafruit_CircuitPython_CircuitPython_CharLCD/blob/master/CODE_OF_CONDUCT.md)
before contributing to help this project stay welcoming.

Installation
============

This library is **NOT** built into CircuitPython to make it easy to update. To
install it either follow the directions below or :ref:`install the library bundle <bundle_installation>`.

To install:

#. Download and unzip the `latest release zip <https://github.com/adafruit/Adafruit_CircuitPython_CharLCD/releases>`_.
#. Copy the unzipped ``adafruit_character_lcd`` to the ``lib`` directory on the ``CIRCUITPY`` or ``MICROPYTHON`` drive.

API
===
.. toctree::
    :maxdepth: 3

    api
