from ssd1306 import SSD1306_I2C
from oled import Write, GFX
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20
import framebuf
import utime

class Screen(SSD1306_I2C):
    
    # screen variables
    width = 128
    height = 64
    line = 1
    highlight = 1
    shift = 0
    list_length = 0
    total_lines = 6
    
    def __init__(self, width, height, iic):
        
        super(Screen, self).__init__(width, height, iic)
        self.width = width
        self.height = height
        self.font15 = Write(self, ubuntu_mono_15)
        self.font20 = Write(self, ubuntu_mono_20)
        
    def welcome(self):
        '''
        Initial splash screen
        '''
        # display logo
        th = bytearray(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xbf\xff\xff\xfe\xbf\xff\xff\xfd\x9f\xff\xff\xfe\x7f\xff\xff\xee\x0f\xff\xff\xeew\xff\xff\xb1\x81\xff\xff\xc9\x8d\xff\xff1\x93\xff\xff0s\xff\xfd\xc9s\xbf\xfe\xceu\x7f\xfe0s\xbf\xfe1\x8c\xbf\xe6\x0epo\xf9\xc9\x8c\x7f\xc6A\x8cg\xfaA\x94W\xc1\xcdLm\xc9\xce\x0c\x9d\xc61\x8c\x9c\xb9\xces\x9d9\xd1\x8b\x9c\xc5\xb2\x92l\xfa\xcdL\x9c\xd61\x8cc\xc61\x8d\x83F\x0et\x1b\xf9\xd6s\x9c\xc51\x8cc\xc61\x8c`\xd9\xces\xfc9\xceL\x939\xd2s\x9c\xf6\xc9\x8cc9\xb6\x03S\xc61\x8d\x9a\xa1\xcerm\xc5\xa9\x93\xac\xc61\x93\x9f\xc9\xcesc9\x0es\xe3\xc5\xb7\x8b\x9c\xa1\xcf\x93\x9c\xf9\xce\xf2`\xc63tb:\xcd\xf3\x939\xafs\x9c\xf61\xf3cF\xcf\xf3\x9f\xca\xcf\xfd\x9c\xda?\x8b\x9c&6\xfec9\xffLo\xff\xc9\xffb\xb9\xfftb6\xce\xff\xdc\xc3\xff\x93\xe4\xfa1\xff\xfb?\xfftc\xd91\xff\xfa\xdf\xffl_:2\xff\xfd?\xff\x8c\x9b\xc6\xce\xff\xff\xff\xff|b\xd9\xce\xff\xff\xff\xff\x8d\xfc\xc91\xff\xff\xff\xff\x8fb:V\xff\xff\xff\xffTl\xfe\xcf\xff\xff\xff\xff\x8d\xff\xd9\xfd\xff\xff\xff\xff\xecc?\xb1\xff\xff\xff\xffs\xfa\xc6*\xff\xff\xff\xffTc\xc7\xce\xff\xff\xff\xff\x8c\xaf\xc6*\xff\xff\xff\xffTb\xfa\xce\xff\xff\xff\xff\x8c\xac9\xb7\xff\xff\xff\xff\xead\xc6.\xff\xff\xff\xff\x8d\x9b\xc6I\xff\xff\xff\xffTb\xc61\xff\xff\xff\xferm\xf9\xd2\xff\xff\xff\xfe\xbc|91\xff\xff\xff\xff\xb3d\xf6.\xff\xff\xff\xfe|}\xc9>\xff\xff\xff\xff\x8b\x9b\xc6M\xff\xff\xff\xff\xf2c\xff\xce\xff\xff\xff\xfe|\\\xc6\xd7\xff\xff\xff\xff\x93c\xfaO\xff\xff\xff\xff\xcc\\&/\xff\xff\xff\xff\xf3\x9c\xc5_\xff\xff\xff\xff\xfb\xa3\xca\x7f\xff\xff\xff\xff\xfec9\xff\xff\xff\xff\xff\xff\\\xc7\xff\xff\xff\xff\xff\xff\xe3\xff\xff\xff\xff\xff\xff\xff\xff\xdf\xff\xff\xff\xff\xff\xff\xfb\xff\xff\xff\xff\xff\xff\xff\xff')
        fb = framebuf.FrameBuffer(th, 64, 64, framebuf.MONO_HLSB)
        self.fill(1)
        self.blit(fb, 32, 0)
        self.show()
        
        # wait for 2 seconds 
        utime.sleep_ms(1000)
        
        # clear
        self.clear()
        
        self.font20.text("Hello Maker!", 14, 25)
        self.show()
        utime.sleep_ms(1000)
        self.clear()
        
    def clear(self):
        '''
        Refresh screen 
        '''
        self.fill(0)
    
    def write_custom(self, m, x, y, font=None):
        '''
        Write text to the screen
        '''
        self.text(m, x, int(y))
        #self.show()
        
    def show_grid(self):
        # draw callibration grid on the screen
        self.hline(1, 1, 1, 64)
        self.show()        
        
    def show_menu(self, menu, line, highlight, shift, list_length, total_lines):
        '''
        This function displays the custom menu for the pikoscope
        '''
        #global line, highlight, shift, list_length
        
        # menu variables
        item = 1
        line = 1
        line_height = 10
        
        # clear the display
        self.fill_rect(0, 0, self.width, self.height, 0)
        
        # shift the list of files so that it shows on the display
        list_length = len(menu)
        short_list = menu[shift:shift+total_lines]
        
        for item in short_list:
            if highlight == line:
                #self.fill_rect(0, (line-1)*line_height, self.width, line_height, 1)
                self.write_custom(">",0, (line-1)*line_height, 0)
                self.write_custom(item, 10, (line-1)*line_height, 0)
                self.show()
            else:
                self.text(item, 10, (line-1)*line_height, 1)
                self.show()
                
            line += 1
        
        self.show()
    

    
        
                   
