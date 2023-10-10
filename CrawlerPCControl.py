import socket
import threading
from pynput import keyboard
import cv2
import sys
import turtle


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from UI_origin import Ui_Form

print("PC start")
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '172.25.13.54'
hostOrange = '172.20.10.12'
hostPC = '172.25.8.147'
hostOuter = '103.46.128.21'
port = 3333

ip = (host, port)
ipOrange = (hostOrange, port)
ipPC = (hostPC, port)
ipOuter = (hostOuter, port)

try:
    mysocket.connect(ip)
    print("successfully connect to the server")
except:
    print("failed to connect")

class sendThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            msgPC = input("\nprint direction:")
            if len(msgPC) > 0:
                mysocket.send(msgPC.encode("utf-8"))

    def send(self, msg):
        msgServer = msg.encode("utf-8")
        if len(msgServer) > 0:
            mysocket.send(msgServer)

class recvThread(QThread):
    dataList = pyqtSignal(list)

    def run(self):
        while True:
            msgServer = mysocket.recv(1024)
            msgList = list(bytes(msgServer))
            self.dataList.emit(msgList)

class UI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        app = QApplication(sys.argv)
        win = UI_control()
        win.show()
        sys.exit(app.exec())



class UI_control(Ui_Form, QtWidgets.QWidget, sendThread):
    def __init__(self):
        super(UI_control, self).__init__()
        self.setupUi(self)
        self.timer_camera = QTimer(self)
        self.cap = cv2.VideoCapture("http://172.25.13.54:8081")
        self.timer_camera.timeout.connect(lambda: self.showStream())
        self.timer_camera.start(10)
        self.showStream()
        self.subThread = recvThread()
        self.subThread.dataList.connect(self.infraredShow)
        self.subThread.start()

    def showStream(self):
        success, frame = self.cap.read()
        #frame = cv2.flip(frame, 1)
        if success:
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.stream.setPixmap(QPixmap.fromImage(img))
            self.timer_camera.start(10)

    def infraredShow(self, msgList):
        if msgList[0] == 0:
            self.left.setStyleSheet("background-color:red;")
        elif msgList[0] == 1:
            self.left.setStyleSheet("background-color:white;")
        if msgList[1] == 0:
            self.right.setStyleSheet("background-color:red;")
        elif msgList[1] == 1:
            self.right.setStyleSheet("background-color:white;")
        if msgList[2] == 0:
            self.back.setStyleSheet("background-color:red;")
        elif msgList[2] == 1:
            self.back.setStyleSheet("background-color:white;")
        if msgList[3] == 0:
            self.front.setStyleSheet("background-color:red;")
        elif msgList[3] == 1:
            self.front.setStyleSheet("background-color:white;")
        dist_mov_avr_z = msgList[4]
        dist_mov_avr_x = msgList[5]
        dist = str(dist_mov_avr_z) + "." + str(dist_mov_avr_x)
        if dist_mov_avr_z == 50:
            self.distAvr.setText(">50")
        else:
            self.distAvr.setText(dist)
        #self.distRight.setText("!: ", distRightAvr)

    @staticmethod
    def leftButton_click():
        sendThread().send("a")

    @staticmethod
    def rightButton_click():
        sendThread().send("d")

    @staticmethod
    def frontButton_click():
        sendThread().send("w")

    @staticmethod
    def backButton_click():
        sendThread().send("s")

    @staticmethod
    def stopButton_click():
        sendThread().send("z")

    @staticmethod
    def sprayButton_click():
        sendThread().send("x")

def on_press(key):
    try:
        #keyboardListen(key.char)
        print('alphanumeric key {0} pressed'.format(key.char))
        sendThread().send(format(key.char))

    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    print('{0} released'.format(key))
    #sendThread().send("z")
    if key == keyboard.Key.esc:
        #Stop listener
        return False

UI = UI()
#mapDrawing = mapDrawing()
UI.start()
#mapDrawing.start()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: listener.join()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = UI_control()
    win.show()
    sys.exit(app.exec())
