from gpiozero import MotionSensor
from datetime import datetime
import time

from db import get_alerts_connection


class PIRSensor:
    # Initializes the PIR sensor using the GPIO pin.
    # gpiozero handles Pi 5 compatibility internally.
    def __init__(self, pin):
        self.sensor = MotionSensor(pin)

    # Returns True if motion is detected.
    def motion_detected(self):
        return self.sensor.motion_detected

    # Inserts a motion alert into the alerts database.
    def upload_alert(self):
        conn = get_alerts_connection()
        cursor = conn.cursor()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO Alerts (sensor_type, alert_time) VALUES (%s, %s)",
            ("PIR", timestamp)
        )

        conn.commit()
        cursor.close()
        conn.close()

        print(f"[DB] PIR alert stored at {timestamp}")
