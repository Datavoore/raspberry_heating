# Raspberry connected heating system

This is a simple project to control a heating system using a Raspberry Pi. The system is controlled using a web interface and a temperature sensor.

Heating system is a wood stove with a water tank and a pump. The pump is controlled by a relay connected to the Raspberry Pi.

## Hardware

- Raspberry Pi 3
- DS18B20 temperature sensor
- 220V Relay module
- Water pump
- Wood stove with water tank
- 5V power supply

## Server command
uvicorn main:app --reload --log-config=log_conf.yaml --host 0.0.0.0 --port 8042