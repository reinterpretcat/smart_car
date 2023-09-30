import math
from .common import Command


class MMotorComand:
    def __init__(self, motor, isDryRun=True) -> None:
        self.motor = motor
        self.isDryRun = isDryRun

    def name(self) -> Command:
        return Command.CMD_M_MOTOR

    def run(self, data):
        # found in C++ source code the following:
        # data[0] represents the Angle to the the Y-axis,Counterclockwise is 0 to 180 degrees
        # data[1] represents the move speed(the first jostick)
        # data[2] represents the Angle to the Y-axis,Counterclockwise is 0 to 180 degrees
        # converts data from the client to its x and y axis positions

        data1, data2, data3, data4 = int(data[0]), int(data[1]), int(data[2]), int(data[3])

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
