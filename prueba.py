# Import the LSM303 module.
import Adafruit_LSM303

from DataStructure.Data import DataStructure
from GUI.sensorGUI import *

# Macros
GRAPHLENGTH = 50         # Quantity of points in the x axis of thee graph
ANIM_INTVL = 1000        # Animation Interval in mS
AVERAGE_ARRAY_SIZE = 50  # Array size of the average filter
SAVEMEASURELENGTH = 50   # Quantity of measures saved in the file




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

def SaveMeasureData (dataStruct):
    if dataStruct.measureQuantity == 0: 									# Only open it if it is the first measure
        dataStruct.measureFile = open("/home/pi/BField_Accel_Meter/data.txt", "w+")

    dataStruct.measureFile.write(str(dataStruct.x_mag) + "," +
                                str(dataStruct.y_mag) + "," +
                                str(dataStruct.z_mag) + "," +
                                str(dataStruct.x_acc) + "," +
                                str(dataStruct.y_acc) + "," +
                                str(dataStruct.z_acc) + "\n")
    dataStruct.measureQuantity = dataStruct.measureQuantity +1

    if dataStruct.measureQuantity == SAVEMEASURELENGTH:
        dataStruct.setSaveDataStatus(False)
        dataStruct.measureQuantity = 0
        dataStruct.measureFile.close()
        return




def main():
    dataStruct = DataStructure()
    app = BMeasureApp(dataStruct=dataStruct)

    #ani = animation.FuncAnimation(f, animate, interval=ANIM_INTVL)

    lsm303 = Adafruit_LSM303.LSM303()

    # qmc = Qmc()
    # qmc.QMCReg_Config()
    #
    #dataStruct.startElapsedTime()
    dataStruct.getZerosFromFile()
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
            SaveMeasureData(dataStruct)

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
