import win32api, win32con
from PIL import ImageGrab
from random import randint
import os
import time
import pyautogui
import math
from random import randint, uniform
import pyscreeze
import cv2
import numpy as np
import argparse
import imutils
import glob
import win32gui
import win32process
from pywinauto import Application, win32defines
from pywinauto.win32functions import SetForegroundWindow, ShowWindow
import psutil
from pynput.mouse import Listener
import logging
import sys
import ImageToText

# Globals
windows = []
ProcessXcord_start = 0
ProcessYcord_start = 0
ProcessXlength = 0
ProcessYheight = 0
click_count = 0
program = 'D:\Program Files\Microvirt\MEmu\MEmu.exe'

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
    global ProcessXcord_start
    global ProcessYcord_start
    global ProcessXlength
    global ProcessYheight
    tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
    if pid == current_pid and win32gui.IsWindowVisible(hwnd):
        windows.append(hwnd)
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        #print "Window %s:" % win32gui.GetWindowText(hwnd)
        #print "\tLocation: (%d, %d)" % (x, y)
        #print "\t    Size: (%d, %d)" % (w, h)

        ProcessXcord_start = x
        ProcessYcord_start = y
        ProcessXlength = w
        ProcessYheight = h
        #return ProcessXcord_start, ProcessYcord_start, ProcessXlength, ProcessYheight

def relX(rel_value):
    X_point = ProcessXcord_start + int(round(ProcessXlength * rel_value))
    return X_point

def relY(rel_value):
    Y_point = ProcessYcord_start + int(round(ProcessYheight * rel_value))
    return Y_point

