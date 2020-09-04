import logging

import serial.tools.list_ports as find_ports
from serial import Serial

import radar.connection.constants as constants


class RadarSerial(Serial):
    def __init__(self, port: str):
        super(RadarSerial, self).__init__(port=port, baudrate=constants.BAUDRATE, timeout=constants.TIMEOUT)

    def write(self, data):
        super(RadarSerial, self).write(data)
        super(RadarSerial, self).write('\n'.encode())

    def test(self) -> bool:
        self.flushInput()
        self.flushOutput()
        self.flush()

        text = ''

        tries = 0
        while (self.in_waiting > 0) | (tries < constants.TEST_TRIES):
            self.write(constants.IDN_CODE.encode())
            try:
                text = self.readline().decode().replace('\r\n', '')
            except UnicodeDecodeError as e:
                logging.debug(f"RadarSerial decode error {e}")

            logging.info(f"RadarSerial test received '{text}'")
            if constants.IDN_VALUE in text:
                self.flushInput()
                self.flushOutput()
                self.flush()

                return True
            tries += 1
        return False

    def read_angle_distance(self) -> tuple:
        angle, distance = -1, -1
        for i in range(5):
            self.write(constants.GET_ANGLE_DISTANCE_COMMAND.encode())
            try:
                angle, distance = self.readline().decode().replace('\r\n', '').split(constants.TUPLE_DELIMITER)
            except ValueError:
                pass
        return int(angle), int(distance)

    def update_range(self, r_min: int, r_max: int):
        self.write(f"{constants.SET_MIN_DISTANCE_COMMAND}{r_min}".encode())
        self.write(f"{constants.SET_MAX_DISTANCE_COMMAND}{r_max}".encode())

    def stop_start(self):
        self.write(constants.STOP_COMMAND.encode())

    def shoot(self):
        self.write(constants.SHOOT_COMMAND.encode())

    def stop_shooting(self):
        self.write(constants.STOP_SHOOTING_COMMAND.encode())


def find_devices() -> list:
    ports = []
    ports_objects = list(find_ports.comports())
    for port in ports_objects:
        serial = RadarSerial(port.device)
        if serial.test():
            ports.append(port.device)
        serial.close()
    return ports
