BUZZER_PIN = 17


class Buzzer:
    def __init__(self, gpio) -> None:
        self.gpio = gpio
        self.gpio.setwarnings(False)
        self.gpio.setmode(gpio.BCM)
        self.gpio.setup(BUZZER_PIN, gpio.OUT)

    def run(self, flag):
        self.gpio.output(BUZZER_PIN, flag)

    def __del__(self):
        'Make sure the sound goes off once a program terminates'
        self.gpio.output(BUZZER_PIN, False)
