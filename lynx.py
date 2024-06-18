import sys
from getopt import getopt, GetoptError
from pathlib import Path

import serial
import serial.tools.list_ports
from serial.tools.list_ports_common import ListPortInfo

from services.rs232 import Rs232Service


def list_com_ports() -> list[ListPortInfo]:
    return serial.tools.list_ports.comports()


def print_help():
    pass


if __name__ == '__main__':
    short_opts = 'h'

    long_opts = [
        "com=",
        "send",
        "help",
    ]

    try:
        options, args = getopt(sys.argv[1:], short_opts, long_opts)
    except GetoptError as err:
        print(f"Error parsing options: {err}")
        sys.exit(2)

    send_flag = False
    com_port = None

    for opt, arg in options:
        if opt in ("-h", "--help"):
            print_help()
        elif opt == "--com":
            com_port = arg
        elif opt == "--send":
            send_flag = True
        else:
            print(f"Unknown option: {opt}")
            print_help()

    ports = list_com_ports()

    for port in ports:
        print(
            f'[{port.name}][{port.hwid}][{port.description}][{port.device}][{port.vid}][{port.manufacturer}][{port.serial_number}]')
        if com_port is None and port.description.startswith('USB Serial Port'):
            com_port = port.device

    if com_port is None:
        print("No USB Serial Port found")
        sys.exit(2)

    print(f'Serial port: {com_port}')

    current_dir = Path.cwd()
    print(f'Current directory: {current_dir}')

    if send_flag:
        sending_directory = current_dir / 'send'
        print(f'Sending directory: {sending_directory}')
        if sending_directory.is_dir():
            # sending_directory.mkdir(exist_ok=True)
            files = [item for item in sending_directory.iterdir() if item.is_file()]
            print(f'Found {len(files)} files')
            print(files)
        else:
            print(f'{sending_directory}: Sending directory does not exist')

    else:
        received_directory = current_dir / 'receive'
        print(f'Received directory: {received_directory}')
        if not received_directory.is_dir():
            received_directory.mkdir()
            print(f'Created directory: {received_directory}')
        rs232 = Rs232Service(com_port)
        rs232.recv_file(received_directory.name)
