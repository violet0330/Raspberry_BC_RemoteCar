import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class waterPump(object):
    def __init__(self):
        self.GPIO_Pump_bottom = 0
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

        self.upAngle1 = 30
        self.upAngle2 = 95
        self.upAngle3 = 120

        self.forAngle1 = 45
        self.forAngle2 = 90
        self.forAngle3 = 135

    def bottom(self, angle):
        while True:
            for i in range(0, 181, 10):
                if self.stopB:
                    self.stopB = False
                    break
                self.GPIO_Pump_bottom.ChangeDutyCycle(2.5 + 10 * i / 180)  # 设置转动角度
                time.sleep(0.02)  # 等该20ms周期结束
                self.GPIO_Pump_bottom.ChangeDutyCycle(0)  # 归零信号
                time.sleep(0.2)

    def forward(self):
        while True:
            for i in range(0, 181, 10):
                if self.stopB:
                    self.stopB = False
                    break
                self.GPIO_Pump_forward.ChangeDutyCycle(2.5 + 10 * i / 180)  # 设置转动角度
                time.sleep(0.02)  # 等该20ms周期结束
                self.GPIO_Pump_forward.ChangeDutyCycle(0)  # 归零信号
                time.sleep(0.2)

    def up(self):
        while True:
            for i in range(0, 181, 10):
                if self.stopB:
                    self.stopB = False
                    break
                self.GPIO_Pump_up.ChangeDutyCycle(2.5 + 10 * i / 180)  # 设置转动角度
                time.sleep(0.02)  # 等该20ms周期结束
                self.GPIO_Pump_up.ChangeDutyCycle(0)  # 归零信号
                time.sleep(0.2)

waterpump = waterPump()
waterpump.bottom(waterpump.forAngle1)
