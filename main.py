import threading
import time
import face_recognition
from cam_handler import handle_camera

img = face_recognition.load_image_file('missing_person.jpg')
known_encoding = face_recognition.face_encodings(img)[0]

cameras = {
    "Cam1": 0,
    "Cam2": "video_files/Cam2.mp4",
    "Cam3": "video_files/Cam3.mp4"
}

print("[NetraGaurd] Starting Multi Camera Monitoring + face search....")

all_threads = []

for cam_id, cam_url in cameras.items():
    threads = handle_camera(cam_id, cam_url, known_encoding)
    all_threads.extend(threads)

try:
    for t in all_threads:
        t.join()
except KeyboardInterrupt:
    print("NetraGaurd Stopped.")
