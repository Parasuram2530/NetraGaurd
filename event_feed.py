import time
from alert import generate_alert

event_stream = [
    "Normal crowd at main gate",
    "Minor congestion near the food stalls",
    "Critical overcrowding at south wing",
    "VIP movement detected near south section",
    "Critical incident at north exit – medical emergency",
    "All clear at west gate"
]

def stream_events():
    for event in event_stream:
        print(f"New event detected: {event}")
        generate_alert(event)
        time.sleep(5)

if __name__ == "__main__":
    print("Starting Netra gaurd Event feed simulation...\n")
    stream_events()