from enum import Enum
from .common import Command


class Mode(Enum):
    MANUAL = 1,
    LIGHT = 2,
    SONIC = 3,
    LINE_TRACK = 4

    def __str__(self):
        return self.name


class ModeCommand:
    def __init__(self, callback, motor, servo, lightCmd, utlrasonicCmd, lineTrackingCmd, isDryRun=True) -> None:
        self.mode = Mode.MANUAL
        self.callback = callback
        self.motor = motor
        self.servo = servo

        self.lightCmd = lightCmd
        self.utlrasonicCmd = utlrasonicCmd
        self.lineTrackingCmd = lineTrackingCmd

        self.isDryRun = isDryRun

        # NOTE very strange logic, but this is just how it was defined..
        self.options = {"0": Mode.MANUAL, "one": Mode.MANUAL, "1": Mode.MANUAL,
                        "two": Mode.LIGHT, "3": Mode.LIGHT,
                        "three": Mode.SONIC, "4": Mode.SONIC,
                        "four": Mode.LINE_TRACK, "2": Mode.LINE_TRACK}
        self.isDryRun = isDryRun

    def name(self) -> Command:
        return Command.CMD_MODE

    def run(self, data) -> None:
        if data[0] in self.options:
            newMode = self.options[data[0]]
        else:
            print(f"{self.name()} unknown mode: '{data[0]}'")
            return

        if newMode == self.mode:
            print('same mode as before, exit')
            return

        print(f"changing from {self.mode} to {newMode}")

        print('stopping the car just in case..')
        # first cleanup all potentially running commands
        self.lightCmd.stop()
        self.utlrasonicCmd.stop()
        self.lineTrackingCmd.stop()

        self.motor.setMotorModel(0, 0, 0, 0)
        self.servo.setServoPwm('0', 90)
        self.servo.setServoPwm('1', 90)

        # as original server does
        self.callback([self.name(), 1, 0, 0])
        self.callback([self.name(), 3, 0])
        self.callback([self.name(), 2, '000'])

        # run actual command
        if newMode == Mode.LIGHT:
            self.lightCmd.run()
        elif newMode == Mode.SONIC:
            self.utlrasonicCmd.run()
        elif newMode == Mode.LINE_TRACK:
            self.lineTrackingCmd.run()

        self.mode = newMode
