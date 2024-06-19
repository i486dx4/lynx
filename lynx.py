import os
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
    print(f'''
usage: {sys.argv[0]} [options]

  --send                   default is receiving
  --com <COM port>
  --baud <Baud>            default 115200
  --folder <folder>        default <send> for sending, <received> for receiving
  
Note: use Y-Modem protocol send file via serial line, always start sending before receiving.
    ''')
    sys.exit()


if __name__ == '__main__':
    short_opts = 'h'

    long_opts = [
        "com=",
        "baud=",
        "folder=",
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
    baud_rate = 115200
    folder = None

    for opt, arg in options:
        if opt in ("-h", "--help"):
            print_help()
        elif opt == "--com":
            com_port = arg
        elif opt == "--send":
            send_flag = True
        elif opt == "--baud":
            baud_rate = int(arg)
        elif opt == '--folder':
            folder = arg
        else:
            print(f"Unknown option: {opt}")
            print_help()

    ports = list_com_ports()

    for port in ports:
        print(
            f'{port.name}: [{port.hwid}] {port.description}, VID: {port.vid}, {port.manufacturer}')
        if com_port is None and port.description.startswith('USB Serial Port'):
            com_port = port.device

    if com_port is None:
        print("No USB Serial Port found")
        sys.exit(2)

    print(f'Serial port: {com_port}, baud rate: {baud_rate}')

    current_dir = Path.cwd()
    print(f'Current directory: {current_dir}')

    sending_directory = current_dir / 'send'
    received_directory = current_dir / 'received'

    if folder is not None:
        sending_directory = folder
        received_directory = folder

    if send_flag:
        print(f'Sending directory: {sending_directory}')
        if sending_directory.is_dir():
            os.chdir(sending_directory)
            rs232 = Rs232Service(com_port, baud_rate=baud_rate)
            rs232.send_file('*.*')
            os.chdir(current_dir)
        else:
            print(f'{sending_directory}: Sending directory does not exist')
    else:
        print(f'Receiving directory: {received_directory}')
        if not received_directory.is_dir():
            received_directory.mkdir()
            print(f'Created directory: {received_directory}')
        rs232 = Rs232Service(com_port, baud_rate=baud_rate)
        rs232.recv_file(received_directory.name)
