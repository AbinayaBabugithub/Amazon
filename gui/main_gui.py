import json
import threading
import time
import sys
import os
import tkinter as tk
import winsound  # Changed from playsound to winsound
from tkinter import ttk, messagebox
from bot import run_bot


class BotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Amazon Shift Finder Bot")
        self.geometry("500x400")
        self.configure(bg="#f0f0f0")

        self.config = self.load_config()
        self.stop_flag = threading.Event()
        self.retry_interval_seconds = 2  # Define retry interval here

        self.create_widgets()

    def load_config(self):
        try:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            json_path = os.path.join(base_path, 'gui', 'job_config.json')  # Correct path for bundled file

            with open(json_path, 'r') as file:
                config = json.load(file)
            return config
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load job_config.json: {e}")
            return {"locations": [], "preferences": {}}

    def create_widgets(self):
        title = tk.Label(self, text="Amazon Job Bot", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        # Removed location dropdown as bot will check all locations
        # No longer need self.location_var or ttk.Combobox for locations

        self.status_label = tk.Label(self, text="Status: Ready", font=("Helvetica", 12), bg="#f0f0f0", wraplength=400,
                                     justify="left")
        self.status_label.pack(pady=10)

        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=20)

        self.start_button = tk.Button(button_frame, text="Start Bot", command=self.start_bot,
                                      font=("Helvetica", 14), bg="#4CAF50", fg="white",
                                      relief="raised", padx=10, pady=5)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(button_frame, text="Stop Bot", command=self.stop_bot,
                                     font=("Helvetica", 14), bg="#f44336", fg="white",
                                     relief="raised", padx=10, pady=5, state=tk.DISABLED)
        self.stop_button.pack(side=tk.RIGHT, padx=10)

    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")
        self.update_idletasks()  # Ensure GUI updates immediately

    def start_bot(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        thread = threading.Thread(target=self.run_bot_for_all_locations)
        thread.start()

    def stop_bot(self):
        self.stop_flag.set()
        self.update_status("Stop requested. Please wait...")
        self.start_button.config(state=tk.NORMAL)  # Enable start button immediately
        self.stop_button.config(state=tk.DISABLED)  # Disable stop button

    def run_bot_for_all_locations(self):
        locations = self.config["locations"]
        preferences = self.config.get("preferences", {})
        self.stop_flag.clear()

        if not locations:
            self.update_status("No locations configured in job_config.json.")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            return

        self.update_status("Starting bot: Checking all configured locations...")

        while not self.stop_flag.is_set():
            shift_booked_in_cycle = False
            for location_config in locations:
                if self.stop_flag.is_set():
                    break  # Exit loop if stop is requested

                # Call bot.py's run_bot for each location
                success = run_bot(
                    location_config=location_config,
                    preferences=preferences,
                    stop_flag=self.stop_flag,
                    status_callback=self.update_status
                )

                if success:
                    shift_booked_in_cycle = True
                    break  # Exit inner loop if a shift is booked, bot will stop

            if shift_booked_in_cycle:
                self.update_status("✅ Shift booked successfully! Bot stopping.")
                # winsound.PlaySound(os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), "gui", "assets", "success.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
                break  # Exit outer loop if a shift was booked

            if not self.stop_flag.is_set() and not shift_booked_in_cycle:
                self.update_status(
                    f"❌ No shift found across all locations. Retrying in {self.retry_interval_seconds} seconds...")
                time.sleep(self.retry_interval_seconds)  # Wait before cycling through locations again

        if self.stop_flag.is_set():
            self.update_status("Bot stopped by user.")

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)


def start_gui():
    app = BotApp()
    app.mainloop()