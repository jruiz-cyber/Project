import RPi.GPIO as GPIO
import time

class Buzzer:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def beep(self, duration=0.1):
        GPIO.output(self.pin, True)
        time.sleep(duration)
        GPIO.output(self.pin, False)

    def slow_alert(self):
        """Beep every 3 seconds"""
        self.beep(0.15)
        time.sleep(3)

    def fast_alert(self):
        """Rapid tamper alarm"""
        for _ in range(10):
            self.beep(0.08)
            time.sleep(0.1)
