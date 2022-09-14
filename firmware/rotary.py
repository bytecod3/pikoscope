from machine import Pin
 
class Rotary:
    def __init__(self, btn_pin, dir_pin, step_pin, highlight, shift, total_lines, list_length):
        self.btn_pin = Pin(btn_pin, Pin.IN, Pin.PULL_UP)
        self.dir_pin = Pin(dir_pin, Pin.IN, Pin.PULL_UP)
        self.step_pin = Pin(step_pin, Pin.IN, Pin.PULL_UP)
        
        self.previous_value = True
        self.btn_down = False
        self.counter = 0
        
        # handler interrupts
        self.btn_pin.irq(handler=self.encoder_handler, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self.dir_pin.irq(handler=self.encoder_handler, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self.step_pin.irq(handler=self.encoder_handler, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
            
    def encoder_handler(self, source):
        if self.previous_value  != self.step_pin.value():
            if self.step_pin.value() == False:
                if self.dir_pin.value() == False:                    
                    # turned right
                    if highlight < total_lines:
                        highlight += 1
                    else:
                        if shift+total_lines < list_length:
                            shift += 1
                    
                else:
                    # turned left
                    if highlight > 1:
                        highlight -= 1
                    else:
                        if shift > 0:
                            shift -= 1
                            
            self.previous_value = self.step_pin.value()
            
        if self.btn_pin.value() == False and not self.btn_down:
            # button press
            print("Button pressed")
            self.btn_down = True
            
        # button debounce
        if self.btn_pin.value() == True and self.btn_down:
            self.btn_down = False

        
        
            
    
    
