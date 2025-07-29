from alert import generate_alert
import time
import random

zones = ["Main gate", "East wing", "West wing", "North Zone", "South Zone", "Middle Ground", "South East Area", "Corner to the North", "Middle of East wing", "Food Court", "At the Stage", "Exit 1", "Exit 2"]

for zone in zones:
    generate_alert(f"Critical Crowd density alert at the {zone}")
    time.sleep(3)