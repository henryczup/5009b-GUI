import serial


class VSerialPort(serial.Serial):

    def __init__(self, port):
        # Call the base constructor
        super().__init__(port, timeout=1.0)
        print(f"Using port {port}")

        self.portLines = []
        self.portLineCount = 0
        self.portLineIndex = 0

        for baudrate in [9600, 115200]:
            # Try to open port with current settings
            self.baudrate = baudrate
            self.close()  # Close port, just in case (does nothing if port is not open)
            self.open()

            # Check if the device responds
            self.write(b'\r')
            self.readAll()

            if self.portLines:
                print(f"Using baudrate {baudrate}")
                break  # Data was received

        else:
            raise RuntimeError("Cannot communicate with 5009")

    def writeline(self, text):
        print(text)
        self.write(bytearray(text, encoding="ascii") + b'\r')

    def readAll(self):
        # Prepare the array to hold the incoming lines of text
        self.portLines = []
        self.portLineCount = self.portLineIndex = 0

        text = self.readline().decode()
        while True:
            if not text:
                return
            print(text)

            self.portLines.append(text)
            self.portLineCount += 1

            # Stop reading when we get a prompt
            if len(text) == 5:
                if text[4] == '>':
                    return

            text = self.readline().decode()

    # Read from the array of previously-received lines of text
    def lineGet(self):
        i = self.portLineIndex
        self.portLineIndex += 1
        if self.portLineIndex > self.portLineCount:
            return ''
        return self.portLines[i]
