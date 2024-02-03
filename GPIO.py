import RPi.GPIO as GPIO
from config import relay_lower_pin_num, relay_raise_pin_num

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_lower_pin_num, GPIO.OUT)
GPIO.setup(relay_raise_pin_num, GPIO.OUT)