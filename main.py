import time
import tkinter as tk
from ctypes import windll
from plyer import notification
import sys

def check_screen_status():
    # Use Windows API to check if the screen is off
    SC_MONITORPOWER = 0xF170
    monitor_power_state = windll.user32.SendMessageW(0xFFFF, 0x0112, SC_MONITORPOWER, -1)
    return monitor_power_state != 2  # 2 means screen is off

def set_window_geometry(root, width_percentage, height_percentage):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * width_percentage)
    window_height = int(screen_height * height_percentage)

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

def show_reminder(normal_mode=True):
    root = tk.Tk()
    root.title("Reminder")
    set_window_geometry(root, 0.4, 0.4)  # 40% of the screen size

    notification_title = "Screen Reminder"
    notification_message = "Look away for 20 seconds"

    if normal_mode:
        label = tk.Label(root, text=notification_message, font=("Helvetica", 14))
        label.pack(pady=20)

        countdown_label = tk.Label(root, text="22", font=("Helvetica", 16))
        countdown_label.pack()

        def countdown(count):
            countdown_label.config(text=str(count))
            if count > 0:
                root.after(1000, countdown, count - 1)
            else:
                root.destroy()

        countdown(22)
        root.mainloop()
    else:
        notification.notify(
            title=notification_title,
            message=notification_message,
            app_name="Screen Reminder",
            timeout=20
        )

def main(reminder_interval):
    mode, reminder_interval = ask_user_mode(reminder_interval)  # Ask for user mode and reminder interval at the start
    screen_time = 0
    reminder_interval_seconds = reminder_interval * 60  # Convert minutes to seconds

    while True:
        time.sleep(5)  # Check every 5 seconds instead of every second
        if check_screen_status():
            screen_time += 5  # Increment by 5 seconds
        else:
            print("Screen is off. Exiting...")
            sys.exit()  # Terminate the process

        if screen_time >= reminder_interval_seconds:
            if mode == "normal":
                show_reminder(normal_mode=True)
            elif mode == "silent":
                show_reminder(normal_mode=False)
            screen_time = 0

def ask_user_mode(default_interval):
    root = tk.Tk()
    root.title("Mode and Interval Selection")
    set_window_geometry(root, 0.4, 0.4)  # 40% of the screen size

    label = tk.Label(root, text="Choose reminder mode:", font=("Helvetica", 14))
    label.pack(pady=10)

    interval_label = tk.Label(root, text="Enter reminder interval (minutes):", font=("Helvetica", 12))
    interval_label.pack(pady=5)
    
    interval_entry = tk.Entry(root)
    interval_entry.insert(0, str(default_interval))
    interval_entry.pack(pady=5)

    def set_mode_and_interval(mode):
        root.mode = mode
        root.interval = int(interval_entry.get())
        root.destroy()

    normal_button = tk.Button(root, text="Normal Mode", command=lambda: set_mode_and_interval("normal"))
    normal_button.pack(pady=5)

    silent_button = tk.Button(root, text="Silent Mode", command=lambda: set_mode_and_interval("silent"))
    silent_button.pack(pady=5)

    root.mainloop()

    return root.mode, root.interval

if __name__ == "__main__":
    default_interval = 20  # Default reminder interval in minutes
    main(default_interval)