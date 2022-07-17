import random
import time

import cv2 as cv
import keyboard
import numpy as np
import pyautogui
import win32api
from PIL import ImageGrab

time_between_games = 8

x_cursor = [797, 724, 883]
y_cursor = [74, 79, 81]

fishing_rod = (801, 208)

x_indicator = 703
y_indicator = 451
catch_indicator_coord = [x_indicator, y_indicator, 190, 20]

# Фотография попловка
needle_img = cv.imread('area.png', cv.IMREAD_UNCHANGED)


def cursor_coord_func(x_cursor, y_cursor):
    return (x_cursor-15, y_cursor-15, x_cursor + 10, y_cursor + 10)
def catching_fish():
    print('Вытаскиваю')
    global caught_fish
    # time.sleep(0.05)
    # pyautogui.moveTo(827 + random.randint(1,15), 226 + random.randint(1,15))
    # time.sleep(0.05)
    numb = 5
    bias = 5
    time.sleep(0.01)
    pyautogui.mouseDown(button='left')
    print('зажимаю...')
    time.sleep(1.1)
    pyautogui.mouseUp(button='left')
    print('отпустил')
    i = 0
    is_pressed = 0
    while True:
        i += 1
        screenshot = pyautogui.screenshot(region=catch_indicator_coord)
        screenshot2 = pyautogui.screenshot(region=catch_indicator_coord)
        # print(f"Индикатор {i} цвет {screenshot.getpixel((40, 10))}")
        haystack_img = cv.cvtColor(np.array(screenshot.copy()), cv.COLOR_RGB2BGR)
        result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        print(max_val,  i)

        if max_val <= 0.5:
            pyautogui.mouseUp(button='left')
            caught_fish += 1
            print(f'Рыбка {caught_fish}  поймана')
            break

        for j in range(numb+5):
            coord = (70 - j * bias, 10)
            pixel = screenshot.getpixel(coord)
            screenshot2.putpixel(coord, (0, 255, 255))
            if pixel[0] > 130 and pixel[1] > 130 and pixel[2]> 130 and is_pressed == 0:
                is_pressed = 1
                print('зажимаю...')
                pyautogui.mouseDown(button='left')
                break

        for j in range(numb):
            coord = (90 + j * bias, 10)
            pixel = screenshot.getpixel(coord)
            screenshot2.putpixel(coord, (255, 0, 0))
            if pixel[0] > 130 and pixel[1] > 130 and pixel[2] > 130:
                is_pressed = 0
                print('отпустил')
                pyautogui.mouseUp(button='left')

                break

        screenshot2.save(f'f/screen_bar{i}.png')


def pixel_coords():
    time.sleep(0.1)
    pyautogui.moveTo(fishing_rod)

    while True:
        if keyboard.is_pressed('w'):
            print(win32api.GetCursorPos())
            time.sleep(0.1)

def screen_shoting():
    time.sleep(0.1)
    i = 0
    print('Начала фотографирования')
    pyautogui.moveTo(830, 227)
    while True:
        screenshot = ImageGrab.grab(bbox=cursor_coord)
        pixel_color = screenshot.getpixel((10,10))
        diff = abs(pixel_color[2] - pixel_color[1]) + abs(pixel_color[2] - pixel_color[0])
        if keyboard.is_pressed('e'):
            print('программа завершена')
            time.sleep(0.1)
            break
        if pixel_color[2] > pixel_color[1] and pixel_color[2] > pixel_color[0] and diff > 40:
            #(f"поймал {i} цвет {screenshot.getpixel((10, 10))}")
            #screenshot.putpixel((10, 10), (0, 255, 0))
            #screenshot.save(f'f/поймал{i}.png')
            i += 1
            time.sleep(0.5)
        #else:
            #print(f"попловок {i} цвет {screenshot.getpixel((10, 10))}")
            #screenshot.putpixel((10, 10), (0, 255, 0))
            #screenshot.save(f'f/попловок{i}.png')
            # i +=1
            # time.sleep(0.5)

def start_fishing(place_numb):
    cursor_coord = cursor_coord_func(x_cursor[place_numb], y_cursor[place_numb])
    fishing_rod = (x_cursor[place_numb], y_cursor[place_numb])
    fishing_rod_to = (x_cursor[place_numb] - 40, y_cursor[place_numb] - 40)
    print('Начал рыбачить', cursor_coord)
    i = 0
    # mouse movement
    pyautogui.moveTo(fishing_rod)
    pyautogui.mouseDown(button='left')
    time.sleep(2.5)
    pyautogui.mouseUp(button='left')
    pyautogui.moveTo(fishing_rod_to)
    time.sleep(0.1)
    while True:
        screenshot = ImageGrab.grab(bbox=cursor_coord)
        # Aim dote
        color_coord = (16,13)
        pixel_color = screenshot.getpixel(color_coord)
        diff = abs(pixel_color[2] - pixel_color[1]) + abs(pixel_color[2] - pixel_color[0])
        #print(f"Скрин {i} {pixel_color}")
        if (pixel_color[2] > pixel_color[1] and pixel_color[2] > pixel_color[0] and diff > 40)\
                or (pixel_color[1] >110 and pixel_color[0]>110):
            # print(f"скрин{i}поймал {screenshot.getpixel(color_coord)}")
            # screenshot.putpixel(color_coord, (0, 255, 0))
            # screenshot.save(f'f/скрин{i}поймал.png')
            i += 1
            time.sleep(0.01)
            break
        else:
            i += 1
            # screenshot.putpixel(color_coord, (0, 255, 0))
            # screenshot.save(f'f/скрин{i}Попловок.png')


#Основной цикл
while True:

    caught_fish = 0
    if keyboard.is_pressed('q'):
        screen_shoting() # else:
        #     print(f"скрин{i}попловок {screenshot.getpixel(color_coord)}")
        #     screenshot.putpixel(color_coord, (0, 255, 0))
        #     screenshot.save(f'f/скрин{i}попловок.png')
        #     i +=1
    if keyboard.is_pressed('p'):
        pixel_coords()
    if keyboard.is_pressed('f'):
        while True:
            if caught_fish % 10 == 0 and caught_fish != 0:
                time.sleep(40 + random.randint(4,10))
            start_fishing(0)
            catching_fish()
            time.sleep(time_between_games)
    if keyboard.is_pressed('i'):
        catch_fish()
    elif keyboard.is_pressed('e'):
        print('полное заврешение')
        break
