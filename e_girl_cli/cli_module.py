from main import _get_screen, feed, drop, satisfy, pet

import time
import curses
import sys

import keyboard

import subprocess, platform

user = 'test'
last_checksum = ''

import os

def clear():
    os.system('cls||clear')
#     if platform.system()=="Windows":
#         subprocess.Popen("cls", shell=True).communicate()
#     else: #Linux and Mac
#         print("\033c", end="")


def refresh(s):
    clear()
    print(s)

def callback_f():
    # print("Food consumed!")
    feed(user)
    scr, checksum = _get_screen(user)
    refresh(scr)
    
def callback_p():
    # print("Pet!")
    pet(user)
    scr, checksum = _get_screen(user)
    refresh(scr)

def callback_s():
    # print("Satisfied!")
    satisfy(user)
    scr, checksum = _get_screen(user)
    refresh(scr)

def callback_d():
    # print("Satisfied!")
    drop(user)
    scr, checksum = _get_screen(user)
    refresh(scr)

keyboard.on_press_key("f", lambda _:callback_f())
keyboard.on_press_key("p", lambda _:callback_p())
keyboard.on_press_key("s", lambda _:callback_s())
keyboard.on_press_key("d", lambda _:callback_d())

def main():
    while True:
        try:
            scr, checksum = _get_screen(user)
            if checksum != last_checksum:
                refresh(scr)
                last_checksum = checksum
            time.sleep(2)
        except KeyboardInterrupt:
            clear()
            break
    return True