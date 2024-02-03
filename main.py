import time

from config import relay_lower_pin_num, relay_raise_pin_num
from heating_controller import HeatingController, Valve
from sonde import sondes

heating_controller = HeatingController(
    sondes[2],
    external_sensor=None,
    valve=Valve(relay_lower_pin_num, relay_raise_pin_num),
    wanted_temperature=40,
)


def run_main_loop():
    while True:
        heating_controller.update()
        time.sleep(60 * 2)


if __name__ == "__main__":
    print("Sonde Temperature | Control Value | Active Time")
    run_main_loop()
