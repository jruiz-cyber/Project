import subprocess
from datetime import datetime
from db import get_camera_connection

class CameraRecorder:
    def record_clip(self):
        filename = f"/home/pi/security_clips/clip_{datetime.now().strftime('%Y%m%d_%H%M%S')}.h264"

        try:
            subprocess.run([
                "libcamera-vid",
                "-t", "5000",
                "-o", filename
            ])

            # Log into Camera DB
            conn = get_camera_connection()
            cursor = conn.cursor()

            sql = "INSERT INTO Clips (file_path, clip_time) VALUES (%s, %s)"
            val = (filename, datetime.now())

            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()

            return filename

        except Exception as e:
            print("Camera Error:", e)
            return None
