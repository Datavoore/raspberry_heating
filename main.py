import time

from config import relay_lower_pin_num, relay_raise_pin_num
from heating_controller import HeatingController, Valve
from sonde import sondes

heating_controller = HeatingController(sondes[2], None, Valve(relay_lower_pin_num, relay_raise_pin_num), 50)


def run_main_loop():
    while True:
        heating_controller.update()
        time.sleep(40)

