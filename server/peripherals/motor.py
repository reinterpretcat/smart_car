import time
import math


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class Motor:
    def __init__(self, adc, pca):
        self.adc = adc
        self.pca = pca
        self.pca.setPWMFreq(50)
        # Depend on your own car,If you want to get the best out of the
        # rotation mode, change the value by experimenting.
        self.time_proportion = 3
        self.rotatable = False


    def dutyRange(self, duty1, duty2, duty3, duty4):
        duty1 = clamp(duty1, -4095, 4095)
        duty2 = clamp(duty2, -4095, 4095)
        duty3 = clamp(duty3, -4095, 4095)
        duty4 = clamp(duty4, -4095, 4095)

        return duty1, duty2, duty3, duty4

    def leftUpperWheel(self, duty):
        if duty > 0:
            self.pca.setMotorPwm(0, 0)
            self.pca.setMotorPwm(1, duty)
        elif duty < 0:
            self.pca.setMotorPwm(1, 0)
            self.pca.setMotorPwm(0, abs(duty))
        else:
            self.pca.setMotorPwm(0, 4095)
            self.pca.setMotorPwm(1, 4095)

    def leftLowerWheel(self, duty):
        if duty > 0:
            self.pca.setMotorPwm(3, 0)
            self.pca.setMotorPwm(2, duty)
        elif duty < 0:
            self.pca.setMotorPwm(2, 0)
            self.pca.setMotorPwm(3, abs(duty))
        else:
            self.pca.setMotorPwm(2, 4095)
            self.pca.setMotorPwm(3, 4095)

    def rightUpperWheel(self, duty):
        if duty > 0:
            self.pca.setMotorPwm(6, 0)
            self.pca.setMotorPwm(7, duty)
        elif duty < 0:
            self.pca.setMotorPwm(7, 0)
            self.pca.setMotorPwm(6, abs(duty))
        else:
            self.pca.setMotorPwm(6, 4095)
            self.pca.setMotorPwm(7, 4095)

    def rightLowerWheel(self, duty):
        if duty > 0:
            self.pca.setMotorPwm(4, 0)
            self.pca.setMotorPwm(5, duty)
        elif duty < 0:
            self.pca.setMotorPwm(5, 0)
            self.pca.setMotorPwm(4, abs(duty))
        else:
            self.pca.setMotorPwm(4, 4095)
            self.pca.setMotorPwm(5, 4095)

    def setMotorModel(self, duty1, duty2, duty3, duty4):
        duty1, duty2, duty3, duty4 = self.dutyRange(duty1, duty2, duty3, duty4)
        self.leftUpperWheel(duty1)
        self.leftLowerWheel(duty2)
        self.rightUpperWheel(duty3)
        self.rightLowerWheel(duty4)

    def rotate(self, n):
        self.rotatable = True
        angle = n
        bat_compensate = 7.5 / (self.adc.recvADC(2) * 3)
        while self.rotatable:
            W = 2000

            VY = int(2000 * math.cos(math.radians(angle)))
            VX = -int(2000 * math.sin(math.radians(angle)))

            FR = VY - VX + W
            FL = VY + VX - W
            BL = VY - VX - W
            BR = VY + VX + W

            self.pca.setMotorModel(FL, BL, FR, BR)

            print("rotating")
            time.sleep(5 * self.time_proportion * bat_compensate / 1000)
            angle -= 5
        self.motor.setMotorModel(0, 0, 0, 0)
