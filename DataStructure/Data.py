# This structure provides communication between the events of the GUI
# and the secuential part of the program
import time
import datetime
import math

BFIELDCORRECTION = 0.1
ACCCORRECTION = 0.001

AVERAGE_ARRAY_SIZE = 100  # Array size of the average filter
SAVEMEASURELENGTH = 50   # Quantity of measures saved in the file

BFIELDSCREEN = 1
ACCSCREEN = 2

class DataStructure (object):
    def __init__(self, *args, **kwargs):
        # Graph lists
        self.xGraphList = []
        self.yGraphList = []
        self.zGraphList = []

        self.timeGraphList = []

        self.x_mag           = 0
        self.y_mag           = 0
        self.z_mag           = 0
        self.mod_mag         = 0
        self.x_mag_raw       = 0
        self.y_mag_raw       = 0
        self.z_mag_raw       = 0
        self.x_zero_mag      = 0
        self.y_zero_mag      = 0
        self.z_zero_mag      = 0
        self.x_avg_mag       = 0
        self.y_avg_mag       = 0
        self.z_avg_mag       = 0
        self.mod_avg_mag     = 0

        self.x_acc           = 0
        self.y_acc           = 0
        self.z_acc           = 0
        self.mod_acc         = 0
        self.x_acc_raw       = 0
        self.y_acc_raw       = 0
        self.z_acc_raw       = 0
        self.x_zero_acc      = 0
        self.y_zero_acc      = 0
        self.z_zero_acc      = 0
        self.x_avg_acc       = 0
        self.y_avg_acc       = 0
        self.z_avg_acc       = 0
        self.mod_avg_acc     = 0

        self.end_time        = 0
        self.start_time      = 0
        self.timeStamp       = 0
        self.saveDataStatus  = False
        self.quitState       = False
        self.measureQuantity = 0
        self.measureFile     = 0

        self.measureSceenType = BFIELDSCREEN
        self.samplingRate    = 0

        self.xAverageArray_mag = [0] * AVERAGE_ARRAY_SIZE
        self.yAverageArray_mag = [0] * AVERAGE_ARRAY_SIZE
        self.zAverageArray_mag = [0] * AVERAGE_ARRAY_SIZE
        self.xAverageArray_acc = [0] * AVERAGE_ARRAY_SIZE
        self.yAverageArray_acc = [0] * AVERAGE_ARRAY_SIZE
        self.zAverageArray_acc = [0] * AVERAGE_ARRAY_SIZE

    def setAxis (self, axis_mag, axis_accel):
        self.x_mag_raw = axis_mag[0]
        self.y_mag_raw = axis_mag[1]
        self.z_mag_raw = axis_mag[2]
        self.x_mag = (self.x_mag_raw - self.x_zero_mag) * BFIELDCORRECTION
        self.y_mag = (self.y_mag_raw - self.y_zero_mag) * BFIELDCORRECTION
        self.z_mag = (self.z_mag_raw - self.z_zero_mag) * BFIELDCORRECTION
        self.mod_mag = math.sqrt(self.x_mag**2 + self.y_mag**2 + self.z_mag**2)

        self.x_acc_raw = axis_accel[0]
        self.y_acc_raw = axis_accel[1]
        self.z_acc_raw = axis_accel[2]
        self.x_acc = (self.x_acc_raw - self.x_zero_acc) * ACCCORRECTION
        self.y_acc = (self.y_acc_raw - self.y_zero_acc) * ACCCORRECTION
        self.z_acc = (self.z_acc_raw - self.z_zero_acc) * ACCCORRECTION
        self.mod_acc = math.sqrt(self.x_acc**2 + self.y_acc**2 + self.z_acc**2)

        self.avgFilter()

        self.mod_avg_mag = math.sqrt(self.x_avg_mag**2 + self.y_avg_mag**2 +
                                        self.z_avg_mag**2)
        self.mod_avg_acc = math.sqrt(self.x_avg_acc**2 + self.y_avg_acc**2 +
                                        self.z_avg_acc**2)

    def getAxis (self):
        return (self.x_avg_mag, self.y_avg_mag, self.z_avg_mag, self.mod_avg_mag,
                self.x_avg_acc, self.y_avg_acc, self.z_avg_acc, self.mod_avg_acc)

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
        self.x_zero_mag = self.x_mag_raw
        self.y_zero_mag = self.y_mag_raw
        self.z_zero_mag = self.z_mag_raw

        self.x_zero_acc = self.x_acc_raw
        self.y_zero_acc = self.y_acc_raw
        self.z_zero_acc = self.z_acc_raw

        saveZeros(self.x_zero_mag, self.y_zero_mag, self.z_zero_mag,
                            self.x_zero_acc, self.y_zero_acc, self.z_zero_acc)

    def getZeros (self):
        return (self.x_zero_mag, self.y_zero_mag, self.z_zero_mag,
                            self.x_zero_acc, self.y_zero_acc, self.z_zero_acc)

    def setRaw (self, raw_data):
        self.x_raw = raw_data[0]
        self.y_raw = raw_data[1]
        self.z_raw = raw_data[2]

    def getZerosFromFile (self):
        aux_x_mag, aux_y_mag, aux_z_mag, aux_x_acc, aux_y_acc, aux_z_acc = readZerosFromFile()

        self.x_zero_mag = aux_x_mag
        self.y_zero_mag = aux_y_mag
        self.z_zero_mag = aux_z_mag
        self.x_zero_acc = aux_x_acc
        self.y_zero_acc = aux_y_acc
        self.z_zero_acc = aux_z_acc

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

    def avgFilter (self):
        self.xSum_mag = 0
        self.ySum_mag = 0
        self.zSum_mag = 0
        self.xSum_acc = 0
        self.ySum_acc = 0
        self.zSum_acc = 0
        self.xAverageArray_mag.append(self.x_mag)
        self.xAverageArray_mag.pop(0)
        self.yAverageArray_mag.append(self.y_mag)
        self.yAverageArray_mag.pop(0)
        self.zAverageArray_mag.append(self.z_mag)
        self.zAverageArray_mag.pop(0)
        self.xAverageArray_acc.append(self.x_acc)
        self.xAverageArray_acc.pop(0)
        self.yAverageArray_acc.append(self.y_acc)
        self.yAverageArray_acc.pop(0)
        self.zAverageArray_acc.append(self.z_acc)
        self.zAverageArray_acc.pop(0)

        for i in range(0, AVERAGE_ARRAY_SIZE):
            self.xSum_mag = self.xSum_mag + self.xAverageArray_mag[i]
            self.ySum_mag = self.ySum_mag + self.yAverageArray_mag[i]
            self.zSum_mag = self.zSum_mag + self.zAverageArray_mag[i]
            self.xSum_acc = self.xSum_acc + self.xAverageArray_acc[i]
            self.ySum_acc = self.ySum_acc + self.yAverageArray_acc[i]
            self.zSum_acc = self.zSum_acc + self.zAverageArray_acc[i]


        self.x_avg_mag = float(self.xSum_mag / AVERAGE_ARRAY_SIZE)
        self.y_avg_mag = float(self.ySum_mag / AVERAGE_ARRAY_SIZE)
        self.z_avg_mag = float(self.zSum_mag / AVERAGE_ARRAY_SIZE)
        self.x_avg_acc = float(self.xSum_acc / AVERAGE_ARRAY_SIZE)
        self.y_avg_acc = float(self.ySum_acc / AVERAGE_ARRAY_SIZE)
        self.z_avg_acc = float(self.zSum_acc / AVERAGE_ARRAY_SIZE)

    def SaveMeasureData (self):
        if self.measureQuantity == 0: 									# Only open it if it is the first measure
            self.measureFile = open("/home/pi/BField_Accel_Meter/data.txt", "w+")

        self.measureFile.write(str(self.x_avg_mag) + "," +
                               str(self.y_avg_mag) + "," +
                               str(self.z_avg_mag) + "," +
                               str(self.x_avg_acc) + "," +
                               str(self.y_avg_acc) + "," +
                               str(self.z_avg_acc) + "\n")
        self.measureQuantity = self.measureQuantity +1

        if self.measureQuantity == SAVEMEASURELENGTH:
            self.setSaveDataStatus(False)
            self.measureQuantity = 0
            self.measureFile.close()
            return

    def setQuitState (self):
        self.quitState = True

    def getQuitState (self):
        return self.quitState

    def getPpValues (self):
        xMax_mag = max(self.xAverageArray_mag)
        xMin_mag = min(self.xAverageArray_mag)
        yMax_mag = max(self.yAverageArray_mag)
        yMin_mag = min(self.yAverageArray_mag)
        zMax_mag = max(self.zAverageArray_mag)
        zMin_mag = min(self.zAverageArray_mag)

        xMax_acc = max(self.xAverageArray_acc)
        xMin_acc = min(self.xAverageArray_acc)
        yMax_acc = max(self.yAverageArray_acc)
        yMin_acc = min(self.yAverageArray_acc)
        zMax_acc = max(self.zAverageArray_acc)
        zMin_acc = min(self.zAverageArray_acc)

        xPp_mag = xMax_mag - xMin_mag
        yPp_mag = yMax_mag - yMin_mag
        zPp_mag = zMax_mag - zMin_mag

        xPp_acc = xMax_acc - xMin_acc
        yPp_acc = yMax_acc - yMin_acc
        zPp_acc = zMax_acc - zMin_acc

        return xPp_mag, yPp_mag, zPp_mag, xPp_acc, yPp_acc, zPp_acc


def saveZeros(x_mag, y_mag, z_mag, x_acc, y_acc, z_acc):
    zeroFile = open("/home/pi/BField_Accel_Meter/zeros.txt", "w+")
    zeroFile.write(str(x_mag) + "," + str(y_mag) + "," + str(z_mag) + "," +
                            str(x_acc) + "," + str(y_acc) + "," + str(z_acc))
    zeroFile.close()

def readZerosFromFile ():
    try:
        zeroFile = open("/home/pi/BField_Accel_Meter/zeros.txt", "r")
    except:
        zeroFile = open("/home/pi/BField_Accel_Meter/zeros.txt", "w+")
        zeroFile.write("0,0,0,0,0,0")
        zeroFile.close()
        zeroFile = open("/home/pi/BField_Accel_Meter/zeros.txt", "r")

    zeroString = zeroFile.read()

    x_m,y_m,z_m,x_a,y_a,z_a = zeroString.split(",")
    x_mag = float(x_m)
    y_mag = float(y_m)
    z_mag = float(z_m)
    x_acc = float(x_a)
    y_acc = float(y_a)
    z_acc = float(z_a)

    zeroFile.close()
    return (x_mag,y_mag,z_mag,x_acc,y_acc,z_acc)
