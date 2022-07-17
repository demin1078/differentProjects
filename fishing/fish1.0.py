from PIL import ImageGrab
import time
import keyboard
import win32api
import pyautogui
import random

caught_fish = 0
#(799, 68)
x_cursor = 790
y_cursor = 65
cursor_coord = [x_cursor, y_cursor, x_cursor + 22, y_cursor + 24]
fishing_rod = (801, 208)

x_indicator = 703
y_indicator = 451
catch_indicator_coord = [x_indicator, y_indicator, x_indicator + 120, y_indicator + 20]


def catch_fish():
    print('Вытаскиваю')


    global caught_fish
    # time.sleep(0.05)
    # pyautogui.moveTo(827 + random.randint(1,15), 226 + random.randint(1,15))
    # time.sleep(0.05)

    time.sleep(0.01)
    pyautogui.mouseDown(button='left')
    print('зажимаю...')
    time.sleep(1.1)
    pyautogui.mouseUp(button='left')
    print('отпустил')
    i = 0
    win_counter = 0
    is_pressed = 0
    while True:
        i += 1
        screenshot = ImageGrab.grab(bbox=catch_indicator_coord)
        # print(f"Индикатор {i} цвет {screenshot.getpixel((40, 10))}")
        pixel = screenshot.getpixel((60, 10))ор
        pixel_finish = screenshot.getpixel((80, 10))

        if pixel[0] > 130 and pixel[1] > 130 and pixel[2] > 130 and is_pressed == 0:
            is_pressed = 1
            print('зажимаю...')
            pyautogui.mouseDown(button='left')
            time.sleep(0.05)
            #catching time
        elif pixel_finish[0] > 130 and pixel_finish[1] > 130 and pixel_finish[2] > 130:
            is_pressed = 0
            print('отпустил')
            pyautogui.mouseUp(button='left')
            win_counter += 1
            time.sleep(0.05)
        if i > 400:
            pyautogui.mouseUp(button='left')
            caught_fish += 1
            print(f'Рыбка {caught_fish}  поймана')
            break

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
            print(f"поймал {i} цвет {screenshot.getpixel((10, 10))}")
            screenshot.putpixel((10, 10), (0, 255, 0))
            screenshot.save(f'f/поймал{i}.png')
            i += 1
            time.sleep(0.5)
        else:
            print(f"попловок {i} цвет {screenshot.getpixel((10, 10))}")
            screenshot.putpixel((10, 10), (0, 255, 0))
            screenshot.save(f'f/попловок{i}.png')
            i +=1
            time.sleep(0.5)

def start_fishing():
    print('Начал рыбачить')
    i = 0
    # mouse movement
    pyautogui.moveTo(fishing_rod)
    pyautogui.mouseDown(button='left')
    time.sleep(2)
    pyautogui.mouseUp(button='left')
    while True:
        screenshot = ImageGrab.grab(bbox=cursor_coord)
        color_coord = (10,10)
        pixel_color = screenshot.getpixel(color_coord)
        diff = abs(pixel_color[2] - pixel_color[1]) + abs(pixel_color[2] - pixel_color[0])

        #print(f"Скрин {i} {pixel_color}")
        if (pixel_color[2] > pixel_color[1] and pixel_color[2] > pixel_color[0] and diff > 40)\
                or ( pixel_color[1] >110 and pixel_color[0]>110):
            print(f"скрин{i}поймал {screenshot.getpixel(color_coord)}")
            screenshot.putpixel(color_coord, (0, 255, 0))
            screenshot.save(f'f/скрин{i}поймал.png')
            i += 1
            time.sleep(0.01)
            break
        else:
            i += 1
            screenshot.putpixel(color_coord, (0, 255, 0))
            screenshot.save(f'f/скрин{i}Попловок.png')


#Основной цикл
while True:
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
                time.sleep(30 + random.randint(4,10))
            start_fishing()
            catch_fish()
            time.sleep(4)
    if keyboard.is_pressed('i'):
        catch_fish()
    elif keyboard.is_pressed('e'):
        print('полное заврешение')
        break
