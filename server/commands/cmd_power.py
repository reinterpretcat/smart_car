from .common import Command

# Specifies led command


class PowerCommand():
    def __init__(self, adc, callback, isDryRun=True) -> None:
        self.adc = adc
        self.callback = callback
        self.isDryRun = isDryRun

    def name(self) -> Command:
        return Command.CMD_POWER

    def run(self, _data=None) -> None:
        if self.isDryRun:
            adc_power = 42
            print(f"{self.name()} simulating with {adc_power=}")
        else:
            adc_power = self.adc.recvADC(2) * 3

            self.callback([self.name(), str(round(adc_power, 2))])
