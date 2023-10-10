import RPi.GPIO as GPIO
import socket
import threading
import time
import math
import os

from infrared import CrawlerInfrared
from ultrasonicLeft import CrawlerUltrasoundLeft
from ultrasonicRight import CrawlerUltrasoundRight


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
print("Raspberry start")

sbuflen = 8192*2
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = "172.25.13.54"
hostOrange = "172.20.10.15"
hostPC = '172.25.8.147'
hostOuter = '103.46.128.21'

port = 3333
ip = (host, port)
ipOrange = (hostOrange, port)
ipPC = (hostPC, port)
ipOuter = (hostOuter, port)

mySocket.bind(ip)
mySocket.listen(5)

try:
    client, address = mySocket.accept()
    print("new connection")
except:
    print("failed to accept")


class CrawlerMove(object):
    def __init__(self):
        self.GPIO_motor_left_ENA = 17
        self.GPIO_motor_left_IN1 = 27
        self.GPIO_motor_left_IN2 = 22
        self.GPIO_motor_right_ENA = 14
        self.GPIO_motor_right_IN1 = 15
        self.GPIO_motor_right_IN2 = 18

        GPIO.setup(self.GPIO_motor_left_ENA, GPIO.OUT)
        GPIO.setup(self.GPIO_motor_left_IN1, GPIO.OUT)
        GPIO.setup(self.GPIO_motor_left_IN2, GPIO.OUT)
        GPIO.setup(self.GPIO_motor_right_ENA, GPIO.OUT)
        GPIO.setup(self.GPIO_motor_right_IN1, GPIO.OUT)
        GPIO.setup(self.GPIO_motor_right_IN2, GPIO.OUT)

        self.motor_left = GPIO.PWM(self.GPIO_motor_left_ENA, 500)
        self.motor_right = GPIO.PWM(self.GPIO_motor_right_ENA, 500)
        self.motor_left.start(0)
        self.motor_right.start(0)

    def rotate_left(self):
        GPIO.output(self.GPIO_motor_left_IN1, 1)
        GPIO.output(self.GPIO_motor_left_IN2, 0)

    def rotate_right(self):
        GPIO.output(self.GPIO_motor_right_IN1, 1)
        GPIO.output(self.GPIO_motor_right_IN2, 0)

    def reverse_left(self):
        GPIO.output(self.GPIO_motor_left_IN1, 0)
        GPIO.output(self.GPIO_motor_left_IN2, 1)

    def reverse_right(self):
        GPIO.output(self.GPIO_motor_right_IN1, 0)
        GPIO.output(self.GPIO_motor_right_IN2, 1)

    def stop(self):
        print("stop")
        self.motor_left.ChangeDutyCycle(0)
        self.motor_right.ChangeDutyCycle(0)

    def forward(self, speed):
        print("forw")
        self.rotate_left()
        self.rotate_right()
        self.motor_left.ChangeDutyCycle(speed)
        self.motor_right.ChangeDutyCycle(speed)

    def backward(self, speed):
        print("back")
        self.reverse_left()
        self.reverse_right()
        self.motor_left.ChangeDutyCycle(speed)
        self.motor_right.ChangeDutyCycle(speed)

    def turn_left_inSitu(self, speed):
        print("turn l")
        self.reverse_left()
        self.rotate_right()
        self.motor_left.ChangeDutyCycle(speed)
        self.motor_right.ChangeDutyCycle(speed)

    def turn_right_inSitu(self, speed):
        print("turn r")
        self.rotate_left()
        self.reverse_right()
        self.motor_left.ChangeDutyCycle(speed)
        self.motor_right.ChangeDutyCycle(speed)

    def turn_dif_for(self, speedL, delta):
        self.rotate_left()
        self.rotate_right()
        self.motor_left.ChangeDutyCycle(speedL)
        self.motor_right.ChangeDutyCycle(speedL + delta)

    def turn_dif_back(self, speedL, delta):
        self.reverse_left()
        self.reverse_right()
        self.motor_left.ChangeDutyCycle(speedL)
        self.motor_right.ChangeDutyCycle(speedL + delta)


