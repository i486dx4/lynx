import serial

from modem import YModem


class Rs232Global:
    ser: serial.Serial | None = None


def _receive_char(sz: int, timeout: int = 1, debug: bool = False) -> bytes:
    if debug:
        print(f'receiving {sz} bytes')
    return Rs232Global.ser.read(sz)


def _send_char(char: bytes, timeout: int = 1, debug: bool = False):
    if debug:
        print(f'sending {len(char)} bytes')
    return Rs232Global.ser.write(char)


class Rs232Service:
    modem: YModem

    def __init__(self, com_port: str, baud_rate: int = 9600):
        Rs232Global.ser = serial.Serial(com_port, baudrate=baud_rate, parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

        # Close the serial port when finished
        self.modem = YModem(_receive_char, _send_char)

    def __del__(self):
        Rs232Global.ser.close()

    def send_file(self, filename: str):
        self.modem.send(filename)

    def recv_file(self, folder: str):
        self.modem.recv(folder)
