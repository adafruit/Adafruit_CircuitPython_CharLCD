Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-charlcd/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/charlcd/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_CharLCD/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_CharLCD/actions/
    :alt: Build Status

This library is compatible with standard Character LCDs such as:

* `Adafruit Standard LCD 16x2 <https://www.adafruit.com/product/181>`_
* `Adafruit RGB backlight negative LCD 16x2 <https://www.adafruit.com/product/399>`_
* `Adafruit RGB backlight negative LCD 20x4 <https://www.adafruit.com/product/498>`_

Installing from PyPI
--------------------

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-charlcd/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-charlcd

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-charlcd

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-charlcd

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Adafruit CircuitPython BusDevice <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Adafruit CircuitPython MCP230xx <https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx>`_
* `Adafruit CircuitPython 74HC595 <https://github.com/adafruit/Adafruit_CircuitPython_74HC595>`_

I2C & SPI displays also depend on:

* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading the
`Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

The ``Character_LCD`` class interfaces a predefined Character LCD display with CircuitPython.

.. code-block:: python

    import board
    import digitalio
    import adafruit_character_lcd.character_lcd as character_lcd

You must define the data pins (``RS``, ``EN``, ``D4``, ``D5``, ``D6``, ``D7``) in your code before using the ``Character_LCD`` class.
If you want to have on/off ``backlight`` functionality, you can also define your backlight as ``lcd_backlight``. Otherwise, the backlight
will always remain on. The following is an example setup.

.. code-block:: python

    lcd_rs = digitalio.DigitalInOut(board.D7)
    lcd_en = digitalio.DigitalInOut(board.D8)
    lcd_d7 = digitalio.DigitalInOut(board.D12)
    lcd_d6 = digitalio.DigitalInOut(board.D11)
    lcd_d5 = digitalio.DigitalInOut(board.D10)
    lcd_d4 = digitalio.DigitalInOut(board.D9)
    lcd_backlight = digitalio.DigitalInOut(board.D13)

You must also define the size of the CharLCD by specifying its ``lcd_columns`` and ``lcd_rows``:

.. code-block:: python

    lcd_columns = 16
    lcd_rows = 2

After you have set up your LCD, we can make the device by calling it

.. code-block:: python

    lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)


To verify that your pins are correct, print a hello message to the CharLCD:

.. code-block:: python

    lcd.message = "Hello\nCircuitPython"


Custom character example with ``create_char()`` is provided within /examples/


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_CharLCD/blob/master/CODE_OF_CONDUCT.md>`_ before contributing to help this project stay welcoming.


Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
