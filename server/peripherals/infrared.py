
class InfraredTracking:
    def __init__(self, motor, gpio):
        self.runnable = False
        self.motor = motor
        self.gpio = gpio
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setup(self.IR01, self.gpio.IN)
        self.gpio.setup(self.IR02, self.gpio.IN)
        self.gpio.setup(self.IR03, self.gpio.IN)

    def run(self):
        self.runnable = True
        while self.runnable:
            self.LMR = 0x00
            if self.gpio.input(self.IR01):
                self.LMR = (self.LMR | 4)
            if self.gpio.input(self.IR02):
                self.LMR = (self.LMR | 2)
            if self.gpio.input(self.IR03):
                self.LMR = (self.LMR | 1)
            if self.LMR == 2:
                self.motor.setMotorModel(800, 800, 800, 800)
            elif self.LMR == 4:
                self.motor.setMotorModel(-1500, -1500, 2500, 2500)
            elif self.LMR == 6:
                self.motor.setMotorModel(-2000, -2000, 4000, 4000)
            elif self.LMR == 1:
                self.motor.setMotorModel(2500, 2500, -1500, -1500)
            elif self.LMR == 3:
                self.motor.setMotorModel(4000, 4000, -2000, -2000)
            elif self.LMR == 7:
                self.motor.setMotorModel(0, 0, 0, 0)

        self.motor.setMotorModel(0, 0, 0, 0)
