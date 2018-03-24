# import the necessary packages
import numpy as np
import argparse
import imutils
import glob
import cv2
from PIL import ImageGrab
import os
import time
import win32gui
import win32process
from pywinauto import Application, win32defines
from pywinauto.win32functions import SetForegroundWindow, ShowWindow
import psutil

windows = []
global ProcessXcord_start
global ProcessYcord_start
global ProcessXlength
global ProcessYheight

def WindowInFront(processpath):
        #Bring window in front
        app = Application().connect(path=processpath)
        w = app.top_window()

        #bring window into foreground
        if w.HasStyle(win32defines.WS_MINIMIZE): # if minimized
            ShowWindow(w.wrapper_object(), 9) # restore window state
        else:
            SetForegroundWindow(w.wrapper_object()) #bring to front

def enum_window_callback(hwnd, pid):
    tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
    if pid == current_pid and win32gui.IsWindowVisible(hwnd):
        windows.append(hwnd)
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        print "Window %s:" % win32gui.GetWindowText(hwnd)
        print "\tLocation: (%d, %d)" % (x, y)
        print "\t    Size: (%d, %d)" % (w, h)

        ProcessXcord_start = x
        ProcessYcord_start = y
        ProcessXlength = w
        ProcessYheight = h

# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-t", "--template", required=True, help="Path to template image")
#ap.add_argument("-i", "--images", required=True,
#	help="Path to images where template will be matched")
#ap.add_argument("-v", "--visualize",
#	help="Flag indicating whether or not to visualize each iteration")
#args = vars(ap.parse_args())
def match(program,template):
        #Bring window in front
        #WindowInFront("D:\\Program Files\\Microvirt\\MEmu\\MEmu.exe")
        WindowInFront(program)
        strprogram = str(program)
        #print strprogram
        strprogram_exe = strprogram.split("\\")[-1]
        #print strprogram_exe
        #Get window position
        notepads = [item for item in psutil.process_iter() if item.name() == strprogram_exe]
        #print(notepads)
        pid = next(item for item in psutil.process_iter() if item.name() == strprogram_exe).pid
        #print(pid)

        win32gui.EnumWindows(enum_window_callback, pid)

        # Now windows variable contains a list of hwnds of MEmu
        # Output of captions of the found windows:
        #print([win32gui.GetWindowText(item) for item in windows])

        #Find template on screen
        imagename = "\\Fullscreen_current.PNG"
        projectpath = os.getcwd() #"C:\\Users\\Michael\\Documents\\Projects\\usr\\bin\\python\\IdleHeroesBot"
        template = projectpath + "\\" + template
        imagePath = projectpath + imagename

	#Get current fullscreen
        box = ()
        im = ImageGrab.grab(box)
        im.save(os.getcwd() + imagename
        , 'PNG')

        # load the image image, convert it to grayscale, and detect edges
        template = cv2.imread(template)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 50, 200)
        (tH, tW) = template.shape[:2]
        #cv2.imshow("Template", template)
        #cv2.waitKey()

        # load the image, convert it to grayscale, and initialize the
        # bookkeeping variable to keep track of the matched region
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        found = None

        # loop over the scales of the image
        for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        	# resize the image according to the scale, and keep track
        	# of the ratio of the resizing
        	resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
        	r = gray.shape[1] / float(resized.shape[1])

                # if the resized image is smaller than the template, then break
                # from the loop
        	if resized.shape[0] < tH or resized.shape[1] < tW:
        		break
            # detect edges in the resized, grayscale image and apply template
        	# matching to find the template in the image
        	edged = cv2.Canny(resized, 50, 200)
        	result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
        	(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        	# if we have found a new maximum correlation value, then ipdate
        	# the bookkeeping variable
        	if found is None or maxVal > found[0]:
        		found = (maxVal, maxLoc, r)

        # unpack the bookkeeping varaible and compute the (x, y) coordinates
        # of the bounding box based on the resized ratio
        (_, maxLoc, r) = found
        (buttonstartX, buttonstartY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (buttonendX, buttonendY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
        print "Area of object found: (" + str(buttonstartX) + "," + str(buttonstartY) + "," + str(buttonendX) + "," + str(buttonendY) + ")"

        return buttonstartX, buttonstartY, buttonendX, buttonendY
        # draw a bounding box around the detected result and display the image
        #cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
        #cv2.imshow("Image", image)
        #cv2.waitKey(0)

        #Delete imagename
        #os.remove(imagename + '.png')

def main():
    pass

if __name__ == '__main__':
    main()
