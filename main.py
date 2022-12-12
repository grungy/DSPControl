import sys
import glob
import serial
import time
from serial.tools.list_ports import comports


COM_PORT = "/dev/cu.usbserial-1420"
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

def reader(ser):
        """loop and copy serial->console"""
        alive = True

        try:
            while alive:
                # read all that is there or wait for one byte
                data = ser.read(ser.in_waiting or 1)
                if data:
                    print(data)
        except serial.SerialException:
            alive = False
            raise       # XXX handle instead of re-raise?

def writer(self):
        """\
        Loop and copy console->serial until self.exit_character character is
        found. When self.menu_character is found, interpret the next key
        locally.
        """
        menu_active = False
        try:
            while self.alive:
                try:
                    c = self.console.getkey()
                except KeyboardInterrupt:
                    c = '\x03'
                if not self.alive:
                    break
                if menu_active:
                    self.handle_menu_key(c)
                    menu_active = False
                elif c == self.menu_character:
                    menu_active = True      # next char will be for menu
                elif c == self.exit_character:
                    self.stop()             # exit app
                    break
                else:
                    #~ if self.raw:
                    text = c
                    for transformation in self.tx_transformations:
                        text = transformation.tx(text)
                    self.serial.write(self.tx_encoder.encode(text))
                    if self.echo:
                        echo_text = c
                        for transformation in self.tx_transformations:
                            echo_text = transformation.echo(echo_text)
                        self.console.write(echo_text)
        except:
            self.alive = False
            raise




if __name__ == '__main__':
    # COM_PORT = ask_for_port()

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

        print(ser.is_open)
        
        ser.write(b"B")


        ser.flush()

        data = ser.read(1)

        if data:
            print(data)
        ser.close()