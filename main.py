import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
import datetime
import threading
import time

FILE_NAME = "classes.json"

class SmartClassReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Class Reminder")
        self.root.geometry("600x400")
        self.classes = []
        self.load_classes()
        self.create_widgets()
        self.start_reminder_thread()

         # GUI Widgets
    def create_widgets(self):
        # Frame for buttons
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="Add Class", command=self.add_class).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Remove Class", command=self.remove_class).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Refresh List", command=self.show_classes).grid(row=0, column=2, padx=5)

        # Treeview for class list
        self.tree = ttk.Treeview(self.root, columns=("Day", "Time", "Link"), show="headings")
        self.tree.heading("Day", text="Day")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Link", text="Link")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.show_classes()

     # Add a class
    def add_class(self):
        title = simpledialog.askstring("Class Title", "Enter class title:")
        if not title: return
        day = simpledialog.askstring("Day", "Enter day (e.g., Monday):")
        if not day: return
        hour = simpledialog.askstring("Time", "Enter start time (HH:MM, 24h):")
        if not hour: return
        link = simpledialog.askstring("Link", "Enter online session link:")
        if not link: return

        self.classes.append({
            "title": title,
            "day": day.capitalize(),
            "hour": hour,
            "link": link
        })
        self.save_classes()
        self.show_classes()
        messagebox.showinfo("Success", f"Class '{title}' added!")
    # Display all classes
     # Show classes in treeview
    def show_classes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for cls in self.classes:
            self.tree.insert("", "end", values=(cls['day'], cls['hour'], cls['link']), text=cls['title'])
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

    # Remove selected class
    def remove_class(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a class to remove!")
            return
        index = self.tree.index(selected[0])
        removed_class = self.classes.pop(index)
        self.save_classes()
        self.show_classes()
        messagebox.showinfo("Removed", f"Class '{removed_class['title']}' removed!")
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
