import logging
import re

from config import probes_paths

logger = logging.getLogger("probe")

pattern = r"t=(\d+|-\d+|)"


def parse_temperature_as_int(probe_file_content):
    match = re.search(pattern, probe_file_content)
    if match:
        extracted_number = int(match.group(1))
        return extracted_number
    else:
        raise ValueError("Temperature not found in file")


class Probe(object):
    def __init__(self, file_path):
        self.__path = file_path
        # We test if the file exists
        with open(self.__path) as probe_temp_file:
            probe_temp_file.read()

    def get_temperature(self):
        with open(self.__path) as probe_temp_file:
            file_content = probe_temp_file.read()
        return parse_temperature_as_int(file_content)


probes = {}
for i in range(len(probes_paths)):
    try:
        probes[i + 1] = Probe(probes_paths[i])
    except FileNotFoundError:
        logger.info(f"Probe {i + 1} not found (path: {probes_paths[i]})")
