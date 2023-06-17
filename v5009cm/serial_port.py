import collections

import serial


class VSerialPort(serial.Serial):

    _BAUDRATES = (9600, 115200)
    _EOL = b"\r"
    _ENCODING = "ascii"

    def __init__(self, port):
        # Call the base constructor
        super().__init__(port, timeout=1.0)
        print(f"Using port {port}")

        self._line_buffer = collections.deque()

        for baudrate in self._BAUDRATES:
            # Try to open port with current settings
            self.baudrate = baudrate
            self.close()  # Close port, just in case (does nothing if port is not open)
            self.open()

            # Check if the device responds
            self.write(self._EOL)
            self.readAll()

            if self._line_buffer:
                # Data was received
                print(f"Using baudrate {baudrate}")
                break

        else:
            raise RuntimeError("Cannot communicate with 5009")

    def writeline(self, line):
        print(line)
        self.write(bytearray(line, encoding=self._ENCODING) + self._EOL)

    def readAll(self):
        self._line_buffer.clear()

        while line := self.readline().decode(encoding=self._ENCODING):
            print(line)
            self._line_buffer.append(line)

            if len(line) == 5 and line[-1] == '>':
                # Stop reading when we get a prompt
                break

    def lineGet(self):
        """Read from the array of previously-received lines of text."""
        return self._line_buffer.popleft() if self._line_buffer else ''
