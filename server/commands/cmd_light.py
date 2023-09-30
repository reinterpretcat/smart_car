from threading import Thread, Timer
from .common import Command
from utils.thread import stopThread


class LightCommand:
    def __init__(self, adc, light, callback, isDryRun=False) -> None:
        self.adc = adc
        self.light = light
        self.callback = callback
        self.isDryRun = isDryRun
        self.lightEnabled = False

    def name(self) -> Command:
        return Command.CMD_LIGHT

    def run(self, _data=None) -> None:
        if self.lightEnabled:
            return

        self.lightEnabled = True
        self.lightRun = Thread(target=self.light.run, daemon=True)
        self.lightRun.start()

        self.lightTimer = Timer(0.3, self._sendLight)
        self.lightTimer.start()

    def _sendLight(self):
        if self.lightEnabled:
            if self.isDryRun:
                adc_light1, adc_light2 = 42, 43
                print(
                    f"{self.name()}: simulating light with {adc_light1=}, {adc_light2=}")
            else:
                adc_light1, adc_light2 = self.adc.recvADC(0), self.adc.recvADC(1)

            try:
                self.callback([self.name(), '1', str(adc_light1), str(adc_light2)])
            except Exception as e:
                self.lightEnabled = False
                print(f"{self.name()}: exception: {e}")
                return

            self.lightTimer = Timer(0.17, self._sendLight)
            self.lightTimer.start()

    def stop(self):
        self.lightEnabled = False
        try:
            self.light.runnable = False
            if hasattr(self, 'lightRun'):
                stopThread(self.lightRun)

        except BaseException:
            pass
