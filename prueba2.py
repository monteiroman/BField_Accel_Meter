#
#
# program with Thread
#
#

import Adafruit_LSM303

from DataStructure.Data import DataStructure
from GUI.sensorGUI import *

import threading


class SensorThread(threading.Thread):
    def setSensor(self):
        self.sensor = Adafruit_LSM303.LSM303()

    def setDataStruct(self, dataStruct):
        self.dataStruct = dataStruct

    def run(self):
        while True:
            start = time.time()                                                 # For debugging
            try:
                accel, mag = self.sensor.read()
            except IOError:
                print("IOError in writeData, retrying.../n")
                time.sleep(0.5)                                                 # waits a moment to reconect
                self.sensor = Adafruit_LSM303.LSM303()
                accel, mag = self.sensor.read()
            self.dataStruct.setAxis(mag, accel)
            end = time.time()                                                   # For debugging
            self.dataStruct.setSamplingRate(1/(end - start))					# For debugging
            if self.dataStruct.getQuitState():
                break


def main():
    dataStruct = DataStructure()
    app = BMeasureApp(dataStruct=dataStruct)

    mythread = SensorThread(name = "SensorThread")
    mythread.setDataStruct(dataStruct)
    mythread.setSensor()

    mythread.start()

    while True:
        if dataStruct.getSaveDataStatus():
            dataStruct.SaveMeasureData()

        if app.getHoldStatus():
            app.frames[MeasurePage].refreshLabel(dataStruct.getSceenType())

        winUpdate (app)
        # time.sleep(0.0005)

if __name__ == '__main__':
    main()
