import sys
import glob
import serial
import time
from serial.tools.list_ports import comports


COM_PORT = ""
BAUD_RATE = 19200


try:
    raw_input
except NameError:
    # pylint: disable=redefined-builtin,invalid-name
    raw_input = input   # in python3 it's "raw"
    unichr = chr

def ask_for_port():
    """\
    Show a list of ports and ask the user for a choice. To make selection
    easier on systems with long device names, also allow the input of an
    index.
    """
    sys.stderr.write('\n--- Available ports:\n')
    ports = []
    for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
        sys.stderr.write('--- {:2}: {:20} {!r}\n'.format(n, port, desc))
        ports.append(port)
    while True:
        sys.stderr.write('--- Enter port index or full name: ')
        port = raw_input('')
        try:
            index = int(port) - 1
            if not 0 <= index < len(ports):
                sys.stderr.write('--- Invalid index!\n')
                continue
        except ValueError:
            pass
        else:
            port = ports[index]
        return port

def reader(ser, str_length):
    """read multiple values from the serial port."""
    alive = True
    data = []

    for i in range(0, str_length):
        print(i)
        # read all that is there or wait for one byte
        data.append(ser.read(1))
        print(data)
    print("out of loop")
    return ''.join(data)

def writer(ser, STR_EXP):

    # send carriage return to get us to a known state in the DSP
    preamble = '\r'
    ser.write(preamble)
    ser.read()

    data = []

    for line in STR_EXP.splitlines():
        ser.write(line + '\r')
        ser.flush()

        # wait for a response to be transmitted
        time.sleep(1e-2)

        # read the response
        data.append( ser.read(ser.in_waiting) )

        # print the response
        print(data[-1])
    
    return data

    


TEST1 = b'v\r'

TEST2 = b"""
efgh
"""




if __name__ == '__main__':

    if not COM_PORT:
        ask_for_port()

    if COM_PORT:
        # configure the serial connections (the parameters differs on the device you are connecting to)
        ser = serial.Serial(
                port=COM_PORT,
                baudrate=BAUD_RATE,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                rtscts=False
            )

        if ser.is_open:
            print("Serial Terminal opened successfully.")
        else:
            print("Unable to open serial port")
            exit()

        ser.close()