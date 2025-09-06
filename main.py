import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
import datetime
import threading
import time

FILE_NAME = "classes.json"

DAYS_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class SmartClassReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Class Reminder")
        self.root.geometry("700x450")
        self.root.configure(bg="#f0f4f8")
        self.classes = []
        self.load_classes()
        self.create_widgets()
        self.start_reminder_thread()

    # GUI Widgets
    def create_widgets(self):
        title_label = tk.Label(self.root, text="📚 Smart Class Reminder", font=("Arial", 18, "bold"), bg="#f0f4f8")
        title_label.pack(pady=10)

        frame = tk.Frame(self.root, bg="#f0f4f8")
        frame.pack(pady=10)

        tk.Button(frame, text="Add Class", command=self.add_class, width=15, bg="#4caf50", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Remove Class", command=self.remove_class, width=15, bg="#f44336", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Refresh List", command=self.show_classes, width=15, bg="#2196f3", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5)

        columns = ("Title", "Day", "Time", "Link")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150 if col != "Title" else 200, anchor="center")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 11), rowheight=30)

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

    # Show classes in treeview
    def show_classes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Sort classes by day and time
        def sort_key(cls):
            day_index = DAYS_ORDER.index(cls['day']) if cls['day'] in DAYS_ORDER else 7
            time_parts = cls['hour'].split(":")
            return (day_index, int(time_parts[0]), int(time_parts[1]))

        sorted_classes = sorted(self.classes, key=sort_key)

        for cls in sorted_classes:
            self.tree.insert("", "end", values=(cls['title'], cls['day'], cls['hour'], cls['link']))

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

    # Reminder thread with 5-minute pre-alert
    def start_reminder_thread(self):
        def reminder_loop():
            alerted = set()
            while True:
                now = datetime.datetime.now()
                current_day = now.strftime("%A")
                current_time = now.strftime("%H:%M")
                current_minutes = now.hour * 60 + now.minute

                for cls in self.classes:
                    if cls['day'] != current_day:
                        continue
                    class_hour, class_minute = map(int, cls['hour'].split(":"))
                    class_minutes = class_hour * 60 + class_minute
                    # Alert 5 minutes before class
                    if current_minutes == class_minutes - 5 and (cls['title'], cls['hour']) not in alerted:
                        messagebox.showinfo("Upcoming Class", f"Class '{cls['title']}' starts in 5 minutes!\nLink: {cls['link']}")
                        alerted.add((cls['title'], cls['hour']))
                    # Alert at class time
                    if current_minutes == class_minutes and (cls['title'], cls['hour']) not in alerted:
                        messagebox.showinfo("Class Reminder", f"Class '{cls['title']}' is starting now!\nLink: {cls['link']}")
                        alerted.add((cls['title'], cls['hour']))

                # Clear alerts after an hour
                alerted = {a for a in alerted if now.hour * 60 + now.minute - int(a[1].split(":")[0])*60 - int(a[1].split(":")[1]) < 60}

                time.sleep(60)

        thread = threading.Thread(target=reminder_loop, daemon=True)
        thread.start()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = SmartClassReminderApp(root)
    root.mainloop()
