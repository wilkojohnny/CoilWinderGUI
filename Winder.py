import serial
import time
from Tkinter import *
import os
import thread
import serial.tools.list_ports

# WINDER CLASS
# Deals with all winder-to-PC communication

class Winder:

    def __init__(self):
        # Create and launch the window to ask for serial port
        self.location = ""
        self.Window = Tk()
        self.SelectButton = Button(self.Window, text="Connect", command=self.WinderWindowOK)
        self.Window.title("Connect to Serial IO")
        self.Window.attributes("-topmost", True)
        self.Window.lift()
        # List of all possible arduino ports
        arduino_ports = [
           p.device
           for p in serial.tools.list_ports.comports()
            ]
        self.arduino_ports_strings = StringVar(self.Window)
        self.arduino_ports_strings.set(arduino_ports[0])
        # Create selector widget
        self.SerialSelector = apply(OptionMenu, (self.Window, self.arduino_ports_strings) + tuple(arduino_ports))
        # Draw Window
        self.SerialSelector.pack(side=LEFT)
        self.SelectButton.pack(side=LEFT)
        # If you close the prompt box, it acts as if OK was clicked
        self.Window.protocol("WM_DELETE_WINDOW", self.WinderWindowOK)
        self.Window.mainloop()

    # Launches when serial port selected in GUI
    def WinderWindowOK(self):
        # Get selected serial port
        self.location = self.arduino_ports_strings.get()
        # Exit window
        self.Window.quit()
        self.Window.destroy()
        # Connect to winder
        self.connect()

    # Connects to serial winder
    def connect(self):
        self.ConnectedWinder = serial.Serial(self.location, 9600, timeout=.1, xonxoff=True)
        time.sleep(2)

    # Write out string to serial
    def writeout(self, sendstring):
        try:
            self.ConnectedWinder.write(sendstring)
            self.ConnectedWinder.flush()
            return sendstring
        except serial.SerialException:
            return sendstring + "Serial IO Error \n"

    # Read in one line from serial
    def read(self):
        try:
            data = self.ConnectedWinder.readline()
            return data
        except serial.SerialException:
            return "Serial IO Error \n"

    # Abort current read
    def stop_reading(self):
        self.ConnectedWinder.cancel_read()

    # Disconnect winder
    def disconnect(self):
        if os.path.exists(self.location):
            self.ConnectedWinder.close()
