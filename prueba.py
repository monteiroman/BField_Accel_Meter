# Install -> Matplotlib
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
BFIELDSCREEN = 1
ACCSCREEN = 2

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

        for F in (SelectMeasurePage, StartPage, MeasurePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # self.show_frame(StartPage)
        time.sleep(4)
        self.show_frame(SelectMeasurePage)

        self.holdStatus = True


    def show_frame(self, cont, measureType = 0):
        if measureType is not 0:
            dataStruct.setScreenType(measureType)
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
                            #command=lambda: controller.show_frame(MeasurePage))
        #button.pack()

        self.img = ImageTk.PhotoImage(Image.open("/home/pi/BField_Accel_Meter/sources/pictures/logo1.png"))
        self.panel = Label(self, image = self.img)
        self.panel.pack()


class SelectMeasurePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        s = ttk.Style()
        s.configure('my.TButton', font=("Verdana", 16))


        buttonB = ttk.Button(self, text="Ir al medidor de campo", style='my.TButton',
                            command=lambda: controller.show_frame(MeasurePage, BFIELDSCREEN))
        buttonB.pack()

        buttonG = ttk.Button(self, text="Ir al medidor de aceleracion", style='my.TButton',
                            command=lambda: controller.show_frame(MeasurePage, ACCSCREEN))
        buttonG.pack()

        exitButton = ttk.Button(self, text="Salir", style='my.TButton',
                            command=lambda: controller.quitProgram())
        exitButton.pack()

        # self.img = ImageTk.PhotoImage(Image.open("/home/pi/BField_Accel_Meter/sources/pictures/logo1.png"))
        # self.panel = Label(self, image = self.img)
        # self.panel.pack()



class MeasurePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        s = ttk.Style()
        s.configure('my.TButton', font=("Verdana", 16))

        self.msg_Title = StringVar()
        self.msg_Title.set("Campo B")
        self.label = ttk.Label(self, textvariable=self.msg_Title, font=MEDIUM_FONT)
        self.label.grid(row=0, column=0, sticky="n")

        self.valuesFrame = tk.Frame(self)
        self.valuesFrame.grid(row=1, column=0, sticky="nsew")

        self.msg_x = StringVar()
        self.msg_x.set("---")
        self.msg_y = StringVar()
        self.msg_y.set("---")
        self.msg_z = StringVar()
        self.msg_z.set("---")
        self.msg_mod = StringVar()
        self.msg_mod.set("---")
        self.msg_elap = StringVar()
        self.msg_elap.set("---")
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
        self.labelMod = ttk.Label(self.valuesFrame, textvariable=self.msg_mod, font=MEDIUM_FONT)
        self.labelMod.grid(row=5, column=0, sticky="nsew")
        self.labelElap = ttk.Label(self.valuesFrame, textvariable=self.msg_elap, font=MEDIUM_FONT)
        self.labelElap.grid(row=6, column=0, sticky="nsew")

#---------------making size for the graph
        self.labelZ = ttk.Label(self.valuesFrame, text=" ", font=MEDIUM_FONT)
        self.labelZ.grid(row=7, column=0, sticky="nsew")
        self.holdButton = ttk.Button(self.valuesFrame, text="Hold", padding=(5,5), style='my.TButton', command=lambda: controller.holdMeasure())
        self.holdButton.grid(row=8, column=0, sticky="nsew")
        self.labelZ = ttk.Label(self.valuesFrame, text=" ", font=MEDIUM_FONT)
        self.labelZ.grid(row=9, column=0, sticky="nsew")
        self.measureButton = ttk.Button(self.valuesFrame, text="Guardar mediciones", padding=(5,5), style='my.TButton', command=lambda: controller.saveBtnClicked())
        self.measureButton.grid(row=10, column=0, sticky="nsew")
        self.labelZ = ttk.Label(self.valuesFrame, text=" ", font=MEDIUM_FONT)
        self.labelZ.grid(row=11, column=0, sticky="nsew")
        self.saveStatusLabel = ttk.Label(self.valuesFrame, textvariable=self.msg_saveStatus, font=SMALL_FONT)
        self.saveStatusLabel.grid(row=12, column=0, sticky="nsew")
        # self.labelZ = ttk.Label(self.valuesFrame, text=" ", font=MEDIUM_FONT)
        # self.labelZ.grid(row=12, column=0, sticky="nsew")
        # self.labelZ = ttk.Label(self.valuesFrame, text=" ", font=MEDIUM_FONT)
        # self.labelZ.grid(row=12, column=0, sticky="nsew")
        #self.labelZ = ttk.Label(self.valuesFrame, text=" ", font=MEDIUM_FONT)
        #self.labelZ.grid(row=13, column=0, sticky="nsew")
#---------------

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().grid(row=1, column=1, sticky="nsew")

        self.exitButton = ttk.Button(self, text="Atras", padding=(5,5), style='my.TButton', command=lambda: controller.show_frame(SelectMeasurePage))
        self.exitButton.grid(row=2, column=0, sticky="nsew")
        self.setZeroButton = ttk.Button(self, text="Setear ceros", padding=(5,5), style='my.TButton', command=lambda: controller.setQMCZeros())
        self.setZeroButton.grid(row=2, column=1, sticky="nsew")



    def refreshLabel (self, type):
        axis = dataStruct.getAxis()
        time = dataStruct.getElapsedTime()
        # tmp = float(time.seconds + (time.microseconds / 1000000))

        if type == BFIELDSCREEN:
            self.msg_Title.set("Campo B")
            self.msg_x.set(" X: {:.2f}".format(axis[0]) + " uT")
            self.msg_y.set(" Y: {:.2f}".format(axis[1]) + " uT")
            self.msg_z.set(" Z: {:.2f}".format(axis[2]) + " uT")
            self.msg_mod.set(" Mod: {:.2f}".format(axis[3]) + " uT")

        if type == ACCSCREEN:
            self.msg_Title.set("Aceleracion")
            self.msg_x.set(" X: {:.2f}".format(axis[4]) + " G")
            self.msg_y.set(" Y: {:.2f}".format(axis[5]) + " G")
            self.msg_z.set(" Z: {:.2f}".format(axis[6]) + " G")
            self.msg_mod.set(" Mod: {:.2f}".format(axis[7]) + " G")

        self.msg_elap.set(" Frec: {:.0f}".format(dataStruct.getSamplingRate()) + " HZ")

        if dataStruct.getSaveDataStatus():
            self.msg_saveStatus.set("   Guardando...")
        else:
            self.msg_saveStatus.set("   Listo para guardar")



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

        self.x_mag = 0
        self.y_mag = 0
        self.z_mag = 0
        self.x_zero_mag = 0
        self.y_zero_mag = 0
        self.z_zero_mag = 0
        self.mod_mag = 0

        self.x_acc = 0
        self.y_acc = 0
        self.z_acc = 0
        self.x_zero_acc = 0
        self.y_zero_acc = 0
        self.z_zero_acc = 0
        self.mod_acc = 0

        self.end_time = 0
        self.start_time = 0
        self.timeStamp = 0
        self.saveDataStatus = False
        self.measureQuantity = 0
        self.measureFile = 0

        self.measureSceenType = BFIELDSCREEN
        self.samplingRate = 0

    def setAxis (self, axis_mag, axis_accel):
        self.x_mag = axis_mag[0]/10
        self.y_mag = axis_mag[1]/10
        self.z_mag = axis_mag[2]/10
        self.mod_mag = math.sqrt(self.x_mag**2 + self.y_mag**2 + self.z_mag**2)

        self.x_acc = axis_accel[0]/1000
        self.y_acc = axis_accel[1]/1000
        self.z_acc = axis_accel[2]/1000
        self.mod_acc = math.sqrt(self.x_acc**2 + self.y_acc**2 + self.z_acc**2)

    def getAxis (self):
        return (self.x_mag, self.y_mag, self.z_mag, self.mod_mag, self.x_acc, self.y_acc, self.z_acc, self.mod_acc)

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
        self.x_zero_mag = self.x_mag
        self.y_zero_mag = self.y_mag
        self.z_zero_mag = self.z_mag

        self.x_zero_acc = self.x_acc
        self.y_zero_acc = self.y_acc
        self.z_zero_acc = self.z_acc

        saveZeros(self.x_zero_mag, self.y_zero_mag, self.z_zero_mag, self.x_zero_acc, self.y_zero_acc, self.z_zero_acc)

    def getZeros (self):
        return (self.x_zero_mag, self.y_zero_mag, self.z_zero_mag)

    def setRaw (self, raw_data):
        self.x_raw = raw_data[0]
        self.y_raw = raw_data[1]
        self.z_raw = raw_data[2]

    def getZerosFromFile (self):
        aux_x, aux_y, aux_z = readZerosFromFile()

        self.x_zero_mag = aux_x
        self.y_zero_mag = aux_y
        self.z_zero_mag = aux_z

    def getSaveDataStatus (self):
        return self.saveDataStatus

    def setSaveDataStatus (self, value):
        self.saveDataStatus = value

    def setScreenType (self, type):
        self.measureSceenType = type

    def getSceenType (self):
        return self.measureSceenType

    def setSamplingRate (self, sr):
        self.samplingRate = sr

    def getSamplingRate (self):
        return self.samplingRate


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



def saveZeros(x_mag, y_mag, z_mag):
    zeroFile = open("/home/pi/medidor_campo_b/zeros.txt", "w+")
    zeroFile.write(str(x_mag) + "," + str(y_mag) + "," + str(z_mag))
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

    #ani = animation.FuncAnimation(f, animate, interval=ANIM_INTVL)

    lsm303 = Adafruit_LSM303.LSM303()

    # qmc = Qmc()
    # qmc.QMCReg_Config()
    #
    #dataStruct.startElapsedTime()
    # dataStruct.getZerosFromFile()
    # qmc.setZero(dataStruct.getZeros())

    while True:
        start = time.time()											# For debugging
        dataStruct.startElapsedTime()
        accel, mag = lsm303.read()

        dataStruct.setAxis(mag, accel)
        # dataStruct.setRaw(qmc.getRawAxis())
        # qmc.setZero(dataStruct.getZeros())
        #qmc.ConsolePrint(dataStruct.getAxis())							# For debugging

        axisData = dataStruct.getAxis()
        #dataGraph(axisData, dataStruct.getElapsedTime())
        if dataStruct.getSaveDataStatus():
            SaveMeasureData(axisData)

		# if the user press the hold button
        if app.getHoldStatus():
            app.frames[MeasurePage].refreshLabel(dataStruct.getSceenType())

        winUpdate (app)

        # time.sleep(.0005)

        end = time.time()                                                           # For debugging
        dataStruct.setSamplingRate(1/(end - start))												# For debugging
        # print("Frecuencia: {:.0f}".format(1/(end - start)))							# For debugging

    return 0

if __name__ == '__main__':
    main()
