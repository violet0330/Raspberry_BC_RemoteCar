import socket
import threading
import time
from pynput import keyboard
import cv2
import sys

import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from UI_origin import Ui_Form

print("PC start")
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '172.25.13.54'
port = 3333
ip = (host, port)

hostPC = '172.25.8.147'
portPC = 3333
ipPC = (hostPC, portPC)


try:
    mysocket.connect((host, port))
    print("successfully connect to the server")
except:
    print("failed to connect")

class sendThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            msgPC = input("\nprint direction:")
            if len(msgPC)>0:
                mysocket.send(msgPC.encode("utf-8"))

    def send(self, msg):
        msgServer = msg.encode("utf-8")
        if len(msgServer) > 0:
            mysocket.send(msgServer)

class recvThread(QThread):
    dataList = pyqtSignal(list)

    #def __init__(self):
     #   threading.Thread.__init__(self)

    def run(self):
        while True:
            msgServer = mysocket.recv(1024)
            msgList = list(bytes(msgServer))
            #print(msgList, "\n")
            self.dataList.emit(msgList)
            #time.sleep(0.05)
        #mysocket.close()

#send_thread = sendThread()
#send_thread.start()
#recv_thread = recvThread()
#recv_thread.start()


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
            #print("l")
            self.left.setStyleSheet("background-color:red;")
        elif msgList[0] == 1:
            #print("0")
            self.left.setStyleSheet("background-color:white;")
        if msgList[1] == 0:
            #print("r")
            self.right.setStyleSheet("background-color:red;")
        elif msgList[1] == 1:
            #print("0")
            self.right.setStyleSheet("background-color:white;")
        if msgList[2] == 0:
            #print("b")
            self.back.setStyleSheet("background-color:red;")
        elif msgList[2] == 1:
            #print("0")
            self.back.setStyleSheet("background-color:white;")
        if msgList[3] == 0:
            #print("f")
            self.front.setStyleSheet("background-color:red;")
        elif msgList[3] == 1:
            #print("0")
            self.front.setStyleSheet("background-color:white;")

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

def infraredE(msgList):
    if msgList[0] == 0:
        print("l")
        UI_control.setStyleSheet("background-color:red;")
    elif msgList[0] == 1:
        print("0")
        # self.left.setStyleSheet("background-color:white;")
    if msgList[1] == 0:
        print("r")
        # self.right.setStyleSheet("background-color:red;")
    elif msgList[1] == 1:
        print("0")
        # self.right.setStyleSheet("background-color:white;")
    if msgList[2] == 0:
        print("b")
        # self.back.setStyleSheet("background-color:red;")
    elif msgList[2] == 1:
        print("0")
        # self.back.setStyleSheet("background-color:white;")
    if msgList[3] == 0:
        print("f")
        # self.front.setStyleSheet("background-color:red;")
    elif msgList[3] == 1:
        print("0")
        # self.front.setStyleSheet("background-color:white;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = UI_control()
    win.show()
    sys.exit(app.exec())
