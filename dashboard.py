import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time
import cv2


if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL':'https://netragaurd-default-rtdb.firebaseio.com/'
    })

st.set_page_config(page_title="NetraGaurd Alert Dashboard", layout="wide")
st.title("NetraGaurd Live Alert Dashboard")
st.markdown("Real-time monitering of the crowd density using YOLO + Firebase")

refresh_interval = 5
placeholder = st.empty()

def fetch_alerts():
    ref = db.reference("alerts")
    data = ref.get()
    if not data:
        return []
    
    alert_list = [{"timestamp":k, "description":v["description"]} for k,v in data.items()]
    alert_list.sort(key=lambda x:x["timestamp"], reverse=True)
    return alert_list

while True:
    with placeholder.container():
        alerts = fetch_alerts()
        if alerts:
            for alert in alerts:
                st.error(f"{alert['timestamp']} - {alert['description']}")
        else:
            st.info("No alerts at the moment. All zones are safe")

    time.sleep(refresh_interval)