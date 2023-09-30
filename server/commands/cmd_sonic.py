from threading import Thread, Timer
from .common import Command
from utils.thread import stopThread


class UltrasonicCommand:
    def __init__(self, ultrasonic, callback, isDryRun=False) -> None:
        self.ultrasonic = ultrasonic
        self.callback = callback
        self.isDryRun = isDryRun
        self.sonicEnabled = False

    def name(self) -> Command:
        return Command.CMD_SONIC

    def run(self, _data=None) -> None:
        if self.sonicEnabled:
            return
        self.sonicEnabled = True
        self.ultrasonicRun = Thread(target=self.ultrasonic.run, daemon=True)
        self.ultrasonicRun.start()

        self.ultrasonicTimer = Timer(0.5, self._sendUltrasonic)
        self.ultrasonicTimer.start()

    def _sendUltrasonic(self):
        if self.sonicEnabled:
            if self.isDryRun:
                adc_ultrasonic = 1
                print(f"{self.name()}: simulating {adc_ultrasonic=}")
            else:
                adc_ultrasonic = self.ultrasonic.getDistance()

            try:
                self.callback([self.name(), '3', str(adc_ultrasonic)])
            except Exception as e:
                self.sonicEnabled = False
                print(f"{self.name()}: exception: {e}")
                return

            self.ultrasonicTimer = Timer(0.23, self._sendUltrasonic)
            self.ultrasonicTimer.start()

    def stop(self):
        self.sonicEnabled = False
        try:
            self.ultrasonic.runnable = False
            if hasattr(self, 'ultrasonicRun'):
                stopThread(self.ultrasonicRun)
        except:
            pass
