from .common import Command


class LedCommand():
    def __init__(self, led, isDryRun=True) -> None:
        self.led = led
        self.isDryRun = isDryRun

    def name(self) -> Command:
        return Command.CMD_LED

    def run(self, data) -> None:
        data1, data2, data3, data4 = int(data[0]), int(data[1]), int(data[2]), int(data[3])

        if self.isDryRun:
            print(f"{self.name()}: {data1=}, {data2=}, {data3=}, {data4=}")
            return

        self.led.ledIndex(data1, data2, data3, data4)
