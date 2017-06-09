"""
`char_lcd` -character lcd module 
=================================================
module for interfacing with character lcds
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
		"""initialization interface for character lcds 
		   
		   :param rs: reset pin
		   :param en: enable pin 
		   :param cols: LCD columns
		   :param lines: LCD lines 
		   :param d4: datapin 4
		   :param d5: datapin 4
		   :param d6: datapin 4
		   :param d7: datapin 4
		"""

		#  save col/line state
		self._cols = lcd_columns
		self._lines = lines 
		#  save pin numbers
		self._rs = rs
	   	self._en = en
	    self._d4 = d4
	    self._d5 = d5
	    self._d6 = d6
	    self._d7 = d7
	    #  set all pins as outputs
		for pin in(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7):
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
		self.write8(LCD_DISPLAYCONTROL | displaycontrol)
		#  write displayfunction
		self.write8(LCD_FUNCTIONSET | displayfunction)
		#  set the entry mode
		self.write8(LCD_ENTRYMODESET | displaymode)
		self.clear()

	def home(self):
		self.write8(LCD_RETURNHOME)
		self.microcontroller.delay_us(3000)

	def clear(self):
		self.write8(LCD_CLEARDISPLAY)
		self.microcontroller.delay_us(3000)

	def set_cursor(self, col, row):
		#  move cursor to explicit column/row position
		# Clamp row to the last row of the display
		if row > self._lines:
			row = self._lines - 1 
		# Set location
		self.write8(LCD_SETDDRAMADDR | (col + LCD_ROW_OFFSETS[row]))

	def enable_display(self, enable):
	        """Enable or disable the display.  Set enable to True to enable."""
	        if enable:
	            self.displaycontrol |= LCD_DISPLAYON
	        else:
	            self.displaycontrol &= ~LCD_DISPLAYON
	        self.write8(LCD_DISPLAYCONTROL | self.displaycontrol)


	# write8 function ported
	#  ASSUMES ALL PINS ARE OUTPUT 
	def write8(value):
		#  one ms delay to prevent writing too quickly.
		microcontroller.delay_us(1000)
		#  set character/data bit. (charmode = False)
		lcd_rs.value = 0
		# WRITE upper 4 bits
		lcd_d4.value = ((value >> 4) & 1) > 0
		lcd_d5.value = ((value >> 5) & 1) > 0
		lcd_d6.value = ((value >> 6) & 1) > 0
		lcd_d7.value = ((value >> 7) & 1) > 0
		#  send command
		pulse_enable()
		# WRITE lower 4 bits 
		lcd_d4.value = (value & 1) > 0
		lcd_d5.value = ((value >> 1) & 1) > 0
		lcd_d6.value = ((value >> 2) & 1) > 0
		lcd_d7.value = ((value >> 3) & 1) > 0
		pulse_enable()

	# pulse the clock en line on, off to send cmd
	def pulse_enable():
		lcd_en.value = False 
		# 1microsec pause
		microcontroller.delay_us(1)
		lcd_en.value = True
		microcontroller.delay_us(1)
		lcd_en.value = False
		microcontroller.delay_us(100)

	#  write text to display 
	def message(self, text):
		line = 0
		#  iterate thru each char
		for char in text:
			# if character is \n, go to next line
			if char == '\n':
				line += 1
				#  move to left/right depending on text direction
				col = 0 if self.displaymode & LCD_ENTRYLEFT > 0 else self._cols-1
				self.set_cursor(col, line)
			# Write character to display 
			else:
				self.write8(ord(char), True)






