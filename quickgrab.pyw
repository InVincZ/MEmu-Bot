from PIL import ImageGrab
import os
import time

# Globals
x_pad = 957
y_pad = 497

def screenGrab():
    box = (x_pad+1,y_pad+1,x_pad+1924,y_pad+1114)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + time.strftime("%Y%m%d-%H%M%S") +
'.png', 'PNG')

def main():
    screenGrab()

if __name__ == '__main__':
    main()
