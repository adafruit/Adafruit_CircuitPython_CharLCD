import time
import cpython_charlcd as LCD 


#  lcd config
lcd_columns = 16
lcd_rows = 2 

#  metro m0 pin assignment
lcd_rs = digitalio.DigitalInOut(D7)
lcd_en = digitalio.DigitalInOut(D8)
lcd_d7 = digitalio.DigitalInOut(D12)
lcd_d6 = digitalio.DigitalInOut(D11)
lcd_d5 = digitalio.DigitalInOut(D10)
lcd_d4 = digitalio.DigitalInOut(D9)

#  init the lcd class
lcd = LCD

#  print a oneline message
lcd.message('helloworld')
# wait five seconds
time.sleep(5)

