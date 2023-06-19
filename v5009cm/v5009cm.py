# Version
# 0.03  Uses a custom command function for each spinbox
#       The arrows work.  Typing in a value doesn't work
#   04  Uses a single partial command function for each spinbox
#       Uses spinbox.Value as the textvariable
#       Derives data from event.widget in the <Return Key> handler
#       Passes the widget as arg[ 0 ] to the spinbox arrow EH
#   05  Put Freq spinbox into the new CwPanel class in a separate file
#       Added Column Labels and some color
#   06  Added the SerialPort class.
#       Added port enumeration and search for FTDI port
#   07  Added DALL query and parsing to the Main Panel
#   08  DALL query and parsing are moved from Main Panel to Main Window
#       Added Mode OptionMenus
#       Tested and modified to run on RPi
#   09  Operation without a synthesizer is supported
#       Menu with File/exit and Help/About is added.
#       PDN buttons are added.
#   10  PDN is changed from Button to Checkbutton
#       Mode selector was changed from Optionmenu to Combobox.
#           Change not retained.
#       Implemented baudrate detection (9600 or 115200 only)
#       Added Reference Source and Reference Frequency.
#   11  Reinforced use of class data.  Previously some items were being
#       reinstantiated as instance data.
# 1.00  Converted to Python 3 and packaged into `v5009cm` with entry point `v5009cm`.

import argparse

import tkinter as tk

import v5009cm.serial_port as VSerialPort
import v5009cm.menu as Menu
import v5009cm.cw_panel as CwPanel


class MainWindow(tk.Tk):
    # Class data
    sp = None
    menuBar = None
    cwPanel = None

    def __init__(self, port):
        # Call the base constructor
        super().__init__()

        self.title('V5009CM')
        self.bg = 'ivory'

        # Instance data
        self.sourceIndex = 99999     # set in parseQueryLines() to 0 or 1
        self.suppressCommands = False

        MainWindow.sp = VSerialPort.VSerialPort(port)
        if MainWindow.sp.isOpen():
            MainWindow.sp.writeLine("status")
            MainWindow.sp.readAll()

        MainWindow.menuBar = Menu.VMenu(self)
        self['menu'] = MainWindow.menuBar

        MainWindow.cwPanel = CwPanel.CwPanel(self)
        MainWindow.cwPanel.pack()

        # Pass some of our state to our child
        CwPanel.CwPanel.setSendCommand(self.sendCommand)

        self.dallQuery()
        # Enable resizing of column zero of the main window
        # self.grid_columnconfigure(0,weight=1)

        # Allow horizontal resizing, but not vertical
        self.resizable(True, False)
        # Prevent resizing when the user types a long text string.
        self.update()
        self.geometry(self.geometry())

        MainWindow.cwPanel.freqBox[0].focus_set()

    def sendCommand(self, widget):
        if (self.suppressCommands):
            return
        source = widget.Source
        command = widget.name
        value = widget.Value.get()
        if (source == -1):
            cmd = '{0} {1}'.format(command, value)
        else:
            cmd = 'source {0}; {1} {2}'.format(source, command, value)
        MainWindow.sp.writeLine(cmd)

        MainWindow.sp.readAll()
        MainWindow.sp.lineGet()       # Throw away the echo of the command
        line = MainWindow.sp.lineGet()
        if (line != ''):
            self.parseQueryLine(source - 1, line)

    def dallQuery(self):

        # This procedure will change values in the widgets.
        # Don't let them send these "new" values back to the synthesizer
        saveSuppressCommands = self.suppressCommands
        self.suppressCommands = True

        # Poison the following index.
        # It will be set to a valid value in parseQuieryLine()
        self.sourceIndex = 99997

        # Fetch the synthesizer's register values
        MainWindow.sp.writeLine("DALL")
        MainWindow.sp.readAll()

        # Parse the register values and store them into our widgets
        queryLine = MainWindow.sp.lineGet()
        while (queryLine != ''):
            self.parseQueryLine(self.sourceIndex, queryLine)
            queryLine = MainWindow.sp.lineGet()

        self.suppressCommands = saveSuppressCommands

    def parseQueryLine(self, sourceIndexParam, queryLine):
        queryLine = queryLine.replace(';', '')
        seg = queryLine.split()

        seg0 = seg[0].upper()

        if (seg0 == 'DALL'):
            pass
        elif (seg0 == 'S1'):
            self.sourceIndex = 0
        elif (seg0 == 'S2'):
            self.sourceIndex = 1
        elif (seg0 == 'F'):
            #  F 2440 MHz; // Act 2440 MHz
            sb = MainWindow.cwPanel.freqBox[sourceIndexParam]
            sb.Value.set(seg[1])
            label = MainWindow.cwPanel.freqActual[sourceIndexParam]
            label.Text.set(seg[5] + ' ' + seg[6])
        elif (seg0 == 'ATT'):
            #  ATT 15.0; // dB
            widget = MainWindow.cwPanel.attBox[sourceIndexParam]
            widget.Value.set(seg[1])
            widget = MainWindow.cwPanel.attActual[sourceIndexParam]
            if (len(seg) == 4):
                widget.Text.set(seg[3])
            elif (len(seg) == 5):
                widget.Text.set(seg[3] + ' ' + seg[4])
            else:
                pass
        elif (seg0 == 'MODE'):
            #  MODE CW;
            widget = MainWindow.cwPanel.modeBox[sourceIndexParam]
            widget.Value.set(seg[1])
            widget = MainWindow.cwPanel.modeActual[sourceIndexParam]
            widget.Text.set(seg[1])
        elif (seg0 == 'PDN'):
            #  PDN 1;
            widget = MainWindow.cwPanel.pdnBox[sourceIndexParam]
            widget.Value.set(seg[1])
            widget = MainWindow.cwPanel.pdnActual[sourceIndexParam]
            widget.Text.set(seg0 + ' ' + seg[1])
        elif (seg0 == 'REFS'):
            # REFS 0;
            widget = MainWindow.cwPanel.refSourceBox
            index = int(seg[1])
            if ((index != 0) and (index != 1)):
                return   # Invalid value
            widget.Value.set(index)
            widget.Text.set(widget.TextValues[index])

            widget = MainWindow.cwPanel.refSourceActual
            widget.Text.set(seg0 + ' ' + seg[1])
        elif (seg0 == "REF"):
            # REF 20 MHz;
            widget = MainWindow.cwPanel.refFreqBox
            widget.Value.set(seg[1])
            widget = MainWindow.cwPanel.refFreqActual
            widget.Text.set(seg[1] + ' ' + seg[2])
        else:
            pass


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=str, help="serial port of the device")
    args = parser.parse_args()

    # instantiate our mainProgram class
    app = MainWindow(args.port)

    # Wait for events
    app.mainloop()

    # Exit
    print()


if __name__ == "__main__":
    main()
