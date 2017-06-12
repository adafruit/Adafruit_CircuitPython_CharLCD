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
`adafruit_CircuitPython_CharLCD`
====================================================

TODO(description)

* Author(s): Brent Rubell
"""

import time 
import math
import busio
import digitalio
from board import *


# Commands
LCD_CLEARDISPLAY        = 0x01
LCD_RETURNHOME          = 0x02
LCD_ENTRYMODESET        = 0x04
LCD_DISPLAYCONTROL      = 0x08
LCD_CURSORSHIFT         = 0x10
LCD_FUNCTIONSET         = 0x20
LCD_SETCGRAMADDR        = 0x40
LCD_SETDDRAMADDR        = 0x80

# Entry flags
LCD_ENTRYRIGHT          = 0x00
LCD_ENTRYLEFT           = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# Control flags
LCD_DISPLAYON           = 0x04
LCD_DISPLAYOFF          = 0x00
LCD_CURSORON            = 0x02
LCD_CURSOROFF           = 0x00
LCD_BLINKON             = 0x01
LCD_BLINKOFF            = 0x00

# Move flags
LCD_DISPLAYMOVE         = 0x08
LCD_CURSORMOVE          = 0x00
LCD_MOVERIGHT           = 0x04
LCD_MOVELEFT            = 0x00

# Function set flags
LCD_8BITMODE            = 0x10
LCD_4BITMODE            = 0x00
LCD_2LINE               = 0x08
LCD_1LINE               = 0x00
LCD_5x10DOTS            = 0x04
LCD_5x8DOTS             = 0x00


# Offset for up to 4 rows.
LCD_ROW_OFFSETS         = (0x00, 0x40, 0x14, 0x54)

class cirpyth_char_lcd(object):
	"""Interface to the character lcd."""
	def __init__(self, rs, en, d4, d5, d6, d7, cols, lines):
		self.cols = cols
		self.lines = lines 
		#  save pin numbers
		self.rs = rs
		self.en = en
		self.d4 = d4
		self.d5 = d5
		self.d6 = d6
		self.d7 = d7
		#  set all pins as outputs
		for pin in(rs, en, d4, d5, d6, d7):
			pin.switch_to_output()
		#  initialize the display 
		self.write8(0x33)
		self.write8(0x32)
		#  init. display control
		self.displaycontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
		#  init display function
		self.displayfunction = LCD_4BITMODE | LCD_1LINE | LCD_2LINE | LCD_5x8DOTS
		#  init display mode 
		self.displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
		#  write to display control
		self.write8(LCD_DISPLAYCONTROL | self.displaycontrol)
		#  write displayfunction
		self.write8(LCD_FUNCTIONSET | self.displayfunction)
		#  set the entry mode
		self.write8(LCD_ENTRYMODESET | self.displaymode)
		self.clear()

	def home(self):
		self.write8(LCD_RETURNHOME)
		time.sleep(0.003)

	def clear(self):
		self.write8(LCD_CLEARDISPLAY)
		time.sleep(0.003)

	def show_cursor(self, show):
		if show:
			self.displaycontrol |= LCD_CURSORON
		else:
			self.displaycontrol &= ~LCD_DISPLAYON
		self.write8(LCD_DISPLAYCONTROL | self.displaycontrol)

	def set_cursor(self, col, row):
		#  move cursor to explicit column/row position
		# Clamp row to the last row of the display
		if row > self.lines:
			row = self.lines - 1 
		# Set location
		self.write8(LCD_SETDDRAMADDR | (col + LCD_ROW_OFFSETS[row]))

	def blink(self, blink):
		if blink:
			self.displaycontrol |= LCD_BLINKON
		else:
			self.displaycontrol &= ~LCD_BLINKON
		self.write8(LCD_DISPLAYCONTROL | self.displaycontrol)

	def move_left(self):
		self.write8(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT)

	def move_right(self):
		self.write8(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)

	def set_left_to_right(self):
		self.displaymode |= LCD_ENTRYLEFT
		self.write8(LCD_ENTRYMODESET | self.displaymode)

	def set_left_to_right(self):
		self.displaymode |= LCD_ENTRYLEFT
		self.write8(LCD_ENTRYMODESET | self.displaymode)


	def enable_display(self, enable):
			"""Enable or disable the display.  Set enable to True to enable."""
			if enable:
				self.displaycontrol |= LCD_DISPLAYON
			else:
				self.displaycontrol &= ~LCD_DISPLAYON
			self.write8(LCD_DISPLAYCONTROL | self.displaycontrol)

	def autoscroll(self, autoscroll):
		if autoscroll:
			self.displaymode |= LCD_ENTRYSHIFTINCREMENT
		else:
			self.displaymode &= ~LCD_ENTRYSHIFTINCREMENT
		self.write8(LCD_ENTRYMODESET | self.displaymode)

	# write8 function ported
	#  ASSUMES ALL PINS ARE OUTPUT 
	def write8(self,value, char_mode = False):
		#  one ms delay to prevent writing too quickly.
		time.sleep(0.001)
		#  set character/data bit. (charmode = False)
		self.rs.value = char_mode
		# WRITE upper 4 bits
		self.d4.value = ((value >> 4) & 1) > 0
		self.d5.value = ((value >> 5) & 1) > 0
		self.d6.value = ((value >> 6) & 1) > 0
		self.d7.value = ((value >> 7) & 1) > 0
		#  send command
		self.pulse_enable()
		# WRITE lower 4 bits 
		self.d4.value = (value & 1) > 0
		self.d5.value = ((value >> 1) & 1) > 0
		self.d6.value = ((value >> 2) & 1) > 0
		self.d7.value = ((value >> 3) & 1) > 0
		self.pulse_enable()

	# pulse the clock en line on, off to send cmd
	def pulse_enable(self):
		self.en.value = False 
		# 1microsec pause
		time.sleep(0.0000001)
		self.en.value = True
		time.sleep(0.0000001)
		self.en.value = False
		time.sleep(0.0000001)



	#  write text to display 
	def message(self, text):
		line = 0
		#  iterate thru each char
		for char in text:
			# if character is \n, go to next line
			if char == '\n':
				line += 1
				#  move to left/right depending on text direction
				col = 0 if self.displaymode & LCD_ENTRYLEFT > 0 else self.cols-1
				self.set_cursor(col, line)
			# Write character to display 
			else:
				self.write8(ord(char), True)


	
