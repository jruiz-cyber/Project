import RPi.GPIO as GPIO
from datetime import datetime
from db import get_alerts_connection

class PIRSensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def motion_detected(self):
        return GPIO.input(self.pin) == GPIO.HIGH

    def log_alert(self):
        conn = get_alerts_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO Alerts (type, alert_time) VALUES (%s, %s)"
        val = ("PIR", datetime.now())

        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
