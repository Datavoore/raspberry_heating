import datetime
import time

from command_override_utils import get_command_override
from probe import Probe
from simple_pid import PID
from csv import writer
import RPi.GPIO as GPIO
from config import relay_lower_pin_num, relay_raise_pin_num, data_path
import logging

logger = logging.getLogger("heating_controller")

def heating_curve(external_temperature, coefficient, command):
    now = datetime.datetime.now()
    if now.hour < 7 or now.hour >= 22:
        return -coefficient * external_temperature + (command - 8)
    else:
        return -coefficient * external_temperature + command


class Valve(object):
    def __init__(self, lower_pin, raise_pin):
        self.__lower_pin = lower_pin
        self.__raise_pin = raise_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(relay_lower_pin_num, GPIO.OUT)
        GPIO.setup(relay_raise_pin_num, GPIO.OUT)
        GPIO.output(relay_lower_pin_num, 0)
        GPIO.output(relay_raise_pin_num, 0)

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
    csv_file_name = data_path + now.strftime("%Y-%m-%d") + ".csv"
    with open(csv_file_name, "a") as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(row)
        f_object.close()


class HeatingController:
    def __init__(
        self,
        output_sensor: Probe,
        external_sensor: Probe,
        valve: Valve,
        tolerance: int = 0.7,
        coefficient: int = 1.4,
        command: int = 50,
    ):
        self.__output_sensor = output_sensor
        self.__external_sensor = external_sensor
        self.__valve = valve
        self.__tolerance = tolerance
        self.__coefficient = coefficient
        self.__command = command
        wanted_temperature = heating_curve(
            external_sensor.get_temperature() / 1000, coefficient, command
        )
        self.__pid = PID(
            1,
            0.5,
            0.05,
            setpoint=wanted_temperature,
            sample_time=None,
            output_limits=(-4, 4),
            # proportional_on_measurement=True,
        )

    def update(self):
        output_temp = self.__output_sensor.get_temperature() / 1000
        pid_control = self.__pid(output_temp)
        outside_temperature = self.__external_sensor.get_temperature() / 1000
        command = get_command_override()
        wanted_temperature = heating_curve(
            outside_temperature, self.__coefficient, command
        )
        self.__command = command
        self.__pid.setpoint = wanted_temperature
        # This means we are close to the wanted temperature, no need to use PID control
        if abs(output_temp - wanted_temperature) <= self.__tolerance:
            control_value = 0
        else:
            control_value = pid_control

        if control_value > 0:
            self.__valve.raise_valve(control_value)
        elif control_value < 0:
            self.__valve.lower_valve(-control_value)

        self.log_and_save_data(output_temp, outside_temperature, control_value)

    def log_and_save_data(self, output_temp, external_temp, control):
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        command = self.__command
        wanted_temperature = heating_curve(
            external_temp, self.__coefficient, command
        )
        logger.info(
            f"| {now_str} | {output_temp} | {external_temp} | {wanted_temperature} | {control} | {command} |"
        )
        csv_row = [now_str, output_temp, external_temp, wanted_temperature, control, command]
        write_row_to_csv(csv_row)
