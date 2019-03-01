# Install -> Matplotlib
#         -> Smbus
#         -> PIL for showing the image at the start. For install it do:
#               sudo apt-get install python3-pil python3-pil.imagetk

#RPi Pinouts
    #I2C Pins
        #GPIO2 -> SDA
        #GPIO3 -> SCL

# Matplotlib imports
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

# Tkinter imports
import tkinter as tk
from tkinter import ttk, font
from tkinter import *
from PIL import ImageTk, Image

#import pandas as pd
#import numpy as np

# General imports
import smbus
import time
import math
import getpass
import subprocess
import datetime

# Import the LSM303 module.
import Adafruit_LSM303


# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
# Slave Address 1
address = 0x0D


LARGE_FONT = ("Verdana", 24)
MEDIUM_FONT = ("Verdana", 18)
SMALL_FONT = ("Verdana", 14)
style.use("ggplot")

f = Figure(figsize=(7,3), dpi=78)
a = f.add_subplot(111)






# Macros
GRAPHLENGTH = 50         # Quantity of points in the x axis of thee graph
ANIM_INTVL = 1000        # Animation Interval in mS
AVERAGE_ARRAY_SIZE = 50  # Array size of the average filter
SAVEMEASURELENGTH = 50   # Quantity of measures saved in the file

#_________________________CLASSES DEFINITIONS________________________________#
#--------------------------------------------------------------------------------------#
# Tkinter Clases
class BMeasureApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.tk = tk.Tk()

        self.tk.attributes("-fullscreen", True)
        self.tk.title("Medidor de campo B")

        container = tk.Frame(self.tk)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        time.sleep(4)
        self.show_frame(PageOne)

        self.holdStatus = True


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def quitProgram (self):
        self.tk.destroy()

    def holdMeasure (self):
        if self.holdStatus:
            self.holdStatus = False
        else:
            self.holdStatus = True

    def getHoldStatus (self):
        return self.holdStatus

    def setQMCZeros (self):
        dataStruct.setZeros()

    def saveBtnClicked (self):
        dataStruct.setSaveDataStatus(True)



class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        s = ttk.Style()
        s.configure('my.TButton', font=("Verdana", 16))

        label = tk.Label(self, text="Medidor de Campo B", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text="Trabajo Practico realizado para la materia Medidas Electrónicas I", font=MEDIUM_FONT)
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text="de la facultad regional Buenos Aires de la UTN.", font=MEDIUM_FONT)
        label.pack(pady=10,padx=10)

        # If we want the start button
        #button = ttk.Button(self, text="Ir al medidor", style='my.TButton',
                            #command=lambda: controller.show_frame(PageOne))
        #button.pack()

        self.img = ImageTk.PhotoImage(Image.open("/home/pi/medidor_campo_b/sources/pictures/logo1.png"))
        self.panel = Label(self, image = self.img)
        self.panel.pack()



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        s = ttk.Style()
        s.configure('my.TButton', font=("Verdana", 16))

        label = tk.Label(self, text="Campo B", font=MEDIUM_FONT)
        label.grid(row=0, column=0, sticky="n")

        self.valuesFrame = tk.Frame(self)
        self.valuesFrame.grid(row=1, column=0, sticky="nsew")

        self.msg_x = StringVar()
        self.msg_x.set("---")
        self.msg_y = StringVar()
        self.msg_y.set("---")
        self.msg_z = StringVar()
        self.msg_z.set("---")
        self.msg_saveStatus = StringVar()
        self.msg_saveStatus.set("    Listo para guardar")

        self.separator = ttk.Label(self.valuesFrame, text="--------------------", font=LARGE_FONT)
        self.separator.grid(row=1, column=0, sticky="nsew")
        self.labelX = ttk.Label(self.valuesFrame, textvariable=self.msg_x, font=MEDIUM_FONT)
        self.labelX.grid(row=2, column=0, sticky="nsew")
        self.labelY = ttk.Label(self.valuesFrame, textvariable=self.msg_y, font=MEDIUM_FONT)
        self.labelY.grid(row=3, column=0, sticky="nsew")
        self.labelZ = ttk.Label(self.valuesFrame, textvariable=self.msg_z, font=MEDIUM_FONT)
        self.labelZ.grid(row=4, column=0, sticky="nsew")

