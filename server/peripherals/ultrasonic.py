import time

class Ultrasonic:
    def __init__(self, motor, servo, gpio):
        self.runnable = False
        self.motor = motor
        self.servo = servo
        self.gpio = gpio
        self.gpio.setwarnings(False)
        self.trigger_pin = 27
        self.echo_pin = 22
        # define the maximum measuring distance, unit: cm
        self.MAX_DISTANCE = 300
        # calculate timeout according to the maximum measuring distance
        self.timeOut = self.MAX_DISTANCE * 60
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setup(self.trigger_pin, self.gpio.OUT)
        self.gpio.setup(self.echo_pin, self.gpio.IN)

    def pulseIn(self, pin, level, timeOut):  # obtain pulse time of a pin under timeOut
        t0 = time.time()
        while(self.gpio.input(pin) != level):
            if((time.time() - t0) > timeOut * 0.000001):
                return 0
        t0 = time.time()
        while(self.gpio.input(pin) == level):
            if((time.time() - t0) > timeOut * 0.000001):
                return 0
        pulseTime = (time.time() - t0) * 1000000
        return pulseTime

    # get the measurement results of ultrasonic module,with unit: cm
    def getDistance(self):
        distance_cm = [0, 0, 0, 0, 0]
        for i in range(5):
            # make trigger_pin output 10us HIGH level
            self.gpio.output(self.trigger_pin, self.gpio.HIGH)
            time.sleep(0.00001)     # 10us
            # make trigger_pin output LOW level
            self.gpio.output(self.trigger_pin, self.gpio.LOW)
            # read plus time of echo_pin
            pingTime = self.pulseIn(self.echo_pin, self.gpio.HIGH, self.timeOut)
            # calculate distance with sound speed 340m/s
            distance_cm[i] = pingTime * 340.0 / 2.0 / 10000.0
        distance_cm = sorted(distance_cm)
        return int(distance_cm[2])

    def runMotor(self, L, M, R):
        if (L < 30 and M < 30 and R < 30) or M < 30:
            self.motor.setMotorModel(-1450, -1450, -1450, -1450)
            time.sleep(0.1)
            if L < R:
                self.motor.setMotorModel(1450, 1450, -1450, -1450)
            else:
                self.motor.setMotorModel(-1450, -1450, 1450, 1450)
        elif L < 30 and M < 30:
            self.motor.setMotorModel(1500, 1500, -1500, -1500)
        elif R < 30 and M < 30:
            self.motor.setMotorModel(-1500, -1500, 1500, 1500)
        elif L < 20:
            self.motor.setMotorModel(2000, 2000, -500, -500)
            if L < 10:
                self.motor.setMotorModel(1500, 1500, -1000, -1000)
        elif R < 20:
            self.motor.setMotorModel(-500, -500, 2000, 2000)
            if R < 10:
                self.motor.setMotorModel(-1500, -1500, 1500, 1500)
        else:
            self.motor.setMotorModel(600, 600, 600, 600)

    def run(self):
        self.runnable = True
        for i in range(30, 151, 60):
            self.servo.setServoPwm('0', i)
            time.sleep(0.2)
            if i == 30:
                L = self.getDistance()
            elif i == 90:
                M = self.getDistance()
            else:
                R = self.getDistance()

        while self.runnable:
            for i in range(90, 30, -60):
                self.servo.setServoPwm('0', i)
                time.sleep(0.2)
                if i == 30:
                    L = self.getDistance()
                elif i == 90:
                    M = self.getDistance()
                else:
                    R = self.getDistance()
                self.runMotor(L, M, R)

            for i in range(30, 151, 60):
                self.servo.setServoPwm('0', i)
                time.sleep(0.2)
                if i == 30:
                    L = self.getDistance()
                elif i == 90:
                    M = self.getDistance()
                else:
                    R = self.getDistance()
                self.runMotor(L, M, R)

        self.motor.setMotorModel(0, 0, 0, 0)
