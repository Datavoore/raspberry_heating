import logging
import time

from GPIO import *
from sonde import Sonde
from simple_pid import PID


class Valve(object):
    def __init__(self, lower_pin, raise_pin):
        self.__lower_pin = lower_pin
        self.__raise_pin = raise_pin

    def lower_valve(self, time_interval):
        GPIO.output(self.__lower_pin, 1)
        time.sleep(time_interval)
        GPIO.output(self.__lower_pin, 0)

    def raise_valve(self, time_interval):
        GPIO.output(self.__raise_pin, 1)
        time.sleep(time_interval)
        GPIO.output(self.__raise_pin, 0)


class HeatingController:
    def __init__(
        self,
        output_sensor: Sonde,
        external_sensor: Sonde,
        valve: Valve,
        wanted_temperature: int = 40,
    ):
        self.__output_sensor = output_sensor
        self.__external_sensor = external_sensor
        self.__valve = valve
        self.__wanted_temperature = wanted_temperature
        self.__pid = PID(
            1,
            0.1,
            0.05,
            setpoint=self.__wanted_temperature,
            sample_time=None,
            output_limits=(-4, 4),
        )

    def update(self):
        out_temp = self.__output_sensor.get_temperature() / 1000
        control_value = self.__pid(out_temp)
        print(f"Control value: {control_value}")
        print(f"Output temperature: {out_temp}")
        if control_value > 0:
            print(f"Raising valve for {control_value} seconds")
            self.__valve.raise_valve(control_value)
        else:
            print(f"Lowering valve for {-control_value} seconds")
            self.__valve.lower_valve(-control_value)

    def set_wanted_temperature(self, wanted_temperature):
        self.__wanted_temperature = wanted_temperature
        self.__pid.setpoint = wanted_temperature

    def get_output_temperature(self):
        return self.__output_sensor.get_temperature()
