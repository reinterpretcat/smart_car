from threading import Thread
import time
from .common import Command
from utils.thread import stopThread


class LedModCommand():
    def __init__(self, led, isDryRun=True) -> None:
        self.led = led
        self.isDryRun = isDryRun

    def name(self) -> Command:
        return Command.CMD_LED_MOD

    def run(self, data) -> None:
        self.stop()
        ledMode = data[0]

        if self.isDryRun:
            print(f"{self.name()}: {ledMode=}")
            return

        self.stop()

        if ledMode == '1':
            self.led.ledMode(ledMode)
            time.sleep(0.1)
            self.led.ledMode(ledMode)
        else:
            time.sleep(0.1)
            self.updater = Thread(target=self.led.ledMode, args=(ledMode,))
            self.updater.start()

    def stop(self):
        try:
            self.led.modable = False
            if hasattr(self, 'updater'):
                stopThread(self.updater)
        except Exception as e:
            print(e)
            pass
