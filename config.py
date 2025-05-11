relay_lower_pin_num = 17
relay_raise_pin_num = 27

w1_path = "/sys/bus/w1/devices/"

probes_paths = [
    w1_path + "28-66685e1f64ff/w1_slave",
    w1_path + "28-4a5f541f64ff/w1_slave",
]
favicon_path = "/home/pi/Pictures/favicon.ico"

data_path = "/home/pi/Documents/raspberry_heating/data/"

COMMAND_OVERRIDE_DIR = "/app/config_overrides"  # Directory for override files
COMMAND_OVERRIDE_FILENAME = "command_setting.json"
COMMAND_OVERRIDE_FILE_PATH = f"{COMMAND_OVERRIDE_DIR}/{COMMAND_OVERRIDE_FILENAME}"

# Default command value if no override is set or file is invalid
DEFAULT_HEATING_COMMAND = 50