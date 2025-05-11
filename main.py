import time

from config import relay_lower_pin_num, relay_raise_pin_num, relay_pump
from heating_controller import HeatingController, Valve, Pump
from probe import probes, Probe
from command_override_utils import get_current_state

state = get_current_state()
command_override, is_on = state['command_override'], state['controller_on']
heating_controller = HeatingController(
    output_sensor=probes[2],
    external_sensor=probes[1],
    valve=Valve(relay_lower_pin_num, relay_raise_pin_num),
    pump=Pump(relay_pump,is_on),
    command=command_override
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
