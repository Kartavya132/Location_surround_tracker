import tkinter as tk
from tkinter import messagebox

import main
from func import function as fnf


class LocationTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Location Surround Tracker")
        self.geometry("520x500")
        self.minsize(420, 420)

        self.current_lat_label = tk.Label(self, text="Current latitude:")
        self.current_lat_label.pack(pady=(15, 0), padx=15, anchor="w")
        self.current_lat_entry = tk.Entry(self, width=35)
        self.current_lat_entry.pack(padx=15, fill="x")

        self.current_lon_label = tk.Label(self, text="Current longitude:")
        self.current_lon_label.pack(pady=(10, 0), padx=15, anchor="w")
        self.current_lon_entry = tk.Entry(self, width=35)
        self.current_lon_entry.pack(padx=15, fill="x")

        self.dest_lat_label = tk.Label(self, text="Destination latitude:")
        self.dest_lat_label.pack(pady=(10, 0), padx=15, anchor="w")
        self.dest_lat_entry = tk.Entry(self, width=35)
        self.dest_lat_entry.pack(padx=15, fill="x")

        self.dest_lon_label = tk.Label(self, text="Destination longitude:")
        self.dest_lon_label.pack(pady=(10, 0), padx=15, anchor="w")
        self.dest_lon_entry = tk.Entry(self, width=35)
        self.dest_lon_entry.pack(padx=15, fill="x")

        self.threshold_label = tk.Label(self, text="Alarm threshold in meters:")
        self.threshold_label.pack(pady=(10, 0), padx=15, anchor="w")
        self.threshold_entry = tk.Entry(self, width=35)
        self.threshold_entry.pack(padx=15, fill="x")

        self.calculate_button = tk.Button(
            self, text="Check Distance", command=self.calculate_distance
        )
        self.calculate_button.pack(pady=(18, 8), padx=15, fill="x")

        self.result_text = tk.Text(self, height=12, wrap="word")
        self.result_text.pack(padx=15, pady=(0, 15), fill="both", expand=True)

    def _safe_float(self, value, label):
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"{label} must be a valid number.")

    def calculate_distance(self):
        try:
            current_location = (
                self._safe_float(self.current_lat_entry.get(), "Current latitude"),
                self._safe_float(self.current_lon_entry.get(), "Current longitude"),
            )
            destination = (
                self._safe_float(self.dest_lat_entry.get(), "Destination latitude"),
                self._safe_float(self.dest_lon_entry.get(), "Destination longitude"),
            )
            threshold_value = self.threshold_entry.get().strip()
            threshold_meters = float(threshold_value) if threshold_value else None

            distance = fnf.calculate_distance_in_meters(current_location, destination)
            summary = main.build_distance_summary(
                current_location, destination, distance, threshold_meters
            )

            alarm_result = (
                fnf.check_distance_alarm(
                    current_location, destination, threshold_meters
                )
                if threshold_meters is not None
                else {
                    "status": "success",
                    "alarm_triggered": False,
                    "message": "No alarm threshold provided.",
                }
            )

            if alarm_result.get("status") == "success":
                summary += f"\nAlarm result: {alarm_result.get('message')}"
            else:
                summary += f"\nAlarm result: {alarm_result.get('message')}"

            result = fnf.save_destination_to_csv(
                current_location, destination, distance
            )
            if result.get("status") == "success":
                summary += f"\nSaved to: {result.get('file_path')}"
            else:
                summary += f"\nSave result: {result.get('message')}"

            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, summary)
        except ValueError as exc:
            messagebox.showerror("Input error", str(exc))
        except Exception as exc:  # pragma: no cover - GUI safety
            messagebox.showerror("Application error", f"Unexpected error: {exc}")


if __name__ == "__main__":
    app = LocationTrackerApp()
    app.mainloop()
