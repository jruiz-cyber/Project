import subprocess

class CameraRecorder:
    def record_clip(self, filename="motion_clip.h264", duration=5):
        try:
            subprocess.run([
                "libcamera-vid",
                "-t", str(duration * 1000),
                "-o", filename
            ])
        except Exception as e:
            print("Camera recording failed:", e)
