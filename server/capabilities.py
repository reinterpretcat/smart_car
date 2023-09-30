from utils.fake import Fake
from commands import *

try:
    from peripherals import *
    isDryRun = False
except ImportError as e:
    print(
        f"\033[93mCannot import peripherals: \"{e}\". Most likely you're missing some dependencies. Switching to dry run mode\033[0m")
    isDryRun = True


class Peripherals():
    """Keeps track of availave hardware abstractions"""
    def __init__(self) -> None:
        self.adc = Adc() if not isDryRun else Fake('Adc')
        self.gpio = GeneralPurposeIO if not isDryRun else Fake('GeneralPurposeIO')
        self.buzzer = Buzzer(self.gpio) if not isDryRun else Fake('Buzzer')
        self.camera = Camera() if not isDryRun else Fake('Camera')
        self.pca = PCA9685(address=0x40, debug=True) if not isDryRun else Fake('PCA9685')
        self.motor = Motor(self.adc, self.pca) if not isDryRun else Fake('Motor')
        self.led = Led() if not isDryRun else Fake('Led')
        self.infrared = InfraredTracking(self.motor, self.gpio) if not isDryRun else Fake('InfraredTracking')
        self.light = Light(self.adc, self.motor) if not isDryRun else Fake('Light')
        self.servo = Servo(self.pca) if not isDryRun else Fake('Servo')
        self.ultrasonic = Ultrasonic(self.motor, self.servo, self.gpio) if not isDryRun else Fake('Ultrasonic')


class Catalog():
    """Keeps track of available commands"""
    def __init__(self, peripherals, callback) -> None:
        # create commands
        buzzerCmd = BuzzerCommand(peripherals.buzzer, isDryRun)
        carRotateCmd = CarRotateCommand(peripherals.motor, isDryRun)
        ledModCmd = LedModCommand(peripherals.led, isDryRun)
        ledCmd = LedCommand(peripherals.led, isDryRun)
        lightCmd = LightCommand(peripherals.adc, peripherals.light, callback, isDryRun)
        lineTrackingCmd = LineTrackingCommand(peripherals.infrared, peripherals.gpio, callback, isDryRun)
        mmotorCmd = MMotorComand(peripherals.motor, isDryRun)
        motorCmd = MotorComand(peripherals.motor, isDryRun)
        powerCmd = PowerCommand(peripherals.adc, callback, isDryRun)
        servoCmd = ServoCommand(peripherals.servo, isDryRun)
        ultrasonicCmd = UltrasonicCommand(peripherals.ultrasonic, callback, isDryRun)
        modeCmd = ModeCommand(callback, peripherals.motor, peripherals.servo, lightCmd, ultrasonicCmd, lineTrackingCmd, isDryRun)

        # create dictionary of commands
        allCommands = [
            buzzerCmd,
            carRotateCmd,
            ledModCmd,
            ledCmd,
            lightCmd,
            lineTrackingCmd,
            mmotorCmd,
            motorCmd,
            powerCmd,
            servoCmd,
            ultrasonicCmd,
            modeCmd]

        self.allCommands = dict([(cmd.name(), cmd) for cmd in allCommands])

    def getAllCommands(self):
        return self.allCommands

# Provides way to use certain capabilities of hardware.


class Capabilities():
    def __init__(self, callback) -> None:
        self.peripherals = Peripherals()
        self.catalog = Catalog(self.peripherals, callback)

    def gePeripherals(self) -> Peripherals:
        return self.peripherals

    def getCatalog(self) -> Catalog:
        return self.catalog
