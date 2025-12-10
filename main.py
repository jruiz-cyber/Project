import time
import datetime
import os
import subprocess
from threading import Thread
import requests

from gpiozero import MotionSensor, Button, Buzzer

from db import get_alerts_connection
from db_camera import get_camera_connection


# =========================================================
# Discord Notification
# =========================================================
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1441469572329898106/tX97dIsNnIEUzOe9mkj_B5hHNB4TtYh9RvOucZuAv61U536zDQG6fK26ZkcjxveP2cVU"

def send_discord(message):
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    print(f"[DISCORD] {message}")


# =========================================================
# Pin Assignments
# =========================================================
PIR_PIN = 23
CRASH_PIN = 27
BUZZER_PIN = 18
FOLDER = "/home/jruiz/Video_and_Photo_Recording"
os.makedirs(FOLDER, exist_ok=True)


# =========================================================
# Initialize Sensors & Buzzer
# =========================================================
pir = MotionSensor(PIR_PIN)
crash = Button(CRASH_PIN, pull_up=True)
buzzer = Buzzer(BUZZER_PIN)


# =========================================================
# Database Insert (Alerts Table)
# =========================================================
def upload_alert(alert_type):
    conn = get_alerts_connection()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO Alerts (alert_type, alert_time) VALUES (%s, %s)",
        (alert_type, timestamp)
    )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"[DB] Stored alert → {alert_type} at {timestamp}")


# =========================================================
# Insert Media (Camera Table)
# =========================================================
def upload_media(file_path, source):
    conn = get_camera_connection()
    cursor = conn.cursor()

    # Determine media type
    media_type = "photo" if file_path.endswith(".jpg") else "video"

    # Insert ONLY into the valid columns
    cursor.execute(
        "INSERT INTO Clips (file_path, media_type) VALUES (%s, %s)",
        (file_path, media_type)
    )

    conn.commit()
    cursor.close()
    conn.close()

    print(f"[DB] Stored {media_type} → {file_path}")

# =========================================================
# Capture Still Image (Crash Sensor / Tampering)
# =========================================================
def capture_tamper_photo():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = f"{FOLDER}/photo_{timestamp}.jpg"

    print(f"[CAMERA] Capturing tampering photo → {output_path}")

    command = [
        "rpicam-still",
        "-o", output_path,
        "--width", "1280",
        "--height", "720"
    ]

    subprocess.run(command)
    upload_media(output_path, "CRASH")
    send_discord(f"📸 Tampering detected! Saved photo: {output_path}")


# =========================================================
# Record Motion Video (PIR Sensor)
# =========================================================
def record_motion_video():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = f"{FOLDER}/video_{timestamp}.mp4"

    print(f"[CAMERA] Recording motion video → {output_path}")

    command = [
        "rpicam-vid",
        "-o", output_path,
        "-t", "20000",     # 20 seconds
        "--width", "1280",
        "--height", "720"
    ]

    subprocess.run(command)
    upload_media(output_path, "PIR")
    send_discord(f"🎥 Motion detected! Saved video: {output_path}")


# =========================================================
# PIR Event Handler
# =========================================================
# Cooldown for PIR alerts so they do not fire nonstop
PIR_COOLDOWN = 5
last_pir_alert_time = 0

pir_active = False

def handle_pir():
    global last_pir_alert_time, pir_active

    while True:
        pir_state = pir.motion_detected
        current_time = time.time()

        # Motion just started here
        if pir_state and not pir_active:
            pir_active = True

            print("[PIR] Motion detected")
            buzzer.on()

            # initial alert
            upload_alert("PIR")
            send_discord("🚨PIR Motion Detected!")

            # Start recording only once instead of every loop
            Thread(target=record_motion_video, daemon=True).start()

            # interval alerts
            last_pir_alert_time = current_time

            time.sleep(2)
            buzzer.off()

        # Reduces Spam
        elif pir_state and pir_active:
            # Updates
            if current_time - last_pir_alert_time >= PIR_COOLDOWN:
                
                # Beep the buzzer for 1 second every 5 seconds
                buzzer.on()
                time.sleep(1)
                buzzer.off()

                send_discord("PIR still detecting motion...")
                last_pir_alert_time = current_time
        
        # Motion ended, reset
        elif not pir_state and pir_active:
            pir_active = False

        time.sleep(0.1)



# =========================================================
# Crash Sensor Event Handler
# =========================================================
last_crash_time = 0

def handle_crash():
    global last_crash_time
    COOLDOWN = 5  # seconds

    while True:
        if crash.is_pressed:  # PRESS = True
            now = time.time()

            # ignore duplicate triggers within cooldown
            if now - last_crash_time < COOLDOWN:
                time.sleep(0.1)
                continue

            # debounce
            time.sleep(0.05)
            if crash.is_pressed:  # still pressed
                last_crash_time = now

                print("[CRASH] Impact detected")
                buzzer.on()
                upload_alert("CRASH")
                send_discord("⚠️ Crash / Tampering Detected!")

                Thread(target=capture_tamper_photo, daemon=True).start()

                time.sleep(2)
                buzzer.off()

        time.sleep(0.1)


# =========================================================
# Main Loop
# =========================================================
if __name__ == "__main__":
    print("=== Security System Active ===")
    send_discord("🟢 Security system is now online")

    Thread(target=handle_pir, daemon=True).start()
    Thread(target=handle_crash, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        buzzer.off()
        send_discord("🔴 Security system shut down")
        print("\nSystem shutdown.")
