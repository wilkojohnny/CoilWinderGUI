from Tkinter import *
import Winder
import time
import thread
import tkMessageBox
import math

# MainHandlers
# Handlers for all mainwindow graphics objects


class MainHandlers:
    noLayers = 0
    intLayers = 0
    spoolLength = 0
    WireDiameter = 0
    noTurns = 0
    TurnsPerLayer = 0
    Command = ""

    def __init__(self, PSerialMonitor, PSpoolBox, PDiameterBox, PTurnsBox):
        self.CurrentWinder = Winder.Winder()
        self.reading = True
        self.stopped_reading = False
        self.SerialMonitor = PSerialMonitor
        self.SpoolBox = PSpoolBox
        self.DiameterBox = PDiameterBox
        self.TurnsBox = PTurnsBox
        self.start_continuousread()
        self.Disconnected = False

    # Send serial data over
    def send_data(self, PSendTextBox=None, PCommand=None):
        # Stop the reading thread
        self.stop_continuousread()
        # Definitely stop any trace of reading
        self.CurrentWinder.stop_reading()
        # Send over to winder, and put the command on the serial monitor
        self.SerialMonitor.insert(END, "Command:: " + self.CurrentWinder.writeout(PCommand + "\n"))
        # If origin is textbox, clear
        if not (PSendTextBox==None):
            PSendTextBox.delete(0, len(PSendTextBox.get()))
        # Restart reading thread
        self.start_continuousread()

    # Start continuous reading thread
    def start_continuousread(self):
        self.reading = True
        thread.start_new_thread(self.continuousread, ())

    # Stop continuous reading thread
    def stop_continuousread(self):
        # Set reading flag to false
        self.reading = False
        # Wait for confirmed finish
        while not self.stopped_reading:
            pass

    # Serial output read - Runs on own thread
    def continuousread(self):
        self.stopped_reading = False
        try:
            # if reading mode on
            while self.reading:
                # if stuff in the read buffer, read it, otherwise wait
                while self.CurrentWinder.ConnectedWinder.in_waiting:
                    self.SerialMonitor.insert(END, self.CurrentWinder.read())
                else:
                    time.sleep(1)
            else:
                # Reading stopped requested
                self.stopped_reading = True
        # If error while reading, abort
        except Exception:
            self.SerialMonitor.insert(END, "Serial IO Error")
            self.CurrentWinder.disconnect()
            self.Disconnected = True

        # Confirm stopped reading for safe write
        self.stopped_reading = True

    # Auto-wind clicked
    def auto_wind(self):
        # Check inputs are numbers
        if not (self.isPositiveNumber(self.SpoolBox.get())
                and self.isPositiveNumber(self.DiameterBox.get())
                and self.isPositiveNumber(self.TurnsBox.get())):
            return

        # Convert values
        self.spoolLength = float(self.SpoolBox.get())
        self.WireDiameter = float(self.DiameterBox.get())
        self.noTurns = float(self.TurnsBox.get())

        # Check spool length is longer than wire diameter, and turns multiple of .25
        if (self.spoolLength < self.WireDiameter) or not (math.floor(4*self.noTurns) == 4*self.noTurns):
            return

        # Work out how many layers
        self.noLayers = self.get_no_layers()
        self.intLayers = math.ceil(self.noLayers)

        # How many turns per layer
        self.TurnsPerLayer = self.get_turns_per_layer()

        # Construct command
        self.Command = "wind -d " + str(self.WireDiameter) + " -t " + str(self.noTurns) + \
                       " -l " + str(self.noLayers) + " -tpl " + str(self.TurnsPerLayer)

        # Get confirmation
        confirmation = tkMessageBox.askquestion("Confirm", "Wire Diameter: " + str(self.WireDiameter) + "\nTurns:" + str(self.noTurns) + \
                                 "\n Layers:" + str(self.intLayers) + "\nTurns per layer:" + str(self.TurnsPerLayer)
                                 + "\n\n" + "Command: \n" + self.Command, icon="question")
        if confirmation == 'yes':
            self.send_data(PCommand=self.Command)
            print 'whirrr whirrr whirrr'

    def isPositiveNumber(self, string):
        try:
            float(string)
        except ValueError:
            return False
        if (abs(float(string)) == float(string)) and float(string)>0:
            return True
        else:
            return False

    def get_no_layers(self):
        # total wind length
        windLength = self.WireDiameter*self.noTurns
        return windLength/self.spoolLength

    def get_turns_per_layer(self):
        return self.noTurns/self.noLayers

    # On window close
    def __delete__(self):
        # Stop serial reading
        self.stop_continuousread()
        # Close serial ports
        self.CurrentWinder.disconnect()
