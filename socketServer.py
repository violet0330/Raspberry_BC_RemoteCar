import RPi.GPIO as GPIO
import socket
import threading
import time
import math


#from infrared import CrawlerInfrared
#from ultrasonic import CrawlerUltrasound
#from motorControl import CrawlerMove

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
print("Raspberry start")

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = "172.25.13.54"
port = 3333
ip = (host, port)

hostPC = '172.25.8.147'
portPC = 3333
ipPC = (hostPC, portPC)

mySocket.bind(ip)
mySocket.listen(5)

client, address = mySocket.accept()
print("new connection")

class sendThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def send(self, msg):
        msgServer = msg.encode("utf-8")
        if len(msgServer) > 0:
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
            msgPC = client.recv(1024)
            if msgPC == b"quit":
                print("quit\n")
                exit()
                break
            elif msgPC == b"front" or b"w":
                #CrawlerMove.forward(80)
                print("go forward")
            elif msgPC == b"left" or b"a":
                #CrawlerMove.turn_left_inSitu(80)
                print("turn left")
            elif msgPC == b"right" or b"d":
                #CrawlerMove.turn_right_inSitu(80)
                print("turn right")
            elif msgPC == b"back" or b"s":
                #CrawlerMove.turn_left_inSitu(50)
                print("go backward")
            elif msgPC == b"stop" or b"\0":
                #CrawlerMove.stop()
                print("stop")
            else:
                print(msgPC.decode("utf-8"))
        mySocket.close()

#class Crawler(CrawlerInfrared, CrawlerUltrasound, CrawlerMove, sendThread):
class Crawler(sendThread):
    def __init__(self):
        #CrawlerInfrared.__init__(self)
        #CrawlerUltrasound.__init__(self)
        #CrawlerMove.__init__(self)
        sendThread.__init__(self)

recv_thread = recvThread()
recv_thread.start()



if __name__ == '__main__':
    try:
        crawler = Crawler()

    except KeyboardInterrupt:
        print("Measurement stopped by User")

