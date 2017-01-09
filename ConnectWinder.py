from Tkinter import *
import serial.tools.list_ports

class ConnectWinderBox():
    def __init__(self):
        self.location = ""
        self.Window = Tk()
        self.PopulateWindow()

    def PopulateWindow(self):
        self.SelectButton = Button(self.Window, text="Connect")
        self.Window.title("Connect to Serial IO")

        arduino_ports = [
           p.device
           for p in serial.tools.list_ports.comports()
            ]

        variable = StringVar(self.Window)
        variable.set(arduino_ports[0])

        self.SerialSelector = apply(OptionMenu, (self.Window, variable) + tuple(arduino_ports))
        self.SerialSelector.pack(side=LEFT)
        self.SelectButton.pack(side=LEFT)

    def ShowWindow(self):
        self.Window.mainloop()

    def CloseWindow(self):
        self.location = self.SerialSelector.get()
        self.Window.quit()

