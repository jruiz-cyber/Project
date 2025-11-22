import RPi.GPIO as GPIO
import time

from ultrasonic import UltrasonicSensor
from crash_sensor import CrashSensor
from buzzer import Buzzer
from camera_record import CameraRecorder
from discord_alerts import DiscordAlert

GPIO.setmode(GPIO.BCM)

# ==== PIN DEFINITIONS ====
ULTRA_TRIG = 23
ULTRA_ECHO = 24
BUZZER_PIN = 18
CRASH_PIN = 17

# ==== INITIALIZE CLASSES ====
ultra = UltrasonicSensor(ULTRA_TRIG, ULTRA_ECHO)
crash = CrashSensor(CRASH_PIN)
buzzer = Buzzer(BUZZER_PIN)
camera = CameraRecorder()
discord = DiscordAlert("https://discord.com/api/webhooks/1441469572329898106/tX97dIsNnIEUzOe9mkj_B5hHNB4TtYh9RvOucZuAv61U536zDQG6fK26ZkcjxveP2cVU")

print("Security System Active...\n")

try:
    while True:
        dist = ultra.distance()

        # ----- ULTRASONIC DETECTS MOTION -----
        if dist < 50:  # threshold for someone walking through a door
            print("Motion detected:", dist, "cm")
            discord.send("🚨 Motion Detected at the Doorway!")
            camera.record_clip("motion.h264")
            buzzer.slow_alert()

        # ----- CRASH SENSOR TAMPERING -----
        if crash.pressed():
            print("TAMPER ALERT: Crash sensor activated!")
            discord.send("⚠️ CRITICAL: Someone is tampering with the security system!")
            buzzer.fast_alert()

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Shutting down system...")

finally:
    GPIO.cleanup()
