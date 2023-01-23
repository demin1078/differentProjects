import cv2 as cv
import keyboard
import numpy as np
import pyautogui
import win32api
from PIL import ImageGrab
from os import listdir
from os.path import isfile, join
import os
import time, datetime

THRESHOLD_CATCH = 0.3 # 0.4 for ussual # 0.3 for sea
THRESHOLD_BAR = 0.1
PHOTO_PTH = "C:\\Users\\dimag\\differentProjects\\fishing\\PHOTOES"

DEBUG = 0

SEA_MOD = 0
SEA_ARR_NUMB = 6
SEA_ARR = [0] * SEA_ARR_NUMB #5 len

fl = open("food_ts.txt")
FOOD_TIME_LAST = fl.read().split(";")[-2]
FOOD_TIME_LAST = datetime.datetime.strptime(FOOD_TIME_LAST, "%Y-%m-%d %H:%M:%S")
TM_DEL_30 = datetime.timedelta(minutes=30)
fl.close()

time_between_games = 7

x_cursor = [560]
y_cursor = [113]

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
            print(min_val, max_val, i, min_loc, max_loc)
            screenshot.save(f"PHOTOES/bar{i}.png")
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
        mins = []
        for hook in hooks:
            mtch = cv.matchTemplate(haystack_img, hook, cv.TM_CCOEFF_NORMED)
            min_val, max_val, _, _ = cv.minMaxLoc(mtch)
            maxs.append(max_val)
            mins.append(min_val)
        average = sum(maxs)/len(maxs)

        SEA_ARR[int(i % SEA_ARR_NUMB)] = 1 if average < THRESHOLD_CATCH else 0
        if DEBUG: print(average, i, max(maxs), min(mins))
        if ((average <= THRESHOLD_CATCH  or max(maxs) < 0.5)and SEA_MOD == 0) or (SEA_MOD == 1 and all(SEA_ARR)):
            if DEBUG: screenshot.save(f'{PHOTO_PTH}\поймал{i}.png')
            pyautogui.mouseUp(button='left')
            time.sleep(0.1)
            return 1
        else:
            if DEBUG: screenshot.save(f'{PHOTO_PTH}\Попловок{i}.png')
        i += 1


def change_fl_names():
    all_files = [f for f in listdir(mypath) if isfile(join(PHOTO_PTH, f))]
    i = 0
    for fl in all_files:
        if "поймал" in fl:
            i +=1
            new_file = fl.replace("поймал", "Попловок")
            if new_file not in all_files:
                os.rename(mypath + fl, mypath + new_file)
    print("Названия заменины")

# def clean_photo():
#     all_files = [f for f in listdir(PHOTO_PTH) if isfile(join(PHOTO_PTH, f))]
#     print(all_files)
#     print(PHOTO_PTH)
#     for i in all_files:
#         os.remove(PHOTO_PTH)
#         print(PHOTO_PTH + i)
#     print("Photo were deleted")

def eat_food(FOOD_TIME_LAST):
    print("eat food")
    tm_now = datetime.datetime.now()
    print(tm_now - TM_DEL_30)
    print(FOOD_TIME_LAST)
    if tm_now - TM_DEL_30 >= FOOD_TIME_LAST:
        print("time")
        pyautogui.press('2')
        time.sleep(0.2)
        pyautogui.press('2')

        # Write new time in file
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file1 = open("food_ts.txt", "a")  # append mode
        file1.write(f"{now};")
        file1.close()

        FOOD_TIME_LAST =  datetime.datetime.now()

    return FOOD_TIME_LAST



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
            now = datetime.datetime.now()
            if now - TM_DEL_30 >= FOOD_TIME_LAST:
                FOOD_TIME_LAST = eat_food(FOOD_TIME_LAST)

    if keyboard.is_pressed('i'):
        catch_fish()
    elif keyboard.is_pressed('e'):
        print('полное заврешение')
        break
