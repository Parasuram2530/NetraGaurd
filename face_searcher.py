import face_recognition
import cv2
from firebase_alert import send_alert
from alert import speak_alert

def search_for_person(cam_id, frame, known_encoding):
    # rgb_frame = frame[:, :, ::-1]  
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    print(f"[{cam_id}] Detected {len(face_encodings)} face(s)")

    for encoding in face_encodings:
        match = face_recognition.compare_faces([known_encoding], encoding, tolerance=0.45)
        if match[0]:
            speak_alert(f"🎯 Alert! Person matched on {cam_id}")
            send_alert(cam_id, "Missing person Found on camera {}".format(cam_id))
            return True
    return False


