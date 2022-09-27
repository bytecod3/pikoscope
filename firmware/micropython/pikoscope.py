from machine import Pin, I2C, ADC
import utime

from ssd1306 import SSD1306_I2C
from screen import Screen
import PikoscopeFunctions
from analog_plot import AnalogPlot
from gfx import GFX

# screen parameters
iic = I2C(0,scl=Pin(1),sda=Pin(0),freq=200000)

# screen variables
width = 128
height = 64
line = 1
highlight = 1
shift = 0
list_length = 0
total_lines = 6

# create screen object
display = Screen(128, 64, iic)

# gfx object to draw shapes on screen
graphics = GFX(128, 64, display.pixel)

# create Rotary encoder object
button_pin = Pin(16, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(17, Pin.IN, Pin.PULL_UP)
step_pin = Pin(18, Pin.IN, Pin.PULL_UP)

# show the splash screen
# display.welcome()

# menu items
menu = [
            'Measure',
            'Callibrate',
            'Voltmeter',
            'Reset',
            'Save',
            'Back'
]

# display the menu
# display.show_menu(menu, line, highlight, shift, list_length, total_lines)

display.grid()

# rotary encoder parameters
previous_value = True
button_down = False

# potentiometer pin
pot = ADC(26)

# voltage conversion factor
conversion_factor = 3.3 / 65535

# analogPlot object
#channel_A = AnalogPlot(display, pot, 120)
#display.grid()
display.screen_header()
display.write_custom("400Hz", 75, 2, color=0)
    
x = 0
# event loop
while True:
    #channel_A.update(x)
    x += 1
    graphics.line(0, 0, 127, 20, 1)
    display.show()

    utime.sleep_ms(20)
