import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trig, echo):
        self.trig = trig
        self.echo = echo

        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def distance(self):
        GPIO.output(self.trig, False)
        time.sleep(0.0002)

        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()

        while GPIO.input(self.echo) == 1:
            pulse_end = time.time()

        duration = pulse_end - pulse_start
        dist = duration * 17150
        return dist
