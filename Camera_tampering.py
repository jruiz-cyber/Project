import subprocess
import datetime
import os

# Folder where photos will be saved
folder = "/home/jruiz/Project/Camera"
os.makedirs(folder, exist_ok=True)

# Create timestamp for filename
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Build output path
output_path = f"{folder}/photo_{timestamp}.jpg"

# rpicam-still command
command = [
    "rpicam-still",
    "-o", output_path,
    "--width", "1280",
    "--height", "720"
]

# Capture photo
print("Capturing tampering photo...")
subprocess.run(command)

print(f"Saved photo: {output_path}")
