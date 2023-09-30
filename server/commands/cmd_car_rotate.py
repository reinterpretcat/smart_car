import math
from threading import Thread
from .common import Command
from utils.thread import stopThread


class CarRotateCommand:
    def __init__(self, motor, isDryRun=True) -> None:
        self.motor = motor
        self.isDryRun = isDryRun
        self.rotationFlag = False

    def name(self) -> Command:
        return Command.CMD_CAR_ROTATE

    def run(self, data) -> None:
        data1, data2, data3, data4 = int(data[0]), int(data[1]), int(data[2]), int(data[3])

        if data4 == 0:
            self.rotationFlag = False
            LX = -int((data2 * math.sin(math.radians(data1))))
            LY = int(data2 * math.cos(math.radians(data1)))
            RX = int(data4 * math.sin(math.radians(data3)))
            RY = int(data4 * math.cos(math.radians(data3)))

            FR, FL, BL, BR = LY - LX + RX, LY + LX - RX, LY - LX - RX, LY + LX + RX

            if self.isDryRun:
                print(
                    f"{self.name()}: {data1=}, {data2=}, {data3=}, {data4=}, {FR=}, {FL=}, {BL=} {BR=}")
                return

            self.motor.setMotorModel(FL, BL, FR, BR)

        elif self.rotationFlag == False:
            self.rotationFlag = True
            if self.isDryRun:
                print(
                    f"{self.name()}: {data1=}, {data2=}, {data3=}, {data4=}, rotate")
            else:
                self.rotateRun = Thread(target=self.motor.rotate, args=(data3,))
                self.rotateRun.start()

    def stop(self):
        try:
            self.motor.rotatable = False
            if hasattr(self, 'rotateRun'):
                stopThread(self.rotateRun)
        except:
            pass
