import time

from config import relay_lower_pin_num, relay_raise_pin_num
from heating_controller import HeatingController, Valve
from probe import probes

heating_controller = HeatingController(
    output_sensor=probes[2],
    external_sensor=probes[1],
    valve=Valve(relay_lower_pin_num, relay_raise_pin_num),
)


def run_main_loop():
    while True:
        heating_controller.update()
        time.sleep(30)


if __name__ == "__main__":
    print(
        "Date/time | Output Temperature | External Temperature | Wanted Temperature | Control Value (time to open valve)"
    )
    run_main_loop()
