import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class CrawlerInfrared(object):
  def __init__(self):
    self.GPIO_Infrared_right = 8
    self.GPIO_Infrared_left = 7
    self.GPIO_Infrared_behind = 25
    self.GPIO_Infrared_front = 24

    GPIO.setup(self.GPIO_Infrared_right, GPIO.IN)
    GPIO.setup(self.GPIO_Infrared_left, GPIO.IN)
    GPIO.setup(self.GPIO_Infrared_behind, GPIO.IN)
    GPIO.setup(self.GPIO_Infrared_front, GPIO.IN)


  def InfraredMeasure(self):
    left_measure = GPIO.input(self.GPIO_Infrared_left)
    right_measure = GPIO.input(self.GPIO_Infrared_right)
    behind_measure = GPIO.input(self.GPIO_Infrared_behind)
    front_measure = GPIO.input(self.GPIO_Infrared_front)
    return [left_measure, right_measure, behind_measure, front_measure]


if __name__ == '__main__':
  try:
    crawler = CrawlerInfrared()
    while True:
      [l, r, b, f] = crawler.InfraredMeasure()
      msg = [l, r, b, f]
      print(msg)
      time.sleep(1)

  except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()

