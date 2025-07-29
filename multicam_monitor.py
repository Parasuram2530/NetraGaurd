import cv2
import json
import threading
from utils.yolo_detector import detect_people

with open("camera_config.json") as f:
    config = json.load(f)

def monitor_camera(cam_id, cam_url):
    cap = cv2.VideoCapture(int(cam_url) if  cam_url.isdigit() else cam_url)

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue


        frame, count = detect_people(frame)
        cv2.putText(frame, f"[{cam_id}] Crowd: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv2.imshow(f"{cam_id}", frame)

        if cv2.waitKey(1) & 0XFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

threads = []
for cam in config['cameras']:
    t = threading.Thread(target=monitor_camera, args=(cam['id'], cam['url']))
    t.start()
    threads.append(t)

for t in threads:
    t.join()