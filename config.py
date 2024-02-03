import time

relay_1_pin_num = 17
relay_2_pin_num = 27

w1_path = "/sys/bus/w1/devices/"

sondes_paths = [w1_path + "28-66685e1f64ff/w1_slave", w1_path + "28-4a5f541f64ff/w1_slave"]
