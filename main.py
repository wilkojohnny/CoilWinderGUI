from mainHandlers import *


def shutdown():
    handlers.__delete__()
    MainWindow.destroy()


def send_button_handler(event=1):
    handlers.send_data(PSendTextBox=SendTextBox, PCommand=SendTextBox.get())


def start_auto_handler():
    handlers.auto_wind()


def start_layer_handler():
    pass

# Declare Objects
MainWindow = Tk()

# Window Frames
SerialEntryFrame = Frame(MainWindow)
SerialMonitorFrame = Frame(MainWindow)
ParametersFrame = Frame(MainWindow)
StatusFrame = Frame(MainWindow)

# --- Declare Window Items ---

# Parameter Selection
SpoolLabel = Label(ParametersFrame, text="Spool Length (mm): ")
SpoolLabel.grid(row=0, column=0)
SpoolBox = Entry(ParametersFrame, width=10)
SpoolBox.grid(row=0, column=1)
DiameterLabel = Label(ParametersFrame, text="Wire Diameter (mm): ")
DiameterLabel.grid(row=1, column=0)
DiameterBox = Entry(ParametersFrame, width=10)
DiameterBox.grid(row=1, column=1)
TurnsLabel = Label(ParametersFrame, text="Turns: ")
TurnsLabel.grid(row=2, column=0)
TurnsBox = Entry(ParametersFrame, width=10)
TurnsBox.grid(row=2, column=1)

StartAutoButton = Button(ParametersFrame, text="Start (Auto)", command=start_auto_handler)
StartAutoButton.grid(row=3, column=0)
StartLayerButton = Button(ParametersFrame, text="Start Layer", command=start_layer_handler)
StartLayerButton.grid(row=3, column=1)

# Status
FeedPositionLabel = Label(StatusFrame, text="Feeder Position:", font=("Arial", 20))
FeedPositionLabel.grid(row=0)
TurnsCompletedLabel = Label(StatusFrame, text="Turns Completed:", font=("Arial", 20))
TurnsCompletedLabel.grid(row=1)
LayersCompletedLabel = Label(StatusFrame, text="Layers Completed:", font=("Arial", 20))
LayersCompletedLabel.grid(row=2)
CurrentFeedPositionLabel = Label(StatusFrame, text="0", fg="red", font=("Courier", 20))
CurrentFeedPositionLabel.grid(row=0, column=1)
CurrentTurnsCompletedLabel = Label(StatusFrame, text="0", fg="red", font=("Courier", 20))
CurrentTurnsCompletedLabel.grid(row=1, column=1)
CurrentLayersCompletedLabel = Label(StatusFrame, text="0", fg="red", font=("Courier", 20))
CurrentLayersCompletedLabel.grid(row=2, column=1)

# Command line
CommandLabel = Label(SerialEntryFrame, text="Command to be sent: ")
SendTextBox = Entry(SerialEntryFrame, width=30)
SerialMonitor = Text(SerialMonitorFrame, width=100, height=5)
SerialMonitorScroll = Scrollbar(SerialMonitorFrame)
SendButton = Button(SerialEntryFrame, text="Send", command=send_button_handler)


# Link Handlers class to GUI
handlers = MainHandlers(PSerialMonitor=SerialMonitor,
                        PSpoolBox=SpoolBox,
                        PDiameterBox=DiameterBox,
                        PTurnsBox=TurnsBox)


def main():

    # Main Window Properties
    MainWindow.protocol("WM_DELETE_WINDOW", shutdown)
    MainWindow.title("Winder GUI")

    # Lay out the frames neatly
    ParametersFrame.grid(row=1)
    StatusFrame.grid(row=1, column=1)
    SerialEntryFrame.grid(row=3, column=0, columnspan=2)
    SerialMonitorFrame.grid(row=4, column=0, columnspan=2)

    # Stop everything crowding together
    MainWindow.grid_rowconfigure(0, minsize=50)
    MainWindow.grid_rowconfigure(2, minsize=100)

    # Bind button Procedures
    SendTextBox.bind('<Return>', send_button_handler, ())

    # Put non-grid objects onto the window
    CommandLabel.pack(side=LEFT)
    SendTextBox.pack(side=LEFT)
    SendButton.pack(side=LEFT)
    SerialMonitor.pack(side=BOTTOM)
    SerialMonitorScroll.pack(side=RIGHT, fill=Y)
    SerialMonitor.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
    SerialMonitorScroll.config(command=SerialMonitor.yview)
    SerialMonitorScroll.grid(row=0, column=1, sticky='nsew')
    SerialMonitor['yscrollcommand'] = SerialMonitorScroll.set

    # Show window
    MainWindow.mainloop()

if __name__ == '__main__':
    main()
