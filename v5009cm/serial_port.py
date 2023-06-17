import serial


class VSerialPort(serial.Serial):

    _BAUDRATES = (9600, 115200)
    _EOL = b"\r"
    _ENCODING = "ascii"

    def __init__(self, port):
        # Call the base constructor
        super().__init__(port, timeout=1.0)
        print(f"Using port {port}")

        self.portLines = []
        self.portLineCount = 0
        self.portLineIndex = 0

        for baudrate in self._BAUDRATES:
            # Try to open port with current settings
            self.baudrate = baudrate
            self.close()  # Close port, just in case (does nothing if port is not open)
            self.open()

            # Check if the device responds
            self.write(self._EOL)
            self.readAll()

            if self.portLines:
                print(f"Using baudrate {baudrate}")
                break  # Data was received

        else:
            raise RuntimeError("Cannot communicate with 5009")

    def writeline(self, line):
        print(line)
        self.write(bytearray(line, encoding=self._ENCODING) + self._EOL)

    def readAll(self):
        # Prepare the array to hold the incoming lines of text
        self.portLines.clear()
        self.portLineCount = self.portLineIndex = 0

        while line := self.readline().decode(encoding=self._ENCODING):
            print(line)
            self.portLines.append(line)
            self.portLineCount += 1

            # Stop reading when we get a prompt
            if len(line) == 5 and line[-1] == '>':
                break

    def lineGet(self):
        """Read from the array of previously-received lines of text."""
        i = self.portLineIndex
        self.portLineIndex += 1
        if self.portLineIndex > self.portLineCount:
            return ''
        return self.portLines[i]
