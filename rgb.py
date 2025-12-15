import neopixel
import board
import neopixel
import time
pixels = None
rgb_num = 0
def init(pin,num):
    global pixels,rgb_num
    rgb_num = num
    pixels = neopixel.NeoPixel(pin, num)
def hide(back_list):
    for i in range(rgb_num):
        if i in back_list:
            continue
        pixels[i] = (0,0,0)
class clock():
    st = False
    kick = 0
    def __init__(self,max_angle=360 ):
        if rgb_num<4:
            return
        self.max_angle = max_angle
        self.kick = rgb_num// max_angle
    def lock(self,angle):
        if self.st:
            if angle>self.max_angle:
                return
            p = self.kick//angle
            pixels[p] = (255,255,255)
            hide(p)