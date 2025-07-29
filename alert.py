import datetime
import firebase_admin
from firebase_admin import credentials, db
import pyttsx3
import threading
import os
from dotenv import load_dotenv
load_dotenv()

try:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.getenv('FIREBASE_DB_URL') 
    })
except Exception as e:
    print(f"[Firebase] Already initialized or failed: {e}")

_engine = pyttsx3.init()
_lock = threading.Lock()

def speak_alert(message):
    def run_speech():
        with _lock:
            _engine.say(message)
            _engine.runAndWait()
    threading.Thread(target=run_speech, daemon=True).start()

def generate_alert(description, cam_id="", alert_type = "High Crowd"):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_message = f"[{timestamp}] [{cam_id}] {description}" if cam_id else f"[{timestamp}] {description}"
    print(full_message)
    speak_alert(f"Alert! {cam_id} is Over Crowded. Please take action.")

    log_data = {
        "description": description,
        "type": "High Crowd",
        "timestamp": timestamp,
    }

    print(f"[{timestamp}] ALERT: {description}")

    with open("alerts_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {description}\n")

    try:
        ref = db.reference("alerts")
        ref.push(log_data)
    except Exception as e:
        print(f"[Firebase Error] Could not send to Firebase: {e}")