def PrepareWindow(program):
    global window
    global houses
    global menu
    global buttons
    global post
    global people
    global casino
    global events
    global circle
    global monsters
    global gold
    global raid
    global arena
    global guild
    global quests
    global blacksmith
    global tower
    #Bring window in front
    #PrepareWindow("D:\\Program Files\\Microvirt\\MEmu\\MEmu.exe")
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

    #Absolute positions
    window = {'left': (relX(0.784), relY(0.432)), 'right': (relX(0.202), relY(0.085))}
    houses = {'tavern': (relX(0.101), relY(0.687)), 'celestial': (relX(0.549), relY(0.262)), 'casino': (relX(0.541), relY(0.697)), 'casino_small': (relX(0.541), relY(0.697)), 'circle': (relX(0.752), relY(0.778)), 'monsters_left': (relX(0.885), relY(0.554)), 'arena': (relX(0.242), relY(0.725)), 'blacksmith': (relX(0.775), relY(0.768)), 'tower': (relX(0.751), relY(0.432))}
    menu = {'messages': (relX(0.035), relY(0.502)), 'people': (relX(0.035), relY(0.626)), 'guild': (relX(0.688), relY(0.93)), 'events': (relX(0.859), relY(0.112)), 'gold': (relX(0.464), relY(0.081)), 'raid': (relX(0.955), relY(0.214)), 'quests': (relX(0.954), relY(0.472)), 'challenges': (relX(0.937), relY(0.334)), 'seasonal': (relX(0.413), relY(0.935))}
    post = {'claim_all': (relX(0.315), relY(0.207)), 'post_close': (relX(0.852), relY(0.139))}
    people = {'claim_send': (relX(0.722), relY(0.255)), 'monster': (relX(0.838), relY(0.777)), 'scout': (relX(0.503), relY(0.819)), 'ok': (relX(0.503), relY(0.655)), 'people_close': (relX(0.805), relY(0.127))}
    casino = {'common': (relX(0.394), relY(0.645)), 'spin': (relX(0.459), relY(0.429)), 'again': (relX(0.653), relY(0.865)), 'ok': (relX(0.377), relY(0.868)), 'casino_close': (relX(0.034), relY(0.076))}
    events = {'check_in': (relX(0.851), relY(0.821)), 'ok': (relX(0.503), relY(0.654)), 'event_close': (relX(0.937), relY(0.154))}
    circle = {'basic': (relX(0.201), relY(0.731)), 'basic_free': (relX(0.201), relY(0.731)), 'heroic': (relX(0.445), relY(0.723)), 'heroic_free': (relX(0.445), relY(0.723)), 'summon_basic': (relX(0.444), relY(0.786)), 'summon_heroic': (relX(0.444), relY(0.786)), 'ok': (relX(0.315), relY(0.789)), 'circle_close': (relX(0.035), relY(0.075))}
    monsters = {'get': (relX(0.9), relY(0.217)), 'loot': (relX(0.86), relY(0.618)), 'claim': (relX(0.501), relY(0.841)), 'monsters_close': (relX(0.034), relY(0.076)), 'level1': (relX(0.215), relY(0.83)), 'level2': (relX(0.361), relY(0.83)), 'level3': (relX(0.5075), relY(0.83)), 'level4': (relX(0.654), relY(0.83)), 'level5': (relX(0.798), relY(0.83)), 'auto_battle': (relX(0.503), relY(0.863)), 'fight': (relX(0.788), relY(0.422)), 'skip': (relX(0.959), relY(0.07)), 'ok': (relX(0.503), relY(0.826)), 'defeat': (relX(0.501), relY(0.531)), 'defeat_close': (relX(0.033), relY(0.077))}
    gold = {'free': (relX(0.412), relY(0.692)), 'claim': (relX(0.503), relY(0.655)), 'more_gold': (relX(0.538), relY(0.692)), 'gold_close': (relX(0.822), relY(0.242))}
    raid = {'gold': (relX(0.247), relY(0.8)), 'brave': (relX(0.502), relY(0.803)), 'hero': (relX(0.756), relY(0.803)), 'mainmenu_close': (relX(0.885), relY(0.13)), 'submenu_close': (relX(0.797), relY(0.17)), 'battle': (relX(0.789), relY(0.419)), 'skip': (relX(0.959), relY(0.07)), 'next': (relX(0.656), relY(0.827)), 'ok': (relX(0.503), relY(0.826))}
    arena = {'join': (relX(0.656), relY(0.796)), 'battle': (relX(0.803), relY(0.607)), 'refresh': (relX(0.778), relY(0.273)), 'enemy': (relX(0.765), relY(0.797)), 'enemy_battle': (relX(0.788), relY(0.421)), 'ok': (relX(0.503), relY(0.828)), 'arena_close': (relX(0.038), relY(0.071))}
    guild = {'daily': (relX(0.327), relY(0.489)), 'territory': (relX(0.283), relY(0.868)), 'mill': (relX(0.168), relY(0.454)), 'order': (relX(0.502), relY(0.715)), 'order_ok': (relX(0.502), relY(0.87)), 'get_order': (relX(0.729), relY(0.259)), 'submenu_close': (relX(0.824), relY(0.118)), 'close_1': (relX(0.033), relY(0.077)), 'close_2': (relX(0.033), relY(0.077))}
    quests = {'quests_close': (relX(0.83), relY(0.139))}
    blacksmith = {'armor': (relX(0.919), relY(0.496)), 'shoes': (relX(0.922), relY(0.645)), 'amulet': (relX(0.918), relY(0.801)), 'weapon': (relX(0.922), relY(0.341)), 'forge': (relX(0.333), relY(0.838)), 'ok': (relX(0.502), relY(0.654)), 'blacksmith_close': (relX(0.033), relY(0.077))}
    tower = {'battle': (relX(0.503), relY(0.811)), 'tower_battle': (relX(0.788), relY(0.421)), 'skip': (relX(0.959), relY(0.07)), 'ok': (relX(0.503), relY(0.826)), 'defeat': (relX(0.501), relY(0.531)), 'defeat_close': (relX(0.033), relY(0.077))}


def screenGrab(program):
    global im
    #screenGrab('D:\Program Files\Microvirt\MEmu\MEmu.exe')
    #PrepareWindow(program)
    box = (ProcessXcord_start, ProcessYcord_start, ProcessXcord_start + ProcessXlength, ProcessYcord_start + ProcessYheight)
    im = ImageGrab.grab(box)
    #im.save(os.getcwd() + '\\buttonSnap_current.png', 'PNG')
    im = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2RGB)

def fullscreenGrab():
    global im
    box = ()
    im = ImageGrab.grab(box)
    im = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2RGB)
    #im.save(os.getcwd() + '\\full_snap__' + time.strftime("%Y%m%d-%H%M%S") +
#'.png', 'PNG')

def buttonSnap(sets,element):
    global im
    #buttonSnap('menu','messages')
    #program = 'D:\Program Files\Microvirt\MEmu\MEmu.exe'

    #PrepareWindow(program)
    cord = eval(sets + "['" + element + "']")

    spotextension = 0.1
    X_conquest = int(round(float(ProcessXlength) * spotextension))
    Y_conquest = int(round(float(ProcessYheight) * spotextension * 1.5))
    box = (cord[0] - X_conquest, cord[1] - Y_conquest, cord[0] + X_conquest, cord[1] + Y_conquest)
    im = ImageGrab.grab(box)
    im = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2RGB)
    #im.save(os.getcwd() + '\\buttonSnap_current.png', 'PNG')

