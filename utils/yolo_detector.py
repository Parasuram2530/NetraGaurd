from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

def detect_people(frame):
    results = model(frame, verbose=False)[0]
    person_count = 0
    for box in results.boxes:
        cls = int(box.cls[0])
        if model.names[cls] == "person":
            person_count += 1
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0),)
            cv2.putText(frame, 'person', (xyxy[0], xyxy[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    return frame, person_count
