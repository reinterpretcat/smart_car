from .common import Command


class ServoCommand():
    def __init__(self, servo, isDryRun=True) -> None:
        self.servo = servo
        self.isDryRun = isDryRun

    def name(self) -> Command:
        return Command.CMD_SERVO

    def run(self, data) -> None:
        data1, data2 = data[0], int(data[1])

        if self.isDryRun:
            print(f"{self.name()}: {data1=}, {data2=}")
            return

        self.servo.setServoPwm(data1, data2)
