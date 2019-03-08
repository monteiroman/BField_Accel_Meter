# Import the LSM303 module.
import Adafruit_LSM303

from DataStructure.Data import DataStructure
from GUI.sensorGUI import *

# Macros
ANIM_INTVL = 1000        # Animation Interval in mS


def main():
    dataStruct = DataStructure()
    app = BMeasureApp(dataStruct=dataStruct)

    #ani = animation.FuncAnimation(f, animate, interval=ANIM_INTVL)

    lsm303 = Adafruit_LSM303.LSM303()

    #dataStruct.startElapsedTime()
    dataStruct.getZerosFromFile()
    # qmc.setZero(dataStruct.getZeros())

    while True:
        start = time.time()											# For debugging

        accel, mag = lsm303.read()
        dataStruct.setAxis(mag, accel)

        axisData = dataStruct.getAxis()
        #dataGraph(axisData, dataStruct.getElapsedTime())

        if dataStruct.getSaveDataStatus():
            dataStruct.SaveMeasureData()

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
