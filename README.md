# Valon-5009-Python-GUI
The files in this directory deomstrate a simple Python/Tk GUI interface for the Valon 5009 synthesizer.

V5009CM.py contains the program's 'main' entry point.  
At a shell (or cmd) prompt, type 

	python V5009cm.py

Or load this file into Idle, and press F5 to start execution.


To run this program, you will need a fairly recent version of Python2.
Your version of Python will need to include PySerial, including its 'tools' directory.

If you see a message "ImportError: No module named serial" then you need to install PySerial.
Get a shell prompt and type

	pip install pyserial

On Linux machines, you will probably need to add "sudo" at the start of the command.
Make sure that is is python2.x that is getting updated.  If python3.x is the default on your machine, then try pip2 instead of pip.

If you see a message about a missing tools directory, get a shell prompt, and type:

	pip install --upgrade pyserial

If pip isn't installed (on a Linux machine), type

	<sudo> apt-get install python-pip

and then repeat the pip command above.

V5009cm was tested with python2.7,
on a PC running Windows 7,
and on a Raspberry Pi B+ running Raspbian.

To use Python3, at a minimum, you will need to modify the serial port module to convert back and forth between unicode and 8-bit characters.  I don't know what else.  Python3 also contains some incompatible changes in the Tkinter module.

You are free to use and modify these files, and share them.

There is very little error handling code here.  For use in a production environment, you will want to add some.

Peter McKone
