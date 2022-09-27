# this class will handle the live plotting of data that is read from the sensors

class AnalogPlot:
    # constructor
    def __init__(self, pin, max_length=100):
        # max_length -> length of the deque buffer
        # pin -> pin to read data from
        self.buffer = deque([0]*max_len)
        self.max_len = max_length
        
    def add_data(self, data):
        self.add_to_deque(self.buffer, data)
        
    def add_to_deque(self, buf, val):
        # add to deque, pop the oldest value
        buf.pop() # will remove the rightmost element
        buf.appendLeft(val) # add new data to the left of the deque
        
    def update(self, frame_num, value):
        try:
            data = pin.read_u16(); # read analog input pin
            print(data);
            #self.add_data(data)  # add data to deque
             
        except:
            pass