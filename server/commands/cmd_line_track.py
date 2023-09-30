from threading import Thread, Timer
from .common import Command
from utils.thread import stopThread


class LineTrackingCommand:
    def __init__(self, infrared, gpio, callback, isDryRun=False) -> None:
        self.infrared = infrared
        self.gpio = gpio
        self.callback = callback
        self.isDryRun = isDryRun

    def name(self) -> Command:
        return Command.CMD_LINE_TRACK

    def run(self, _data=None):
        if self.lineEnabled:
            return

        self.infraredRun = Thread(target=self.infrared.run, daemon=True)
        self.infraredRun.start()

        self.lineEnabled = True
        self.lineTimer = Timer(0.4, self._sendLine)
        self.lineTimer.start()

    def _sendLine(self):
        if self.lineEnabled:
            if self.isDryRun:
                line1, line2, line3 = 14, 1, 23
                print(f"{self.name()}: simulating with {line1=}, {line2=}, {line3=}")
            else:
                line1 = 1 if self.gpio.input(14) else 0
                line2 = 1 if self.gpio.input(15) else 0
                line3 = 1 if self.gpio.input(23) else 0
            try:
                self.callback([self.name(), '2', str(line1), str(line2), str(line3)])
            except Exception as e:
                self.lineEnabled = False
                print(f"{self.name()}: exception: {e}")
                return

            self.lineTimer = Timer(0.20, self._sendLine)
            self.lineTimer.start()

    def stop(self):
        self.lineEnabled = False
        try:
            self.infrared.runnable = False
            stopThread(self.infraredRun)
        except BaseException:
            pass
