import socket
import threading
import time
from pynput import keyboard
import cv2
import sys
import numpy as np
import turtle
from PIL import Image, ImageTk
import math

class mapDrawing(threading.Thread):
    moving = False

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        turtle.shape(name="arrow")
        bk = turtle.screensize(500, 500, bg="white")
        turtle.mainloop()

    def CrawerRun(self, char):
        if char == "w":
            self.moving = False
            self.up()
        elif char == "a":
            self.moving = False
            self.left()
        elif char == "d":
            self.moving = False
            self.right()
        elif char == "s":
            self.moving = False
            self.down()

    def up(self):
        turtle.setheading(90)
        self.moving = True
        step = 1
        while self.moving:
            turtle.forward(step)

    def down(self):
        turtle.setheading(-90)
        self.moving = True
        step = 1
        while self.moving:
            turtle.forward(step)

    def right(self):
        turtle.setheading(0)
        self.moving = True
        step = 1
        while self.moving:
            turtle.forward(step)

    def left(self):
        turtle.setheading(180)
        turtle.fd(20)


def on_press(key):
    try:
        #keyboardListen(key.char)
        print('alphanumeric key {0} pressed'.format(key.char))
        mapDrawing().CrawerRun(format(key.char))

        #sendThread().send(format(key.char))

    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    print('{0} released'.format(key))
    #sendThread().send("z")
    if key == keyboard.Key.esc:
        #Stop listener
        return False

map = mapDrawing()
map.start()

with keyboard.Listener(on_press=on_press, on_release = on_release) as listener: listener.join()



