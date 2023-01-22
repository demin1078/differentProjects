import random
import time

import cv2 as cv
import keyboard
import numpy as np
import pyautogui
import win32api
from PIL import ImageGrab
from os import listdir
from os.path import isfile, join
import os
import re

THRESHOLD_CATCH = 0.4
THRESHOLD_BAR = 0.05
PHOTO_PTH = "C:\\Users\\dimag\\differentProjects\\fishing\\PHOTOES"
DEBUG = 0


time_between_games = 7

x_cursor = [1316]
y_cursor = [403]

fishing_rod = (801, 208)

x_indicator = 703
y_indicator = 451
catch_indicator_coord = [x_indicator, y_indicator, 190, 20]

# Фотография бара рыбалки
needle_img = cv.imread('area.png', cv.IMREAD_UNCHANGED)
autorise_img = cv.imread('login.png', cv.IMREAD_UNCHANGED)
abort = cv.imread('reconnecting.png', cv.IMREAD_UNCHANGED)

# hooks
hooks = []
mypath = "hooks/"
all_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for fl in all_files:
    pth = mypath+fl
    hk_img = cv.imread(pth, 0)
    hooks.append(hk_img)

def checkLogouting():
    screenshot = pyautogui.screenshot()
    haystack_img = cv.cvtColor(np.array(screenshot.copy()), cv.COLOR_RGB2BGR)
    result = cv.matchTemplate(haystack_img, abort, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    if max_val >= 0.9:
        print("Вас выкинуло")
        pyautogui.moveTo(max_loc)
        pyautogui.mouseDown(button='left')
        time.sleep(0.2)
        pyautogui.mouseUp(button='left')
    time.sleep(15)
    screenshot = pyautogui.screenshot()
    haystack_img = cv.cvtColor(np.array(screenshot.copy()), cv.COLOR_RGB2BGR)
    result = cv.matchTemplate(haystack_img, autorise_img, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    if max_val >= 0.9:
        print("Вас выкинуло")
        pyautogui.moveTo(max_loc)
        pyautogui.mouseDown(button='left')
        time.sleep(0.2)
        pyautogui.mouseUp(button='left')


def cursor_coord_func(x_cursor, y_cursor):
    return (x_cursor-25, y_cursor-25, x_cursor + 25, y_cursor + 25)


def catching_fish():
    global caught_fish
    # time.sleep(0.05)
    # pyautogui.moveTo(827 + random.randint(1,15), 226 + random.randint(1,15))
    # time.sleep(0.05)
    numb = 5
    bias = 5
    time.sleep(0.01)
    pyautogui.mouseDown(button='left')

    time.sleep(1.1)
    pyautogui.mouseUp(button='left')

    i = 0
    is_pressed = 0
    while True:
        i += 1
        screenshot = pyautogui.screenshot(region=catch_indicator_coord)
        haystack_img = cv.cvtColor(np.array(screenshot.copy()), cv.COLOR_RGB2BGR)
        result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if DEBUG:
            screenshot.save(f"PHOTOES/bar{i}.png")
            print(min_val, max_val, i)
        if max_val <= THRESHOLD_BAR or i >= 1700:
            pyautogui.mouseUp(button='left')
            caught_fish += 1
            print(f'Рыбка {caught_fish}  поймана')
            break

        for j in range(numb + 5):
            coord = (70 - j * bias, 10)
            pixel = screenshot.getpixel(coord)
            if pixel[0] > 130 and pixel[1] > 130 and pixel[2] > 130 and is_pressed == 0:
                is_pressed = 1

                pyautogui.mouseDown(button='left')
                break

        for j in range(numb):
            coord = (90 + j * bias, 10)
            pixel = screenshot.getpixel(coord)
            if pixel[0] > 130 and pixel[1] > 130 and pixel[2] > 130:
                is_pressed = 0

                pyautogui.mouseUp(button='left')

                break
def pixel_coords():
    time.sleep(0.1)
    pyautogui.moveTo(fishing_rod)

    while True:
        if keyboard.is_pressed('w'):
            print(win32api.GetCursorPos())
            time.sleep(0.1)

def start_fishing(place_numb):
    print("Начинаю ловить")
    cursor_coord = cursor_coord_func(x_cursor[place_numb], y_cursor[place_numb])
    fishing_rod = (x_cursor[place_numb], y_cursor[place_numb])
    fishing_rod_to = (x_cursor[place_numb] - 40, y_cursor[place_numb] - 40)

    # mypath = "PHOTOES/"
    # all_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    # max_catch = max([int(re.search("поймал(.*)\.png", f).group(1)) for f in all_files if "поймал" in f])
    # max_hook = max([int(re.search("Попловок(.*)\.png", f).group(1)) for f in all_files if "Попловок" in f])
    # i = max([max_catch, max_hook]) + 1

    i = 0

    pyautogui.moveTo(fishing_rod)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(fishing_rod_to)
    time.sleep(2.5)
    while True:
        screenshot = ImageGrab.grab(bbox=cursor_coord)
        haystack_img = cv.cvtColor(np.array(screenshot.copy()), cv.COLOR_BGR2GRAY)

        maxs = []
        for hook in hooks:
            mtch = cv.matchTemplate(haystack_img, hook, cv.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv.minMaxLoc(mtch)
            maxs.append(max_val)
        average = sum(maxs)/len(maxs)

        # if (pixel_color[2] > pixel_color[1] and pixel_color[2] > pixel_color[0] and diff > 40)\
        #         or (pixel_color[1] >110 and pixel_color[0]>110):

        if DEBUG: (average, i)
        if average <= THRESHOLD_CATCH:
            if DEBUG: screenshot.save(f'{PHOTO_PTH}\поймал{i}.png')
            i += 1
            pyautogui.mouseUp(button='left')
            time.sleep(0.1)
            return 1

        else:
            i += 1
            if DEBUG: screenshot.save(f'{PHOTO_PTH}\Попловок{i}.png')


def change_fl_names():
    mypath = "PHOTOES/"
    all_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    i = 0
    for fl in all_files:
        if "поймал" in fl:
            i +=1
            new_file = fl.replace("поймал", "Попловок")
            if new_file not in all_files:
                os.rename(mypath + fl, mypath + new_file)
    print("Названия заменины")


#Основной цикл
while True:

    caught_fish = 0
    if keyboard.is_pressed('p'):
        print("Была нажата p")
        pixel_coords()
    if keyboard.is_pressed('y'):
        while True:

            # if caught_fish % 13 == 0 and caught_fish != 0:
            #
            #     checkLogouting()
            # else:
            #     time.sleep(time_between_games + random.randint(0,2))
            start_fishing(0)
            catching_fish()
            time.sleep(5)

    if keyboard.is_pressed('i'):
        catch_fish()
    elif keyboard.is_pressed('e'):
        print('полное заврешение')
        break