#---------------making size for the graph
        self.labelZ = ttk.Label(self.valuesFrame, text=" ", font=MEDIUM_FONT)
        self.labelZ.grid(row=5, column=0, sticky="nsew")
        self.holdButton = ttk.Button(self.valuesFrame, text="Hold", padding=(5,5), style='my.TButton', command=lambda: controller.holdMeasure())
        self.holdButton.grid(row=6, column=0, sticky="nsew")
        self.labelZ = ttk.Label(self.valuesFrame, text=" ", font=MEDIUM_FONT)
        self.labelZ.grid(row=7, column=0, sticky="nsew")
        self.measureButton = ttk.Button(self.valuesFrame, text="Guardar mediciones", padding=(5,5), style='my.TButton', command=lambda: controller.saveBtnClicked())
        self.measureButton.grid(row=8, column=0, sticky="nsew")
        self.labelZ = ttk.Label(self.valuesFrame, text=" ", font=MEDIUM_FONT)
        self.labelZ.grid(row=9, column=0, sticky="nsew")
        self.saveStatusLabel = ttk.Label(self.valuesFrame, textvariable=self.msg_saveStatus, font=SMALL_FONT)
        self.saveStatusLabel.grid(row=10, column=0, sticky="nsew")
        self.labelZ = ttk.Label(self.valuesFrame, text=" ", font=MEDIUM_FONT)
        self.labelZ.grid(row=11, column=0, sticky="nsew")
        self.labelZ = ttk.Label(self.valuesFrame, text=" ", font=MEDIUM_FONT)
        self.labelZ.grid(row=12, column=0, sticky="nsew")
        #self.labelZ = ttk.Label(self.valuesFrame, text=" ", font=MEDIUM_FONT)
        #self.labelZ.grid(row=13, column=0, sticky="nsew")
#---------------

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().grid(row=1, column=1, sticky="nsew")

        self.exitButton = ttk.Button(self, text="Salir", padding=(5,5), style='my.TButton', command=lambda: controller.quitProgram())
        self.exitButton.grid(row=2, column=0, sticky="nsew")
        self.setZeroButton = ttk.Button(self, text="Setear ceros", padding=(5,5), style='my.TButton', command=lambda: controller.setQMCZeros())
        self.setZeroButton.grid(row=2, column=1, sticky="nsew")



    def refreshLabel (self):
        axis = dataStruct.getAxis()

        self.msg_x.set(" X: {:.2f}".format(axis[0]) + " uT")
        self.msg_y.set(" Y: {:.2f}".format(axis[1]) + " uT")
        self.msg_z.set(" Z: {:.2f}".format(axis[2]) + " uT")

        if dataStruct.getSaveDataStatus():
            self.msg_saveStatus.set("   Guardando...")
        else:
            self.msg_saveStatus.set("   Listo para guardar")



#--------------------------------------------------------------------------------------#
# QMC Class (i2c communication)
class Qmc():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.x_raw = 0
        self.y_raw = 0
        self.z_raw = 0
        self.x_zero = 0
        self.y_zero = 0
        self.z_zero = 0
        self.myfilter = averageFilter()
        self.avgAux = []
        #self.correction = 0.0244140625       # 16*1000000/(65536*10000)
                                             # --> ([rango_en_G * paso_a_uT / [nCuentas_ADC * Gauss_a_Tesla])
                                             #
        #self.correction = 0.033333333        # or if we use the info from de QMC's datasheet:
                                             # 1000000/(10000*3000)  <-- +-8G
        self.correction = 0.00833333333      # 1000000/(10000*12000)  <-- +-2G


    # Writes the byte "data" in the device at "addr" at the "reg" register
    def WriteByteData (self, addr, reg, data):
        try:
                bus.write_byte_data(addr, reg, data)
        except IOError:
                print("IOError in writeData, retrying.../n")
                subprocess.call(['i2cdetect', '-y', '1'])
                bus.write_byte_data(addr, reg, data)
        return


    # Writes the byte "data" in the device at "addr"
    def WriteByte (self, addr, data):
        try:
                bus.write_byte(addr, data)
        except IOError:
                print("IOError in writeData, retrying.../n")
                subprocess.call(['i2cdetect', '-y', '1'])		# If the sensor fails to receive the data i2cdetect revives it
                bus.write_byte(addr, data)
        return


    #QMC REGISTER configuration
    def QMCReg_Config (self):
        # SET/RESET Period register (0x0B)
        self.WriteByteData(address, 0x0B, 0x01)                 # It is recommended that the register 0BH is written by 0x01
        time.sleep(.1)

        # Control register 1 (0x09)
        self.WriteByteData(address, 0x09, 0x0D)                 # Continuous Measure Mode - 200Hz Output Data Rate - 2G Full Scale (0x1D if +-8G)- Over Sample Rate 512
        time.sleep(.1)
        print("QMC Configured...")


    def ReadByte (self, device_addr, reg_ini):
        # Tells the QMC what register is going to be read
        # Starting with register reg_ini.
        self.WriteByte (device_addr, reg_ini)

        # Read the data..
        aux = bus.read_i2c_block_data(device_addr, reg_ini, 2)

        data =  aux[0]                                    #LSB
        data |= aux[1] << 8;                              #MSB

        # Converts to 2 complements and returns
        if data > 32767:
            return int((65536-data) * (-1))
        else:
            return int(data)


    def ConsolePrint (self, axis):
        s = 'x=' + repr(axis[0]) + '\t  y=' + repr(axis[1]) + '\t  z=' + repr(axis[2]) + '\t  Modulo=' + repr(axis[3])
        print(s)


    def getAxis (self):
        xAux = float('%.2f'%(self.ReadByte(address,0x00) * self.correction))
        yAux = float('%.2f'%(self.ReadByte(address,0x02) * self.correction))
        zAux = float('%.2f'%(self.ReadByte(address,0x04) * self.correction))
        avgAux = self.myfilter.filterAvg([xAux, yAux, zAux])
        self.x_raw = avgAux[0]
        self.y_raw = avgAux[1]
        self.z_raw = avgAux[2]
        self.x = self.x_raw - self.x_zero
        self.y = self.y_raw - self.y_zero
        self.z = self.z_raw - self.z_zero

        self.mod = math.sqrt(self.x**2 + self.y**2 + self.z**2)

        return [self.x, self.y, self.z, self.mod]


    def setZero (self, zeros):
        self.x_zero = zeros[0]
        self.y_zero = zeros[1]
        self.z_zero = zeros[2]

    def getRawAxis (self):
        return [self.x_raw, self.y_raw, self.z_raw]



