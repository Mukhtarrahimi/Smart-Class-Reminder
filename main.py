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
         if not self.classes:
            print("No classes scheduled yet.")
            return
            print("\n📚 Scheduled Classes:")
            for i, cls in enumerate(self.classes, start=1):
                print(f"{i}. {cls['title']} | Day: {cls['day']} | Time: {cls['hour']} | Link: {cls['link']}")

    # Search for a class by title or day
    def search_class(self):
        keyword = input("Enter keyword to search: ")
        found = [cls for cls in self.classes if keyword.lower() in cls['title'].lower() or keyword.lower() in cls['day'].lower()]
        if not found:
            print("No matching classes found.")
            return
        print("\n🔎 Found Classes:")
        for cls in found:
            print(f"{cls['title']} | Day: {cls['day']} | Time: {cls['hour']} | Link: {cls['link']}")

    # Remove a class by index
    def remove_class(self):
        self.show_classes()
        if not self.classes:
            return
        try:
            index = int(input("Enter the number of the class to remove: "))
            if 1 <= index <= len(self.classes):
                removed = self.classes.pop(index-1)
                self.save_classes()
                print(f"❌ Class '{removed['title']}' has been removed.")
            else:
                print("Invalid number.")
        except ValueError:
            print("Please enter a valid number.")