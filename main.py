import time

from config import relay_lower_pin_num, relay_raise_pin_num
from heating_controller import HeatingController, Valve
from sonde import sondes

heating_controller = HeatingController(
    output_sensor=sondes[2],
    external_sensor=sondes[1],
    valve=Valve(relay_lower_pin_num, relay_raise_pin_num),
    wanted_temperature=40,
)


def run_main_loop():
    while True:
        heating_controller.update()
        time.sleep(30 * 2)


if __name__ == "__main__":
    print("Sonde Temperature | Control Value | Active Time | Wanted Temperature")
    run_main_loop()
