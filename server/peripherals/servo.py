class Servo:
    def __init__(self, pca):
        self.pwmServo = pca
        self.pwmServo.setPWMFreq(50)
        self.pwmServo.setServoPulse(8, 1500)
        self.pwmServo.setServoPulse(9, 1500)

    def setServoPwm(self, channel, angle, error=10):
        angle = int(angle)
        value = int((angle + error) / 0.09)

        if channel == '0':
            self.pwmServo.setServoPulse(8, 2500 - value)
        elif channel == '1':
            self.pwmServo.setServoPulse(9, 500 + value)
        elif channel == '2':
            self.pwmServo.setServoPulse(10, 500 + value)
        elif channel == '3':
            self.pwmServo.setServoPulse(11, 500 + value)
        elif channel == '4':
            self.pwmServo.setServoPulse(12, 500 + value)
        elif channel == '5':
            self.pwmServo.setServoPulse(13, 500 + value)
        elif channel == '6':
            self.pwmServo.setServoPulse(14, 500 + value)
        elif channel == '7':
            self.pwmServo.setServoPulse(15, 500 + value)
