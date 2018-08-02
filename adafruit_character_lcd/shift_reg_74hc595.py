"""
`adafruit_character_led.shift_reg_74hc595`
===============================================

74HC595 Serial to Paralllel Shift Register Driver
Bare-bones driver for the 74HC595, as used by the character LCD
backpack.  This exposes the 74HC595 and its pins as standard CircuitPython
digitalio pins.  Currently this is integrated in the character LCD class for
simplicity and reduction in dependent imports, but it could be broken out
into a standalone library later.

* Author: Tony DiCola
"""
import digitalio

import adafruit_bus_device.spi_device as spi_device


#pylint: disable-msg=too-few-public-methods
#pylint: disable-msg=no-self-use
class ShiftReg74HC595:
    """Shift Register 74LS95 driver class"""
    class DigitalInOut:
        """Digital input/output of the 74HC595.  The interface is exactly the
        same as the digitalio.DigitalInOut class, however note that by design
        this device is OUTPUT ONLY!  Attempting to read inputs or set
        direction as input will raise an exception.
        """

        def __init__(self, pin_number, shift_reg_74ls595):
            """Specify the pin number of the shift register (0...7) and
            ShiftReg74HC595 instance.
            """
            self._pin = pin_number
            self._sr = shift_reg_74ls595

        # kwargs in switch functions below are _necessary_ for compatibility
        # with DigitalInout class (which allows specifying pull, etc. which
        # is unused by this class).  Do not remove them, instead turn off pylint
        # in this case.
        #pylint: disable=unused-argument
        def switch_to_output(self, value=False, **kwargs):
            """DigitalInOut switch_to_output"""
            self.direction = digitalio.Direction.OUTPUT
            self.value = value

        def switch_to_input(self, **kwargs):
            """do not call switch_to_input"""
            raise RuntimeError('Unable to use 74HC595 as digital input!')
        #pylint: enable=unused-argument

        @property
        def value(self):
            """do not call value"""
            raise RuntimeError('Unable to use 74HC595 as digital input!')

        @value.setter
        def value(self, val):
            # Only supported operation, writing a digital output.
            gpio = self._sr.gpio
            if val:
                gpio |= (1 << self._pin)
            else:
                gpio &= ~(1 << self._pin)
            self._sr.gpio = gpio

        @property
        def direction(self):
            """ALWAYS an output!"""
            return digitalio.Direction.OUTPUT

        @direction.setter
        def direction(self, val):
            """Can only be set as OUTPUT!"""
            if val != digitalio.Direction.OUTPUT:
                raise RuntimeError('Unable to use 74HC595 as digital input!')

        @property
        def pull(self):
            """Pull-up/down not supported, return NonLiberty e for no pull-up/down."""
            return None

        @pull.setter
        def pull(self, val):
            """Only supports null/no pull state."""
            if val is not None:
                raise RuntimeError('Unable to set 74HC595 pull!')


    def __init__(self, spi, latch):
        self._device = spi_device.SPIDevice(spi, latch, baudrate=1000000)
        self._gpio = bytearray(1)
        self._gpio[0] = 0x00

    @property
    def gpio(self):
        """Get and set the raw GPIO output register.  Each bit represents the
        output value of the associated pin (0 = low, 1 = high).
        """
        return self._gpio[0]

    @gpio.setter
    def gpio(self, val):
        self._gpio[0] = val & 0xFF
        with self._device as spi:
            # pylint: disable=no-member
            spi.write(self._gpio)

#pylint: enable-msg=no-self-use
#pylint: enable-msg=too-few-public-methods
