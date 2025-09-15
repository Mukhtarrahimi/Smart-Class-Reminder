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
        print(f"Class '{title}' has been successfully added!")

    # Display all classes
    def show_classes(self):
        if not self.classes:
            print("No classes scheduled yet.")
            return
        print("\nScheduled Classes:")
        for i, cls in enumerate(self.classes, start=1):
            print(f"{i}. {cls['title']} | Day: {cls['day']} | Time: {cls['hour']} | Link: {cls['link']}")

    # Search for a class by title or day
    def search_class(self):
        keyword = input("Enter keyword to search: ")
        found = [cls for cls in self.classes if keyword.lower() in cls['title'].lower() or keyword.lower() in cls['day'].lower()]
        if not found:
            print("No matching classes found.")
            return
        print("\nFound Classes:")
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
                print(f"Class '{removed['title']}' has been removed.")
            else:
                print("Invalid number.")
        except ValueError:
            print("Please enter a valid number.")

    # Save classes to file
    def save_classes(self):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(self.classes, f, ensure_ascii=False, indent=4)

    # Load classes from file
    def load_classes(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                self.classes = json.load(f)

    # Reminder loop to notify classes on time
    def reminder_loop(self):
        print("Reminder loop is running. Press Ctrl+C to stop.")
        try:
            while True:
                now = datetime.datetime.now()
                current_day = now.strftime("%A")
                current_time = now.strftime("%H:%M")
                for cls in self.classes:
                    if cls['day'] == current_day and cls['hour'] == current_time:
                        print(f"\nReminder: Class '{cls['title']}' is starting now! Link: {cls['link']}")
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\nReminder loop stopped.")

def main():
    reminder = SmartClassReminder()
    while True:
        print("\n--- Smart Class Reminder Menu ---")
        print("1. Add a Class")
        print("2. Show All Classes")
        print("3. Search for a Class")
        print("4. Remove a Class")
        print("5. Start Reminder")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            reminder.add_class()
        elif choice == "2":
            reminder.show_classes()
        elif choice == "3":
            reminder.search_class()
        elif choice == "4":
            reminder.remove_class()
        elif choice == "5":
            reminder.reminder_loop()
        elif choice == "6":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
