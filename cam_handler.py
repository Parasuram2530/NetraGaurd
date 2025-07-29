import threading
import cv2
from face_searcher import search_for_person
from crowd_monitor import monitor_camera

def handle_camera(cam_id, cam_url, known_encoding):
    def crowd_task():
        monitor_camera(cam_id, cam_url)

    def face_search_task():
        cap = cv2.VideoCapture(cam_url)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            found = search_for_person(cam_id, frame, known_encoding)
            if found:
                print(f"[FACE MATCH] 🎯 Person found on {cam_id}")
                break
        cap.release()

    crowd_thread = threading.Thread(target=crowd_task)
    face_thread = threading.Thread(target=face_search_task)

    crowd_thread.start()
    face_thread.start()

    return [crowd_thread, face_thread]