def buttonSnap_levels(sets,element):
    global im_levels
    #buttonSnap('menu','messages')
    #program = 'D:\Program Files\Microvirt\MEmu\MEmu.exe'

    #PrepareWindow(program)
    cord = eval(sets + "['" + element + "']")

    spotextension = 0.02
    X_conquest = int(round(float(ProcessXlength) * spotextension * 1.5))
    Y_conquest = int(round(float(ProcessYheight) * spotextension * 1.15))
    box = (cord[0] - X_conquest, cord[1] - Y_conquest, cord[0] + X_conquest, cord[1] + Y_conquest)
    im_levels = ImageGrab.grab(box)
    im_levels.save(os.getcwd() + '\\buttonSnap_levels_current.png', 'PNG')
    #im_levels = cv2.cvtColor(np.array(im_levels), cv2.COLOR_BGR2RGB)

def mousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))

def leftClick(cord,delay):
    mousePos((cord[0], cord[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(delay)
    print "Clicked position " + str(cord[0]) + ", " + str(cord[1]) + ": Delay=" + str(delay)         #completely optional. But nice for debugging purposes.

def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    print 'left Down'

def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)
    print 'left release'

def mousemove(x_start,y_start,x_end,y_end):
    mousePos((x_start,y_start))
    leftDown()
    time.sleep(.1)
    pyautogui.dragTo(x_end, y_end, duration=2.0)
    leftUp()

def q():
    x,y = win32api.GetCursorPos()
    print x,y

def r():
    program = 'D:\Program Files\Microvirt\MEmu\MEmu.exe'
    #r('D:\Program Files\Microvirt\MEmu\MEmu.exe')
    PrepareWindow(program)
    x,y = win32api.GetCursorPos()
    xcord_rel = (float(x - ProcessXcord_start) / ProcessXlength) # relative value
    ycord_rel = (float(y - ProcessYcord_start) / ProcessYheight) # relative value

    print "(relX(" + str(round(xcord_rel,3)) + "), relY(" + str(round(ycord_rel,3)) + "))"

def Menu_swipe_left():

    #Swipe left
    #print "(" + str(ProcessXcord_start + int(round(ProcessXlength * 0.784))) + "," + str(ProcessYcord_start + int(round(ProcessYheight * 0.432))) + ")"
    x_start = window['left'][0]
    y_start = window['left'][1]

    x_end = ProcessXcord_start
    y_end = window['left'][1]
    mousemove(x_start,y_start,x_end,y_end)

def Menu_swipe_right():

    #Swipe right
    #print "(" + str(ProcessXcord_start + int(round(ProcessXlength * 0.784))) + "," + str(ProcessYcord_start + int(round(ProcessYheight * 0.432))) + ")"
    x_start = window['right'][0]
    y_start = window['right'][1]

    x_end = ProcessXcord_start + ProcessXlength
    y_end = window['right'][1]
    mousemove(x_start,y_start,x_end,y_end)

def buttonSnippet(x, y, click_count):
    #buttonSnippet((0, 1))
    #Get full screen and crop image afterwards cause of runtime issues
    box = ()
    im = ImageGrab.grab(box)
    #im.save(os.getcwd() + '\\buttonSnippet_current.png', 'PNG')

    if (x >= ProcessXcord_start) and (x <= (ProcessXcord_start + ProcessXlength)) and (y >= ProcessYcord_start) and (y <= (ProcessYcord_start + ProcessYheight)):
        #Calculate clicked button area and save image with position
        spotextension = 0.018
        X_conquest = int(round(float(ProcessXlength) * spotextension))
        Y_conquest = int(round(float(ProcessYheight) * spotextension * 1.3))
        box = (x - X_conquest, y - Y_conquest, x + X_conquest, y + Y_conquest)
        xcord_str = str(round((float(x - ProcessXcord_start) / ProcessXlength),3)) # relative value as str
        ycord_str = str(round((float(y - ProcessYcord_start) / ProcessYheight),3)) # relative value as str
        im2 = im.crop(box)
        im2.save(os.getcwd() + '\\' + str(click_count) + ' - buttonSnippet_position_(relX(' + xcord_str + '), relY(' + ycord_str + ')).png', 'PNG')
        return xcord_str, ycord_str
    else:
        print "Mouse click outside target window! No data logged."
        print "X: " + str(x) + " -- Y: " + str(y)
        xcord_str = None
        ycord_str = None
        return xcord_str, ycord_str

def match2(program, template, im):

    #PrepareWindow(program)

    #imagename = "\\buttonSnap_current.PNG"
    projectpath = os.getcwd() #"C:\\Users\\Michael\\Documents\\Projects\\usr\\bin\\python\\IdleHeroesBot"
    template = projectpath + "\\" + template
    #imagePath = projectpath + imagename
    # Read the images from the file
    #img_rgb = cv2.imread(im)

    template = cv2.imread(template)
    w, h = template.shape[:-1]

    loc = None
    res = cv2.matchTemplate(im, template, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    loc = np.where(res >= threshold)
    #print len(loc[0])
    if len(loc[0]) > 0 and len(loc[1]) > 0:
    #for pt in zip(*loc[::-1]):  # Switch collumns and rows
    #    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    #    print pt
    #    print pt[0] + w, pt[1] + h
        print "Area with requested object found!"
    else:
        print "No area with requested object found! Try again..."
    return len(loc[0]), len(loc[1])
    #cv2.imwrite('result.png', img_rgb)

# logging.basicConfig(filename="mouselog.txt", level=logging.DEBUG, format="%(message)s")
#
# def on_click(x, y, button, pressed):
#     global click_count
#     if pressed:
#         click_count += 1
#         xcord_str, ycord_str = buttonSnippet(x, y, click_count)
#         if (xcord_str != None) and (ycord_str != None):
#             print 'X:' + xcord_str + ' Y:' + ycord_str
#             logging.info("Mouse clicked at: (relX({0}), relY({1}))".format(xcord_str, ycord_str))
#         else:
#             print "Error"

#def on_move(x, y):
#        print ("Mouse moved to ({0}, {1})".format(x, y))

# with Listener(on_click=on_click) as Listener:
#     Listener.join()

def VerifiedClick(sets, element):
    i = 0
    j = 0
    #program = 'D:\Program Files\Microvirt\MEmu\MEmu.exe'
    template = sets + "\\" + element + ".png"

    cord = eval(sets + "['" + element + "']")
    while i < 8:
        buttonSnap(sets,element)
        try:
            len_x, len_y = match2(program,template,im)
            if len_x != 0 and len_y != 0:
                leftClick(((cord[0],cord[1])),.3)
                i = 8
                j = 8
                #return cord[0], cord[1]
            else:
                i += 1
                time.sleep(1)
        except (RuntimeError, TypeError, NameError):
            i += 1
            time.sleep(1)

    if (j == 0):
        #print ("No button found! Bot stops now.")
        raise RuntimeError('No button found! Bot stops now.')
    else:
        pass

def VerifiedClick_except(sets, element, element_2):
    try:
        VerifiedClick(sets, element)
    except Exception, err:
        VerifiedClick(sets, element_2)

def VerifiedClick_any(template, bourne):
    i = 0
    j = 0
    #program = 'D:\Program Files\Microvirt\MEmu\MEmu.exe'
    #imagename = "\\buttonSnap_current.PNG"
    #projectpath = os.getcwd() #"C:\\Users\\Michael\\Documents\\Projects\\usr\\bin\\python\\IdleHeroesBot"
    #imagePath = projectpath + imagename
    template = cv2.imread(template)
    w, h = template.shape[:-1]
    while i < 8:
        screenGrab(program)
        try:
            #img_rgb = cv2.imread(im)
            loc = None
            res = cv2.matchTemplate(im, template, cv2.TM_CCOEFF_NORMED)
            threshold = .8
            loc = np.where(res >= threshold)
            #print len(loc[0])
            if len(loc[0]) > 0 and len(loc[1]) > 0:
                if bourne == 'last':
                    pt = zip(*loc)[len(loc[0])-1]  # Switch collumns and rows
                else:
                    pt = zip(*loc)[0]  # Switch collumns and rows
                #print pt
                buttonclick = (pt[1] + int(round(ProcessXcord_start*1.00875)), pt[0] + int(round(ProcessYcord_start*1.03)))
                #print buttonclick
                print "Area with requested object found!"
                leftClick(buttonclick,1)
                i = 8
                j = 8
            else:
                print "No area with requested object found! Try again..."
                i += 1
                time.sleep(1)
        except (RuntimeError, TypeError, NameError):
            i += 1
            time.sleep(1)
    if (j == 0):
        #print ("No button found! Bot stops now.")
        raise RuntimeError('No button found! Bot stops now.')
    else:
        pass

def FarmPost():

    VerifiedClick('menu', 'messages')
    VerifiedClick('post', 'claim_all')
    VerifiedClick('post', 'post_close')

def FarmPeople():

    VerifiedClick('menu', 'people')
    VerifiedClick('people', 'claim_send')
    VerifiedClick('people', 'monster')
    try:
        VerifiedClick('people', 'scout')
    except:
        pass
    try:
        VerifiedClick('people', 'ok')
    except:
        pass
    time.sleep(1) 
    VerifiedClick('people', 'people_close')

def FarmCasino():

    try:
        VerifiedClick('houses', 'casino')
    except:
        VerifiedClick_any('houses/casino_small.png', 'first')

    VerifiedClick('casino', 'common')
    time.sleep(1)
    VerifiedClick('casino', 'spin')
    VerifiedClick('casino', 'spin')
    VerifiedClick('casino', 'spin')
    time.sleep(.5)
    VerifiedClick('casino', 'again')
    VerifiedClick('casino', 'ok')
    VerifiedClick('casino', 'casino_close')

def FarmEvents():

    VerifiedClick('menu', 'events')
    VerifiedClick('events', 'check_in')
    VerifiedClick('events', 'ok')
    VerifiedClick('events', 'event_close')

def FarmSummonCircle():

    VerifiedClick('houses', 'circle')
    VerifiedClick_except('circle', 'basic', 'basic_free')
    VerifiedClick('circle', 'summon_basic')
    VerifiedClick('circle', 'ok')
    VerifiedClick_except('circle', 'heroic', 'heroic_free')
    VerifiedClick('circle', 'summon_heroic')
    VerifiedClick('circle', 'ok')
    VerifiedClick('circle', 'circle_close')

def FarmMonsters():

    x = 0
    VerifiedClick('houses', 'monsters_left')
    while x < 8:
        try:
            VerifiedClick('monsters', 'get')
            x += 1
        except:
            time.sleep(.25)
    VerifiedClick('monsters', 'loot')
    VerifiedClick('monsters', 'claim')
    VerifiedClick('monsters', 'monsters_close')

def FarmGold():

    VerifiedClick('menu', 'gold')
    VerifiedClick('gold', 'free')
    VerifiedClick('gold', 'claim')
    VerifiedClick('gold', 'more_gold')
    VerifiedClick('gold', 'claim')
    VerifiedClick('gold', 'gold_close')

def FarmRaid():

    VerifiedClick('menu', 'raid')
    menus = ['gold', 'brave', 'hero']
    for x in menus:
        VerifiedClick('raid', x)
        y = 0
        mousemove(relX(0.498), relY(0.81), relX(0.498), relY(0.334))
        mousemove(relX(0.498), relY(0.81), relX(0.498), relY(0.334))
        time.sleep(1)
        while y < 1:
                try:
                    VerifiedClick_any('raid/challenge.png', 'last')
                    y += 1
                except:
                    mousemove(relX(0.498), relY(0.334), relX(0.498), relY(0.5))
                    time.sleep(1)
        VerifiedClick('raid', 'battle')
        time.sleep(.5)
        VerifiedClick('raid', 'skip')
        VerifiedClick('raid', 'next')
        time.sleep(.5)
        VerifiedClick('raid', 'skip')
        VerifiedClick('raid', 'ok')
        VerifiedClick('raid', 'submenu_close')
    VerifiedClick('raid', 'mainmenu_close')

def FarmGuild():
    starts = 0

    VerifiedClick('menu', 'guild')
    VerifiedClick('guild', 'daily')
    VerifiedClick('guild', 'territory')
    VerifiedClick('guild', 'mill')
    time.sleep(1)
    try:
        VerifiedClick('guild', 'order')
        VerifiedClick('guild', 'order_ok')
    except:
        pass
    VerifiedClick('guild', 'get_order')
    mousemove(relX(0.4), relY(0.565), relX(0.766), relY(0.565))
    time.sleep(1)
    while starts < 3:
        try:
            VerifiedClick_any('guild/start.png', 'first')
        except Exception, err:
            #Swipe menu left
            mousemove(relX(0.766), relY(0.565), relX(0.4), relY(0.565))
            time.sleep(1)
            starts += 1
    VerifiedClick('guild', 'submenu_close')
    VerifiedClick('guild', 'close_1')
    VerifiedClick('guild', 'close_2')

def FarmQuests():
    max_clicks = 0

    VerifiedClick('menu', 'quests')
    while max_clicks < 11:
        try:
            VerifiedClick_any('quests/claim.png', 'last')
            max_clicks += 1
        except Exception, err:
            max_clicks = 11
    VerifiedClick('quests', 'quests_close')

def FarmArena():
    starts = 0

    VerifiedClick('houses', 'arena')
    VerifiedClick('arena', 'join')
    for x in range(0, 3):
        VerifiedClick('arena', 'battle')
        VerifiedClick_any('arena/enemy.png', 'last')
        VerifiedClick('arena', 'enemy_battle')
        time.sleep(5)
        leftClick((relX(0.502), relY(0.497)),.3)
        time.sleep(3)
        leftClick((relX(0.503), relY(0.828)),.3)
        VerifiedClick('arena', 'ok')
    VerifiedClick('arena', 'arena_close')

def FarmBlacksmith():
    x = 0
    y = 0
    menus = ['armor', 'shoes', 'amulet', 'weapon']

    VerifiedClick('houses', 'blacksmith')
    time.sleep(1)
    leftClick((relX(0.922), relY(0.341)),.3)
    while (x < 3) or (y < 4):
        try:
            VerifiedClick_any('blacksmith/red_dot.png', 'first')
            time.sleep(1)
            leftClick((relX(0.293), relY(0.627)),.3)

            time.sleep(1)
            leftClick((relX(0.293), relY(0.627)),.3)
            pyautogui.press('left')
            pyautogui.press('left')
            pyautogui.press('left')
            pyautogui.press('del')
            pyautogui.press('del')
            pyautogui.press('del')
            time.sleep(.1)
            pyautogui.typewrite('1')
            leftClick((relX(0.43), relY(0.675)),.3)
            VerifiedClick('blacksmith', 'forge')
            VerifiedClick('blacksmith', 'ok')
            x += 1
            if x == 3:
                y = 4
            else:
                pass
        except:
            if y < 4:
                VerifiedClick('blacksmith', menus[y])
            else:
                pass
            y += 1
    VerifiedClick('blacksmith', 'blacksmith_close')

def FarmTower():
    run = 0
    VerifiedClick('houses', 'tower')
    while run < 1:
        time.sleep(1)
        leftClick((relX(0.536), relY(0.861)),.3)
        VerifiedClick('tower', 'battle')
        VerifiedClick('tower', 'tower_battle')
        VerifiedClick('tower', 'skip')
        try:
            VerifiedClick_any('tower/defeat.png', 'first')
            run = 1
            VerifiedClick('tower', 'defeat_close')
        except:
            VerifiedClick('tower', 'ok')
        time.sleep(.5)

def FarmLevels(stage):
    y = 0
    step = 1
    stage_end = stage - 3
    levels = ['level1', 'level2', 'level3', 'level4', 'level5']
    while step <= stage:
        cord = monsters[levels[y]]
        leftClick(((cord[0],cord[1])),.3)
        print step
        print stage
        #print y
        try:
            VerifiedClick_any('monsters/passed.png', 'first')
            cord = monsters[levels[y+1]]
            leftClick(((cord[0],cord[1])),.3)
            time.sleep(.3)
            VerifiedClick('monsters', 'auto_battle')
            #step = stage
            step += 1
            if (y < 1) or (step > stage_end):
                y += 1
            time.sleep(.3)
        except:
            try:
                time.sleep(1)
                leftClick((relX(0.501), relY(0.619)),.3)
                VerifiedClick('monsters', 'fight')
                VerifiedClick('monsters', 'skip')
                try:
                    VerifiedClick_any('monsters/defeat.png', 'first')
                    step = stage + 1
                    VerifiedClick('monsters', 'defeat_close')
                except:
                    VerifiedClick('monsters', 'ok')
                time.sleep(.5)
                if step == stage:
                    step += 1   
            except:
                step = stage + 1
                
        #buttonSnap_levels('monsters', 'level1')
        #image_text = ImageToText.readText()
        #if '-' in image_text:
        #        level = image_text[0:1]
        #else:
        #    pass

def FullAuto():
    Menu_swipe_right()
    FarmPost()
    FarmPeople()
    FarmCasino()
    FarmEvents()
    FarmSummonCircle()
    FarmMonsters()
    FarmGold()
    FarmRaid()
    FarmGuild()
    Menu_swipe_left()
    FarmArena()
    FarmBlacksmith()
    FarmQuests()
    FarmTower()

def main():
    PrepareWindow(program)

if __name__ == '__main__':
    main()
