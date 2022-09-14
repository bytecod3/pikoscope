from machine import Pin, I2C, ADC
import utime

from ssd1306 import SSD1306_I2C
from screen import Screen
import PikoscopeFunctions
from analog_plot import AnalogPlot

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
input_pin = AnalogPlot(pot, max_length=50)

# event loop
while True:
    # read potentiometer value
    #analog_value = pot.read_u16();
    #voltage = analog_value * conversion_factor
    input_pin.update()
    
    # create a buffer to hold up to 100 values
    # once the buffer is full, draw it on the screen and clear to read other incoming data
    
    
    # RUN MENU
    if previous_value != step_pin.value():
        if step_pin.value() == False:

            # Turned Left 
            if direction_pin.value() == False:
                if highlight < total_lines:
                    highlight += 1
                else: 
                    if shift+total_lines < list_length:
                        shift += 1 

            # Turned Right
            else:
                if highlight > 1:
                    highlight -= 1  
                else:
                    
                    if shift > 0:
                        shift -= 1 

            display.show_menu(menu, line, highlight, shift, list_length, total_lines)
            
        previous_value = step_pin.value()   
        
    # Check for button pressed
    if button_pin.value() == False and not button_down:
        button_down = True
    
        PikoscopeFunctions.map(menu[(highlight-1)+shift]) # call the function name currently highlighted on the menu -> see *map* function

    # debounce button
    if button_pin.value() == True and button_down:
        button_down = False
        
    # ---------------------------------------------------------------------

    # give pico time to read. Sleep for 20 milliseconds
    #utime.sleep(20);
    

    
    

