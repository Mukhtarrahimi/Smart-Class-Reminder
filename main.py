import json
import os
import datetime
import time

FILE_NAME = "classes.json"


class SmartClassReminder:
    def __init__(self):
        self.classes = []
        self.load_classes()

         # Add a new class/session
        def add_class(self):
            title = input("Class Title: ")
            day = input("Day (e.g., Monday): ")
            hour = input("Start Time (24h format, e.g., 14:30): ")
            link = input("Online Session Link: ")
            self.classes.append({
                "title": title,
                "day": day.capitalize(),
                "hour": hour,
                "link": link
            })
            self.save_classes()
            print(f"✅ Class '{title}' has been successfully added!")
        
        # Display all classes
    def show_classes(self):
        pass