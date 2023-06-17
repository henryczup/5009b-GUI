import sys
import serial
import serial.tools.list_ports


class VSerialPort(serial.Serial):

    def __init__(self):
        # Call the base constructor
        serial.Serial.__init__(self)

        self.portLines = []
        self.portLineCount = 0
        self.portLineIndex = 0

        portList = []
        for port, desc, hwid in serial.tools.list_ports.comports():
            print(('Port: ', port, ' Desc: ', desc, ' HwId: ', hwid))
            if (hwid.find("FTDI") != -1):       # on Windows PC
                portList.append(port)
            elif (desc.find("Future") != -1):   # on Raspberry Pi
                portList.append(port)
            elif "Valon" in desc:
                portList.append(port)

        if (len(portList) == 0):
            print("No FTDI com ports are available")
            return

        self.baudrate = 9600
        self.timeout = 1.0
        self.port = portList[0]
        self.open()

        self.write(b'\r')
        self.readAll()
        if (len(self.portLines) == 0):
            self.baudrate = 115200
            self.write(b'\r')
            self.readAll()
            if (len(self.portLines) == 0):
                print("Can't communicate with 5009")
                # exit()

        print(("Using " + self.port))

        # ----- End of Constructor -----

    def writeline(self, text):
        print(text)
        if (not self.isOpen()):
            return
        self.write(bytearray(text, encoding="ascii") + b'\r')

    def readAll(self):
        # Prepare the array to hold the incoming lines of text
        self.portLines = []
        self.portLineCount = self.portLineIndex = 0

        if (not self.isOpen()):
            return

        text = self.readline().decode()
        while (1):
            if (text == ""):
                return
            sys.stdout.write(text)

            self.portLines.append(text)
            self.portLineCount += 1

            # Stop reading when we get a prompt
            if (len(text) == 5):
                if text[4] == '>':
                    sys.stdout.flush()
                    return

            text = self.readline().decode()

    # Read from the array of previously-received lines of text
    def lineGet(self):
        i = self.portLineIndex
        self.portLineIndex += 1
        if (self.portLineIndex > self.portLineCount):
            return ''
        return self.portLines[i]
