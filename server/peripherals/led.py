import time
from rpi_ws281x import *

LED_COUNT = 8         # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


class Led:
    def __init__(self):
        # control the sending order of color data
        self.ORDER = "RGB"
        self.strip = Adafruit_NeoPixel(
            LED_COUNT,
            LED_PIN,
            LED_FREQ_HZ,
            LED_DMA,
            LED_INVERT,
            LED_BRIGHTNESS,
            LED_CHANNEL)
        self.strip.begin()
        self.modable = False


    def ledTypr(self, order, R_G_B):
        B = R_G_B & 255
        G = R_G_B >> 8 & 255
        R = R_G_B >> 16 & 255

        Led_type = ["GRB", "GBR", "RGB", "RBG", "BRG", "BGR"]
        color = [Color(G, R, B), Color(G, B, R), Color(R, G, B),
                 Color(R, B, G), Color(B, R, G), Color(B, G, R)]
        if order in Led_type:
            return color[Led_type.index(order)]

    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        color = self.ledTypr(self.ORDER, color)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def theaterChase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        color = self.ledTypr(self.ORDER, color)
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, color)
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = pos * 3
            g = 255 - pos * 3
            b = 0
        elif pos < 170:
            pos -= 85
            r = 255 - pos * 3
            g = 0
            b = pos * 3
        else:
            pos -= 170
            r = 0
            g = pos * 3
            b = 255 - pos * 3

        return self.ledTypr(self.ORDER, Color(r, g, b))

    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel(
                    (int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))

                self.strip.show()
                time.sleep(wait_ms / 1000.0)

                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    def ledIndex(self, index, R, G, B):
        color = self.ledTypr(self.ORDER, Color(R, G, B))
        for i in range(8):
            if index & 0x01 == 1:
                self.strip.setPixelColor(i, color)
                self.strip.show()
            index = index >> 1

    def ledMode(self, n):
        self.mode = n
        self.modable = True
        while self.modable:
            self.colorWipe(Color(0, 0, 0), 10)
            if self.mode == '2':
                self.colorWipe(Color(255, 0, 0))  # Red wipe
                self.colorWipe(Color(0, 255, 0))  # Green wipe
                self.colorWipe(Color(0, 0, 255))  # Blue wipe
            elif self.mode == '3':
                self.theaterChaseRainbow()
            elif self.mode == '4':
                self.rainbow()
            elif self.mode == '5':
                self.rainbowCycle()
            else:
                break
        self.colorWipe(Color(0, 0, 0), 10)