class averageFilter ():

    def __init__(self, *args, **kwargs):
        self.xAverageArray = [0] * AVERAGE_ARRAY_SIZE
        self.yAverageArray = [0] * AVERAGE_ARRAY_SIZE
        self.zAverageArray = [0] * AVERAGE_ARRAY_SIZE
        self.average = ["x", "y", "z"]

    def filterAvg (self, axis):
        self.xSum = 0
        self.ySum = 0
        self.zSum = 0
        self.xAverageArray.append(axis[0])
        self.xAverageArray.pop(0)
        self.yAverageArray.append(axis[1])
        self.yAverageArray.pop(0)
        self.zAverageArray.append(axis[2])
        self.zAverageArray.pop(0)

        for i in range(0, AVERAGE_ARRAY_SIZE):
            self.xSum = self.xSum + self.xAverageArray[i]
            self.ySum = self.ySum + self.yAverageArray[i]
            self.zSum = self.zSum + self.zAverageArray[i]

        self.average[0] = float('%.2f'%(self.xSum / AVERAGE_ARRAY_SIZE))
        self.average[1] = float('%.2f'%(self.ySum / AVERAGE_ARRAY_SIZE))
        self.average[2] = float('%.2f'%(self.zSum / AVERAGE_ARRAY_SIZE))

        return(self.average)


# This structure provides communication between the events of the GUI
# and the secuential part of the program
class DataStructure ():
    def __init__(self, *args, **kwargs):
        # Graph lists
        self.xGraphList = []
        self.yGraphList = []
        self.zGraphList = []
        self.timeGraphList = []

        self.x = 0
        self.y = 0
        self.z = 0
        self.x_raw = 0
        self.y_raw = 0
        self.z_raw = 0
        self.x_zero = 0
        self.y_zero = 0
        self.z_zero = 0
        self.mod = 0
        self.end_time = 0
        self.start_time = 0
        self.timeStamp = 0
        self.saveDataStatus = False
        self.measureQuantity = 0
        self.measureFile = 0

    def setAxis (self, axis):
        self.x = axis[0]
        self.y = axis[1]
        self.z = axis[2]
        # self.mod = axis[3]

    def getAxis (self):
        return (self.x, self.y, self.z, self.mod)

    def startElapsedTime (self):
        self.start_time = datetime.datetime.now()

    def getElapsedTime (self):
        self.end_time = datetime.datetime.now()
        return (self.end_time - self.start_time)

    def zAppend (self, data):
        self.zGraphList.append(data)

    def yAppend (self, data):
        self.yGraphList.append(data)

    def xAppend (self, data):
        self.xGraphList.append(data)

    def timeAppend (self, data):
        self.timeGraphList.append(data)

    def popZList(self):
        self.zGraphList.pop(0)

    def popYList(self):
        self.yGraphList.pop(0)

    def popXList(self):
        self.xGraphList.pop(0)

    def popTimeList(self):
        self.timeGraphList.pop(0)

    def setZeros (self):
        self.x_zero = self.x_raw
        self.y_zero = self.y_raw
        self.z_zero = self.z_raw

        saveZeros(self.x_zero, self.y_zero, self.z_zero)

    def getZeros (self):
        return (self.x_zero, self.y_zero, self.z_zero)

    def setRaw (self, raw_data):
        self.x_raw = raw_data[0]
        self.y_raw = raw_data[1]
        self.z_raw = raw_data[2]

    def getZerosFromFile (self):
        aux_x, aux_y, aux_z = readZerosFromFile()

        self.x_zero = aux_x
        self.y_zero = aux_y
        self.z_zero = aux_z

    def getSaveDataStatus (self):
        return self.saveDataStatus

    def setSaveDataStatus (self, value):
        self.saveDataStatus = value


