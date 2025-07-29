import cv2
from ultralytics import YOLO

class CrowdDetector:
    def __init__(self, model_path = 'yolov8n.pt', person_threshold=20):
        self.model = YOLO(model_path)
        self.person_threshold = person_threshold

    def process_frame(self, frame):
        results = self.model(frame, verbose=False)[0]
        person_count = 0

        for box in results.boxes:
            cls = int(box.cls[0])
            if cls == 0:
                person_count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1,y1), (x2,y2), (0, 255, 0), 2)
            
        status = "Critical" if person_count >= self.person_threshold else "Normal"
        cv2.putText(frame, f"People: {person_count} | Status: {status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255) if status == "Critical" else (0,255,0), 2)

        return frame, person_count, status
    
    def run(self, source=0):
        cap = cv2.VideoCapture(source)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame, count, status = self.process_frame(frame)
            cv2.imshow("Netra gaurd monitor", frame)

            if cv2.waitKey(1) & 0XFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        

