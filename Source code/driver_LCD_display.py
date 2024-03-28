# Prova_LCD_I2C
# Created at 2020-04-19 12:07:19.762516

import i2c

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit

port = None
def LCD_init(i2cPort):
  global port
  port = i2c.I2C(i2cPort, 0x27)
  port.start()
  lcd_write(0x03)
  lcd_write(0x03)
  lcd_write(0x03)
  lcd_write(0x02)

  lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
  lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
  lcd_write(LCD_CLEARDISPLAY)
  lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
  sleep(200)
  


# clocks EN to latch command
def lcd_strobe(data):
  global port
  port.write([data | En | LCD_BACKLIGHT])
  sleep(500, MICROS)
  port.write([((data & ~En) | LCD_BACKLIGHT)])
  sleep(100, MICROS)
  

def lcd_write_four_bits(data):
  global port
  port.write([data | LCD_BACKLIGHT])
  lcd_strobe(data)

# write a command to lcd
def lcd_write(cmd, mode=0):
  lcd_write_four_bits(mode | (cmd & 0xF0))
  lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

# write a character to lcd (or character rom) 0x09: backlight | RS=DR<
# works!
def lcd_write_char(charvalue, mode=1):
  lcd_write_four_bits(mode | (charvalue & 0xF0))
  lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))

# put string function with optional char positioning
def lcd_display_string(string, line=1, pos=0):
    global Rs
    if line == 1:
      pos_new = pos
    elif line == 2:
      pos_new = 0x40 + pos
    elif line == 3:
      pos_new = 0x14 + pos
    elif line == 4:
      pos_new = 0x54 + pos

    lcd_write(0x80 + pos_new)
    
    for char in (string):
      lcd_write(ord(char), Rs)

# clear lcd and set to home
def lcd_clear():
  lcd_write(LCD_CLEARDISPLAY)
  lcd_write(LCD_RETURNHOME)

# define backlight on/off (lcd.backlight(1); off= lcd.backlight(0)
def backlight(state): # for state, 1 = on, 0 = off
  global port
  if state == 1:
     port.write([LCD_BACKLIGHT])
  elif state == 0:
     port.write([LCD_NOBACKLIGHT])

# add custom characters (0 - 7)
def lcd_load_custom_chars(fontdata):
  lcd_write(0x40);
  for char in fontdata:
     for line in char:
        lcd_write_char(line)         
         
def print_on_display(str, time):
    lcd_clear()
    lcd_display_string(str)
    sleep(time)
    lcd_clear()