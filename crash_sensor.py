import RPi.GPIO as GPIO

class CrashSensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def pressed(self):
        return GPIO.input(self.pin) == GPIO.LOW
