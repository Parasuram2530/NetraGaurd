import cv2
import time
from ultralytics import YOLO
from alert import generate_alert
import firebase_admin
from firebase_admin import credentials, db
import threading
from collections import defaultdict

cam_statuses = defaultdict(lambda: "Normal")
status_lock = threading.Lock()


model = YOLO("yolov8s.pt")

alert_thresholds = {
    'Cam1':300000,
    'Cam2':250000, 
    'Cam3':220000
}  
alert_cooldown = 20      
last_alert_times = {
    'Cam1':0,
    'Cam2':0, 
    'Cam3':0
}

def log_to_firebase(cam_id, crowd_level):
    ref = db.reference(f"/NetraGaurd/{cam_id}")
    ref.set({
        'timestamp':int(time.time()),
        'status':crowd_level
    })
    with status_lock:
        cam_statuses[cam_id] = crowd_level

def log_escalation_to_firebase(message):
    ref = db.reference("/NetraGaurd/Escalation")
    ref.push({
        'timestamp':int(time.time()),
        'message':message
    })

def check_escalation():
    with status_lock:
        overcrowded_cams = [cam for cam, status in cam_statuses.items() if status == "OverCrowded"]
        if len(overcrowded_cams) >= 2:
            desc = f"🚨 Multiple zones overcrowded: {', '.join(overcrowded_cams)}"
            generate_alert(desc, alert_type="Multi-Cam Escalation")
            print(f"[ESCALATION] {desc}")

def monitor_camera(cam_id, source):
    cap = cv2.VideoCapture(source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_count = 0

    print("[NetraGaurd] Live Crowd monitoring Started...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 2 != 0:
            continue  

        start_time = time.time()

        results = model.predict(source=frame, stream=False, verbose=False)[0]

        total_area = 0
        boxes = []

        for r in results.boxes:
            if int(r.cls[0]) == 0:  
                x1, y1, x2, y2 = map(int, r.xyxy[0])
                area = (x2 - x1) * (y2 - y1)
                total_area += area
                boxes.append((x1, y1, x2, y2))

        for (x1, y1, x2, y2) in boxes:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.putText(frame, f"People Detected: {len(boxes)}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        fps = 1/(time.time() - start_time)
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.imshow(f"{cam_id}", frame)


        current_time = time.time()
        threshold = alert_thresholds.get(cam_id, 300000)
        if total_area > threshold and (current_time - last_alert_times[cam_id]) > alert_cooldown:
            event_desc = "🔴 Critical crowd density detected "
            generate_alert(event_desc, cam_id)
            log_to_firebase(cam_id, "OverCrowded")
            print(f"[ALERT] {event_desc}")
            last_alert_times[cam_id] = current_time
            check_escalation()

            with status_lock:
                cam_statuses[cam_id] = "OverCrowded"
                overcrowded_cams = [c for c,s in cam_statuses.items() if s=='OverCrowded']
                if len(overcrowded_cams)>=2:
                    escalation_msg = f"Critical: {len(overcrowded_cams)} cams Overcrowded - {', '.join(overcrowded_cams)}"
                    generate_alert(escalation_msg, cam_id)
                    log_escalation_to_firebase(escalation_msg)
                    print(f"[ESCALATION] {escalation_msg}")
        else:
            log_to_firebase(cam_id, "Normal")
            with status_lock:
                cam_statuses[cam_id] = "Normal"

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    cameras = {
        "Cam1":0,
        "Cam2": 'video_files/Cam2.mp4',
        "Cam3": 'video_files/Cam3.mp4'
    }
    threads = []
    for cam_id, src in cameras.items():
        if src is not None:
            t = threading.Thread(target=monitor_camera, args= (cam_id, src))
            t.start()
            threads.append(t)
    
    for t in threads:
        t.join()
    
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()