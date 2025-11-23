import subprocess
import datetime
import os

# Folder where videos will be saved
folder = "/home/jruiz/Video_and_Photo_Recording"
os.makedirs(folder, exist_ok=True)

# Create timestamp for filename
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Build output path
output_path = f"{folder}/video_{timestamp}.mp4"

# rpicam-vid command
command = [
    "rpicam-vid",
    "-o", output_path,
    "-t", "20000",    # 20 seconds
    "--width", "1280",
    "--height", "720"
]

# Record video
print(f"Recording motion event video at {timestamp}...")
subprocess.run(command)

print(f"Saved video: {output_path}")
