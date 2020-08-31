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
        self.flushInput()
        self.flush()

        for i in range(2):
            try:
                angle, distance = self.readline().decode().replace('\r\n', '').split(constants.TUPLE_DELIMITER)
                return int(angle), int(distance)
            except ValueError as e:
                pass
        raise e


def find_devices() -> list:
    ports = []
    ports_objects = list(find_ports.comports())
    for port in ports_objects:
        serial = RadarSerial(port.device)
        if serial.test():
            ports.append(port.device)
        serial.close()
    return ports
