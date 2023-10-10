import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class CrawlerUltrasoundRight(object):
    def __init__(self):
        self.GPIO_rightU_TRIGGER = 1
        self.GPIO_rightU_ECHO = 12

        GPIO.setup(self.GPIO_rightU_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_rightU_ECHO, GPIO.IN)

        self.dist_mov_ave = 0



    def DistRightMeasure(self):
        GPIO.output(self.GPIO_rightU_TRIGGER, False)
        time.sleep(0.000002)
        GPIO.output(self.GPIO_rightU_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(self.GPIO_rightU_TRIGGER, False)

        i = 0
        while GPIO.input(self.GPIO_rightU_ECHO) == 0:
            i = i + 1
            if i > 10000:
                print('Ultrasound error: the sensor missed the echo')
                return 0
            pass
        start_time = time.time()

        while GPIO.input(self.GPIO_rightU_ECHO) == 1:
            # the duration of high level of ECHO is the time between the emitting the pulse and receiving the echo
            pass
        stop_time = time.time()

        time_delta = stop_time - start_time
        distance = (time_delta * 34300) / 2

        return distance

    def DistRightMeasureMovingAverage(self):
        dist_current = self.DistRightMeasure()
        if dist_current == 0:  # if the sensor missed the echo, the output dis_mov_ave will equal the last dis_mov_ave
            return self.dist_mov_ave
        else:
            self.dist_mov_ave = 0.8 * dist_current + 0.2 * self.dist_mov_ave
            return self.dist_mov_ave


if __name__ == '__main__':
    try:
        car = CrawlerUltrasoundRight()
        while True:
            dist = car.DistRightMeasureMovingAverage()
            print("Measured Distance = {:.2f} cm".format(dist))
            time.sleep(1)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()