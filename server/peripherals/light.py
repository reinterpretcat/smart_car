class Light:
    def __init__(self, adc, motor) -> None:
        self.adc = adc
        self.motor = motor
        self.runnable = False

    def run(self):
        self.runnable = True
        while self.runnable:
            L = self.adc.recvADC(0)
            R = self.adc.recvADC(1)
            if L < 2.99 and R < 2.99:
                self.motor.setMotorModel(600, 600, 600, 600)
            elif abs(L - R) < 0.15:
                self.motor.setMotorModel(0, 0, 0, 0)

            elif L > 3 or R > 3:
                if L > R:
                    self.motor.setMotorModel(-1200, -1200, 1400, 1400)

                elif R > L:
                    self.motor.setMotorModel(1400, 1400, -1200, -1200)
        self.motor.setMotorModel(0, 0, 0, 0)
