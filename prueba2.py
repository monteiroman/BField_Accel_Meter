import Adafruit_LSM303

from DataStructure.Data import DataStructure
from GUI.sensorGUI import *

import threading


class SensorThread(threading.Thread):
    def setSensor(self, sensor):
        self.sensor = sensor

    def setDataStruct(self, dataStruct):
        self.dataStruct = dataStruct

    def run(self):
        while True:
            start = time.time()                                                 # For debugging
            accel, mag = self.sensor.read()
            self.dataStruct.setAxis(mag, accel)
            end = time.time()                                                   # For debugging
            self.dataStruct.setSamplingRate(1/(end - start))					# For debugging
            if self.dataStruct.getQuitState():
                break

def updateData(app, dataStruct):
    app.updateData(dataStruct.getData)

def main():
    dataStruct = DataStructure()
    sensor = Adafruit_LSM303.LSM303()
    app = BMeasureApp(dataStruct=dataStruct)

    mythread = SensorThread(name = "SensorThread")
    mythread.setDataStruct(dataStruct)
    mythread.setSensor(sensor)

    mythread.start()

    while True:
        app.frames[MeasurePage].refreshLabel(dataStruct.getSceenType())
        winUpdate (app)
        time.sleep(.05)

    # tkinter.setup()
    # tkinter.mainloop()

if __name__ == '__main__':
    main()
