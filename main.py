import RPi.GPIO as GPIO
import time

from pir_sensor import PIRSensor
from crash_sensor import CrashSensor
from buzzer import Buzzer
from camera_record import CameraRecorder
from discord_alerts import DiscordAlert

GPIO.setmode(GPIO.BCM)

PIR_PIN = 23
CRASH_PIN = 17
BUZZER_PIN = 18

pir = PIRSensor(PIR_PIN)
crash = CrashSensor(CRASH_PIN)
buzzer = Buzzer(BUZZER_PIN)
camera = CameraRecorder()
discord = DiscordAlert("YOUR_WEBHOOK_URL")

print("Security System Online...")

try:
    while True:

        # PIR motion detection
        if pir.motion_detected():
            print("Motion detected!")

            pir.log_alert()  # INSERT INTO Alerts
            discord.send("🚨 Motion Detected!")
            buzzer.slow_alert()

            clip = camera.record_clip()  # INSERT INTO Clips
            if clip:
                print("Clip saved:", clip)

            time.sleep(2)

        # Crash sensor tampering
        if crash.pressed():
            print("TAMPER ALERT!")

            crash.log_alert()  # INSERT INTO Alerts
            discord.send("⚠️ CRITICAL: System Tampering Detected!")
            buzzer.fast_alert()

            time.sleep(2)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("System Shutting Down...")

finally:
    GPIO.cleanup()
