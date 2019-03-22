#
#
# program with Process
#
#

import Adafruit_LSM303
import os

from DataStructure.Data import DataStructure
from GUI.sensorGUI import *

from multiprocessing import Process, Queue


class SensorProcess(sensor, dataStruct):
    # self.sensor = sensor
    # self.datastruct = dataStruct

    while True:
        start = time.time()                                                 # For debugging
        accel, mag = sensor.read()
        dataStruct.setAxis(mag, accel)
        end = time.time()                                                   # For debugging
        dataStruct.setSamplingRate(1/(end - start))					# For debugging
        if dataStruct.getQuitState():
            break


def main():
    dataStruct = DataStructure()
    sensor = Adafruit_LSM303.LSM303()
    app = BMeasureApp(dataStruct=dataStruct)

    myprocess = Process(target=SensorProcess, args=(sensor, dataStruct,))
    myprocess.start()

    while True:
        if dataStruct.getSaveDataStatus():
            dataStruct.SaveMeasureData()

        if app.getHoldStatus():
            app.frames[MeasurePage].refreshLabel(dataStruct.getSceenType())

        winUpdate (app)
        # time.sleep(.05)

    # tkinter.setup()
    # tkinter.mainloop()

if __name__ == '__main__':
    main()
