import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


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

        self.motor_left.start(0)  # motors start
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
        self.motor_left.stop()
        self.motor_right.stop()

    def forward(self, speed):
        self.rotate_left()
        self.rotate_right()
        self.motor_left.ChangeDutyCycle(speed)
        self.motor_right.ChangeDutyCycle(speed)

    def backward(self, speed):
        self.reverse_left()
        self.reverse_right()
        self.motor_left.ChangeDutyCycle(speed)
        self.motor_right.ChangeDutyCycle(speed)

    def turn_left_inSitu(self, speed):
        self.reverse_left()
        self.rotate_right()
        self.motor_left.ChangeDutyCycle(speed)
        self.motor_right.ChangeDutyCycle(speed)

    def turn_right_inSitu(self, speed):
        self.rotate_left()
        self.reverse_right()
        self.motor_left.ChangeDutyCycle(speed)
        self.motor_right.ChangeDutyCycle(speed)

    def turn_dif_for(self, speedL, delta):
        self.rotate_left()
        self.rotate_right()
        self.motor_left.ChangeDutyCycle(speedL)
        self.motor_right.ChangeDutyCycle(speedL+delta)

    def turn_dif_back(self, speedL, delta):
        self.reverse_left()
        self.reverse_right()
        self.motor_left.ChangeDutyCycle(speedL)
        self.motor_right.ChangeDutyCycle(speedL+delta)

if __name__ == '__main__':
    try:
        crawler = CrawlerMove()
        while True:
            crawler.turn_dif_for(40, 20)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()