import datetime
import logging
import time

from GPIO import *
from sonde import Sonde
from simple_pid import PID
from csv import writer


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


def write_row_to_csv(row):
    now = datetime.datetime.now()
    csv_file_name = "data/" + now.strftime("%Y-%m-%d") + ".csv"
    with open(csv_file_name, "a") as f_object:
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object)
        writer_object.writerow(row)

        # Close the file object
        f_object.close()


class HeatingController:
    def __init__(
            self,
            output_sensor: Sonde,
            external_sensor: Sonde,
            valve: Valve,
            wanted_temperature: int = 40,
            tolerance: int = 0.7,
    ):
        self.__output_sensor = output_sensor
        self.__external_sensor = external_sensor
        self.__valve = valve
        self.__wanted_temperature = wanted_temperature
        self.__tolerance = tolerance
        self.__pid = PID(
            1,
            0.5,
            0.05,
            setpoint=self.__wanted_temperature,
            sample_time=None,
            output_limits=(-4, 4),
            # proportional_on_measurement=True,
        )

    @property
    def wanted_temperature(self):
        return self.__wanted_temperature

    @wanted_temperature.setter
    def wanted_temperature(self, wanted_temperature):
        self.__wanted_temperature = wanted_temperature
        self.__pid.setpoint = wanted_temperature

    def update(self):
        out_temp = self.__output_sensor.get_temperature() / 1000
        pid_control = self.__pid(out_temp)
        # This means we are close to the wanted temperature, no need to use PID control
        if abs(out_temp - self.__wanted_temperature) <= self.__tolerance:
            control_value = 0
        else:
            control_value = pid_control
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{now_str} | {out_temp} | {control_value} |")
        csv_row = [now_str, out_temp, control_value]
        write_row_to_csv(csv_row)
        if control_value > 0:
            self.__valve.raise_valve(control_value)
        elif control_value < 0:
            self.__valve.lower_valve(-control_value)
