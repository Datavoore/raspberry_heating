import re

pattern = r"t=(\d+)"

def parse_temperature_as_int(sonde_file_content, regex = pattern):
    match = re.search(pattern, sonde_file_content)
    if match:
        extracted_number = int(match.group(1))
    return extracted_number

class Sonde(object):
    def __init__(self, file_path):
        self.__path = file_path
    
    def get_temperature(self):
        with open(self.__path) as sonde_temp_file :
            file_content = sonde_temp_file.read()
        return parse_temperature_as_int(file_content)