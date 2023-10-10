import RPi.GPIO as GPIO
import time
import math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class CrawlerUltrasoundLeft(object):
    def __init__(self):
        self.GPIO_leftU_TRIGGER = 1
        self.GPIO_leftU_ECHO = 12

        GPIO.setup(self.GPIO_leftU_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_leftU_ECHO, GPIO.IN)

        self.dist_mov_ave = 0

    def DistLeftMeasure(self):
        GPIO.output(self.GPIO_leftU_TRIGGER, False)
        time.sleep(0.000002)
        GPIO.output(self.GPIO_leftU_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(self.GPIO_leftU_TRIGGER, False)


        i = 0
        while GPIO.input(self.GPIO_leftU_ECHO) == 0:
            i = i + 1
            if i > 10000:
                print('Ultrasound error: the sensor missed the echo')
                return 0
            pass
        start_time = time.time()

        while GPIO.input(self.GPIO_leftU_ECHO) == 1:
            pass
        stop_time = time.time()

        time_delta = stop_time - start_time
        distance = (time_delta * 34300) / 2

        return distance

    def DistLeftMeasureMovingAverage(self):
        dist_current = self.DistLeftMeasure()
        if dist_current == 0:
            return self.dist_mov_ave
        else:
            self.dist_mov_ave = 0.8 * dist_current + 0.2 * self.dist_mov_ave
            return self.dist_mov_ave


if __name__ == '__main__':
    try:
        car = CrawlerUltrasoundLeft()
        while True:
            dist_ave = car.DistLeftMeasureMovingAverage()