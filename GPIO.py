import RPi.GPIO as GPIO
from config import relay_1_pin_num, relay_2_pin_num

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_1_pin_num, GPIO.OUT)
GPIO.setup(relay_2_pin_num, GPIO.OUT)