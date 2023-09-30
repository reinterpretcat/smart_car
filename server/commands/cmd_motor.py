from .common import Command


class MotorComand:
    def __init__(self, motor, isDryRun=True) -> None:
        self.motor = motor
        self.isDryRun = isDryRun

    def name(self) -> Command:
        return Command.CMD_MOTOR

    def run(self, data):
        data1, data2, data3, data4 = int(data[0]), int(data[1]), int(data[2]), int(data[3])

        if self.isDryRun:
            print(f"{self.name()}: {data1=}, {data2=}, {data3=}, {data4=}")
            return

        self.motor.setMotorModel(data1, data2, data3, data4)