class waterPump(object):
    def __init__(self):
        self.GPIO_Pump_forward = 5
        self.GPIO_Pump_up = 6
        self.GPIO_WaterPump = 16

        GPIO.setup(self.GPIO_Pump_bottom, GPIO.OUT)
        GPIO.setup(self.GPIO_Pump_forward, GPIO.OUT)
        GPIO.setup(self.GPIO_Pump_up, GPIO.OUT)
        GPIO.setup(self.GPIO_WaterPump, GPIO.OUT)

        self.MG90_bottom = GPIO.PWM(self.GPIO_Pump_bottom, 50)
        self.MG90_forward = GPIO.PWM(self.GPIO_Pump_forward, 50)
        self.MG90_up = GPIO.PWM(self.GPIO_Pump_up, 50)
        self.WaterPump = GPIO.PWM(self.GPIO_WaterPump, 500)

        self.MG90_bottom.start(0)
        self.MG90_forward.start(0)
        self.MG90_up.start(0)
        self.WaterPump.start(0)

        self.upAngle1 = 75
        self.upAngle2 = 110
        self.upAngle3 = 145

        self.forAngle1 = 45
        self.forAngle2 = 90
        self.forAngle3 = 135

        self.sprayOpen = False

    def bottom(self, angle):
        duty_cycle = float(angle) / 18 + 2.5
        self.MG90_forward.ChangeDutyCycle(duty_cycle)
        time.sleep(1)
        self.MG90_up.ChangeDutyCycle(0)

    def forward(self, angle):
        print("pump forward")
        duty_cycle = float(angle) / 18 + 2.5
        self.MG90_forward.ChangeDutyCycle(duty_cycle)
        time.sleep(1)
        self.MG90_up.ChangeDutyCycle(0)

    def up(self, angle):
        print("pump up")
        duty_cycle = float(angle) / 18 + 2.5
        self.MG90_up.ChangeDutyCycle(duty_cycle)
        time.sleep(1)
        self.MG90_up.ChangeDutyCycle(0)

    def sprayBegin(self):
        print("spray")
        self.WaterPump.ChangeDutyCycle(90)

    def sprayStop(self):
        print("spray Stop")
        self.WaterPump.ChangeDutyCycle(0)


class Crawler(CrawlerInfrared, CrawlerUltrasoundLeft, CrawlerUltrasoundRight):
    def __init__(self):
        CrawlerInfrared.__init__(self)
        CrawlerUltrasoundLeft.__init__(self)
        CrawlerUltrasoundRight.__init__()


class sendThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def send(self, msg):
        if len(msg) > 0:
            if isinstance(msg, str):
                msgServer = msg.encode("utf-8")
            elif isinstance(msg, list):
                msgServer = bytes(msg)
            client.send(msgServer)

    def run(self):
        while True:
            msgServer = input("\nprint obstacle:")
            if len(msgServer) > 0:
                client.send(msgServer.encode("utf-8"))


class recvThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            msg = client.recv(1024)
            msgPC = msg.decode("utf-8")
            if msgPC == "quit":
                print("quit\n")
                exit()
                break
            elif msgPC == "w":
                CrawlerMove.forward(100)
            elif msgPC == "a":
                CrawlerMove.turn_left_inSitu(100)
            elif msgPC == "d":
                CrawlerMove.turn_right_inSitu(100)
            elif msgPC == "s":
                CrawlerMove.turn_left_inSitu(100)
            elif msgPC == "z":
                CrawlerMove.stop()
            elif msgPC == "x":
                if waterPump.sprayOpen == False:
                    waterPump.sprayBegin()
                    waterPump.sprayOpen = True
                else:
                    waterPump.sprayStop()
                    waterPump.sprayOpen = False

            elif msgPC == "y":
                waterPump.forward(waterPump.forAngle1)
            elif msgPC == "u":
                waterPump.forward(waterPump.forAngle2)
            elif msgPC == "i":
                waterPump.forward(waterPump.forAngle3)

            elif msgPC == "h":
                waterPump.up(waterPump.upAngle1)
            elif msgPC == "j":
                waterPump.up(waterPump.upAngle2)
            elif msgPC == "k":
                waterPump.up(waterPump.upAngle3)

            else:
                print(msgPC)
        mySocket.close()


recv_thread = recvThread()
recv_thread.start()


def cameraOpen():
    os.system("sudo killall -TERM motion")
    time.sleep(1)
    os.system("sudo motion")
    print("camera open")


if __name__ == '__main__':
    try:
        GPIO.cleanup()
        CrawlerMove = CrawlerMove()
        waterPump = waterPump()
        crawler = Crawler()
        cameraOpen()
        while True:
            distLeft_mov_avr = crawler.DistLeftMeasureMovingAverage()
            distRight_mov_avr = crawler.DistRightMeasureMovingAverage()
            [l, r, b, f] = crawler.InfraredMeasure()
            sendThread().send([l, r, b, f, distLeft_mov_avr, distRight_mov_avr])

    except KeyboardInterrupt:
        print("Measurement stopped by User")
