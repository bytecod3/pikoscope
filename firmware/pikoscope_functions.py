

def map(val):
    '''call a function depending on the value that has been pressed'''
    if val == 'Measure':
        measure(45)
    elif val == 'Callibrate':
        callibrate()
    elif val == 'Voltmeter':
        voltmeter()
    elif val == 'Reset':
        reset()
    elif val == 'Save':
        save()
    elif val == 'Back':
        back()
    

def measure(a):
    '''Sample the signal connected to ADC and display'''
    # READ LDR
    #test_sig = ldr.read_u16()
    #volts = round((test_sig * conversion_factor), 2)
    print(a)
    #utime.sleep_ms(10)
    
def callibrate(a):
    pass
    
def voltmeter(a):
    pass
    
def reset(a):
    pass
    
def save(a):
    pass
        
    def back(self, a):
        pass
