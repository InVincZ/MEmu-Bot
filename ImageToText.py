from PIL import Image
from pytesser import *
import os

def readText():
    image_file = os.getcwd() + '\\buttonSnap_levels_current.png'
    #print image_file
    im = Image.open(image_file)
    image_text = image_to_string(im)
    image_text = image_file_to_string(image_file)
    image_text = image_file_to_string(image_file, graceful_errors=True)
    return image_text
