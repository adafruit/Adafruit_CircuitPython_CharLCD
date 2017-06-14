
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-CircuitPython_CharLCD/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/CircuitPython_CharLCD/en/latest/
    :alt: Documentation Status

.. image :: https://badges.gitter.im/adafruit/circuitpython.svg
    :target: https://gitter.im/adafruit/circuitpython?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
    :alt: Gitter


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

The ``LCD`` class interfaces a predefined Character LCD display with CircuitPython.



.. code-block:: python
    import adafruit_character_lcd as LCD

You must define the data pins (``RS``, ``EN``, ``D4``, ``D5``, ``D6``, ``D7``) in your code before using the ``LCD`` class. 
If you want to have on/off ``backlight`` functionality, you can also define your backlight as ``lcd_backlight``. Otherwise, the backlight will always remain on. An example of this is below

.. code-block:: python
    lcd_rs = digitalio.DigitalInOut(D7)
    lcd_en = digitalio.DigitalInOut(D8)
    lcd_d7 = digitalio.DigitalInOut(D12)
    lcd_d6 = digitalio.DigitalInOut(D11)
    lcd_d5 = digitalio.DigitalInOut(D10)
    lcd_d4 = digitalio.DigitalInOut(D9)
    lcd_backlight = digitalio.DigitalInOut(D13)

You must also define the size of the CharLCD by specifying its ``lcd_columns`` and ``lcd_rows``:

.. code-block 
    lcd_columns = 16
    lcd_rows = 2 

After you have set up your LCD, we can make the device by calling it 

.. code-block::python
    lcd = LCD.cirpyth_char_lcd(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)


To verify that your pins are correct, print a hello message to the CharLCD:

.. code-block::python
    lcd.message('hello\ncircuitpython')
    


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_CircuitPython_CharLCD/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

API Reference
=============

.. toctree::
   :maxdepth: 2

   api