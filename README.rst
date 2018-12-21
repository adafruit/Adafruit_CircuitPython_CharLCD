
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-charlcd/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/charlcd/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.com/adafruit/Adafruit_CircuitPython_CharLCD.svg?branch=master
    :target: https://travis-ci.com/adafruit/Adafruit_CircuitPython_CharLCD
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

I2C & SPI displays also depend on:

* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

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

Contributions are welcome! Please read our [Code of Conduct](https://github.com/adafruit/Adafruit_CircuitPython_CircuitPython_CharLCD/blob/master/CODE_OF_CONDUCT.md)
before contributing to help this project stay welcoming.

Installation
============

This library is **NOT** built into CircuitPython to make it easy to update. To
install it either follow the directions below or :ref:`install the library bundle <bundle_installation>`.

To install:

#. Download and unzip the `latest release zip <https://github.com/adafruit/Adafruit_CircuitPython_CharLCD/releases>`_.
#. Copy the unzipped ``adafruit_character_lcd`` to the ``lib`` directory on the ``CIRCUITPY`` or ``MICROPYTHON`` drive.

Building locally
================

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

    source .env/bin/activate

Then run the build:

.. code-block:: shell

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-charlcd --library_location .

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.
