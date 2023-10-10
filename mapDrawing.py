import socket
import threading
import time
from pynput import keyboard
import cv2
import sys
import numpy as np
from PIL import Image, ImageTk
import math

class mapDrawing(threading.Thread):
    moving = False

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        bkGround = Image.new("RGB", (500, 500), (255, 255, 255))
        craw = Image.new("RGB", (30, 30), (0, 0, 255))
        self.bkgA = np.array(bkGround)
        self.Craw = np.array(craw)
        self.Crawpos = [0, 0]
        self.position = [self.Crawpos[0]+15, self.Crawpos[1]+15]

        for i in range(self.Crawpos[0], self.Crawpos[0]+30):
            for j in range(self.Crawpos[1], self.Crawpos[1]+30):
                self.bkgA[i][j] = [0, 0, 255]

        bkG = Image.fromarray(self.bkgA)
        bkG.show("Map")

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

    def CrawMove(self):
        for i in range(self.Crawpos[0], self.Crawpos[0]+30):
            for j in range(self.Crawpos[1], self.Crawpos[1]+30):
                self.bkgA[i][j] = [0, 0, 255]

    def showImg(self):
        bkG = Image.fromarray(self.bkgA)
        bkG.show("Map")

    def up(self):
        self.moving = True
        step = 1
        while True:
            self.Crawpos += [1,0]
            self.CrawMove()
            self.showImg()
            time.sleep(0.2)

    def down(self):
        self.moving = True
        step = 1
        while True:
            self.Crawpos += [-1,0]
            self.CrawMove()
            self.showImg()
            time.sleep(0.2)

    '''def right(self):
        turtle.setheading(0)
        self.moving = True
        step = 1
        while self.moving:
            turtle.forward(step)

    def left(self):
        turtle.setheading(180)
        turtle.fd(20)'''


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



