import firebase_admin
from firebase_admin import credentials,db

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL':'https://netragaurd-default-rtdb.firebaseio.com/'
    })

def send_alert(camera_id, message):
    ref = db.reference(f"alerts/camera_{camera_id}")
    ref.push({'message':message})
    print(f"[Firebase] 🚨 Alert from Camera {camera_id}: {message}")