dataStruct = DataStructure ()



#_________________________FUNCTIONS DEFINITIONS________________________________#
def winUpdate (app):
    app.update_idletasks()
    app.update()



def animate(i):
    a.clear()

    a.plot(dataStruct.timeGraphList, dataStruct.xGraphList,
        dataStruct.timeGraphList, dataStruct.yGraphList,
        dataStruct.timeGraphList, dataStruct.zGraphList)
    a.legend(("Eje X", "Eje Y", "Eje Z"), loc="upper right")
    a.set_title("Campo B en eje Z")
    a.set(xlabel='Tiempo [S]', ylabel='[uT]')
    a.axis(ymin=0, ymax=53)



def saveZeros(x, y, z):
    zeroFile = open("/home/pi/medidor_campo_b/zeros.txt", "w+")
    zeroFile.write(str(x) + "," + str(y) + "," + str(z))
    zeroFile.close()



def readZerosFromFile ():
    try:
        zeroFile = open("/home/pi/medidor_campo_b/zeros.txt", "r")
    except:
        zeroFile = open("/home/pi/medidor_campo_b/zeros.txt", "w+")
        zeroFile.write("0,0,0")
        zeroFile.close()
        zeroFile = open("/home/pi/medidor_campo_b/zeros.txt", "r")

    zeroString = zeroFile.read()

    x,y,z = zeroString.split(",")
    x = float(x)
    y = float(y)
    z = float(z)

    zeroFile.close()
    return (x,y,z)



def dataGraph (axis, timeStamp):

    x_axis = axis[0]
    y_axis = axis[1]
    z_axis = axis[2]
    tmp = float(timeStamp.seconds + (timeStamp.microseconds / 1000000))

    if len(dataStruct.timeGraphList) <= GRAPHLENGTH:
        dataStruct.timeAppend(tmp)
        #z_axis_g=float('%.1f'%z_axis)									#set decimals to a requested value for graph
        #dataStruct.zAppend(z_axis_g)
        dataStruct.xAppend(abs(x_axis))
        dataStruct.yAppend(abs(y_axis))
        dataStruct.zAppend(abs(z_axis))


    else:
        dataStruct.popTimeList()
        dataStruct.timeAppend(tmp)
        dataStruct.popXList()
        dataStruct.popYList()
        dataStruct.popZList()
        #z_axis_g=float('%.1f'%z_axis)                                  #set decimals to a requested value for graph
        #dataStruct.zAppend(z_axis_g)
        dataStruct.xAppend(abs(x_axis))
        dataStruct.yAppend(abs(y_axis))
        dataStruct.zAppend(abs(z_axis))

    #print( timeStamp.seconds, ":", timeStamp.microseconds)				# For debugging

def SaveMeasureData (axis):
    if dataStruct.measureQuantity == 0: 									# Only open it if there is the first measure
        dataStruct.measureFile = open("/home/pi/medidor_campo_b/data.txt", "w+")

    dataStruct.measureFile.write(str(axis[0]) + "," + str(axis[1]) + "," + str(axis[2]) + "\n")
    dataStruct.measureQuantity = dataStruct.measureQuantity +1

    if dataStruct.measureQuantity == SAVEMEASURELENGTH:
        dataStruct.setSaveDataStatus(False)
        dataStruct.measureQuantity = 0
        dataStruct.measureFile.close()
        return




def main():
    app = BMeasureApp()

    ani = animation.FuncAnimation(f, animate, interval=ANIM_INTVL)

    lsm303 = Adafruit_LSM303.LSM303()

    # qmc = Qmc()
    # qmc.QMCReg_Config()
    #
    dataStruct.startElapsedTime()
    # dataStruct.getZerosFromFile()
    # qmc.setZero(dataStruct.getZeros())

    while True:
        #start = time.time()											# For debugging

        accel, mag = lsm303.read()

        dataStruct.setAxis(accel)
        # dataStruct.setRaw(qmc.getRawAxis())
        # qmc.setZero(dataStruct.getZeros())
        #qmc.ConsolePrint(dataStruct.getAxis())							# For debugging

        axisData = dataStruct.getAxis()
        dataGraph(axisData, dataStruct.getElapsedTime())
        if dataStruct.getSaveDataStatus():
            SaveMeasureData(axisData)

		# if the user press the hold button
        if app.getHoldStatus():
            app.frames[PageOne].refreshLabel()

        winUpdate (app)

        #end = time.time()												# For debugging
        #print("TIEMPO: " + str(end - start))							# For debugging

        time.sleep(.05)

    return 0

if __name__ == '__main__':
    main()
