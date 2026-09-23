<div align="center">

# 📍 Location Surround Tracker

**A lightweight Python utility for calculating distance between coordinates and triggering proximity alerts.**

![Python](https://img.shields.io/badge/python-3.7%2B-3776AB?logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Formula](https://img.shields.io/badge/distance-Haversine-blueviolet)
![Status](https://img.shields.io/badge/status-active-brightgreen)

</div>

---

## 🧭 Overview

**Location Surround Tracker** calculates the distance between two latitude/longitude coordinates and can trigger an alarm when the distance falls below a user-defined threshold.

It ships with both a simple **command-line workflow** and a **desktop GUI** built with Tkinter, making it useful for quick distance checks, destination tracking, and proximity alerts.

---

## 📑 Table of Contents

- [Features](#-features)
- [Why This Project Exists](#-why-this-project-exists)
- [Project Structure](#️-project-structure)
- [Requirements](#-requirements)
- [How to Run](#-how-to-run)
- [How It Works](#-how-it-works)
- [Distance Logic](#-distance-logic)
- [Output File](#-output-file)
- [Testing](#-testing)
- [Quick Example](#-quick-example)
- [Summary](#-summary)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📐 **Haversine Distance** | Accurate geospatial distance calculation between two coordinates |
| ⌨️ **Manual Entry** | Enter current and destination coordinates by hand |
| 🚨 **Alarm Threshold** | Set a distance (in meters) that triggers an alert |
| 🔊 **Audio Alert** | Sound notification when the target is within range |
| 📄 **CSV Logging** | Every tracked route is logged to `location.csv` |
| 🌐 **IP-Based Lookup** | Optional public IP location lookup |
| 🖥️ **GUI + CLI** | Use the Tkinter desktop app or the terminal — your choice |

---

## 🧭 Why This Project Exists

This app is designed for quick proximity checks such as:

- ✅ Checking how far you are from a destination
- ✅ Comparing current coordinates against a saved target
- ✅ Triggering an alert when you enter a safe/unsafe radius
- ✅ Keeping a simple record of tracked routes in a CSV file

---

## 🏗️ Project Structure

```text
Location_surround_tracker/
├── app.py                 # Tkinter desktop interface
├── main.py                # CLI entry point
├── start_app.bat          # Windows launcher for the GUI app
├── location.csv           # Generated CSV output from tracked routes
├── README.md              # Project documentation
├── func/
│   ├── function.py        # Input helpers, alarm logic, UI-related logic
│   ├── request.py         # Coordinate validation, distance calculation, CSV saving
│   └── location.csv       # Optional local generated CSV location data
├── tests/
│   └── test_project.py    # Project validation tests
└── requirements.txt       # Optional dependency listing (if added later)
```

> **Note:** This project currently relies on the Python standard library plus the `requests` package for location lookups.

---

## 🔧 Requirements

Install the one external dependency if needed:

```powershell
pip install requests
```

---

## 🚀 How to Run

### Option 1 — GUI (recommended)

Double-click the launcher:

```powershell
start_app.bat
```

Or run it directly:

```powershell
python app.py
```

### Option 2 — Command Line

```powershell
python main.py
```

---

## 📝 How It Works

1. Enter the **current** latitude and longitude.
2. Enter the **destination** latitude and longitude.
3. Set the **alarm threshold** in meters.
4. The app calculates the direct distance between the two points.
5. If the distance is below the threshold, an **alarm is triggered**.
6. The result is saved to a **CSV file** for later review.

---

## 📊 Distance Logic

Distance is calculated using the **Haversine formula**, which models the shortest path over the Earth's surface:

```python
# Approximate great-circle distance between two lat/lon points
# using Earth's radius in meters
```

This provides a practical estimate for nearby geographic checks without needing external mapping services for the core math.

---

## 📁 Output File

Route data is saved to `location.csv` with the following columns:

| Column | Description |
|---|---|
| `current_latitude` | Latitude of the current position |
| `current_longitude` | Longitude of the current position |
| `destination_latitude` | Latitude of the destination |
| `destination_longitude` | Longitude of the destination |
| `distance_meters` | Computed distance between the two points |

---

## 🧪 Testing

Run the full test suite with:

```powershell
python -m unittest discover -s tests
```

The tests cover:

- ✅ Module imports
- ✅ Manual coordinate input
- ✅ Distance summaries
- ✅ Coordinate distance calculation
- ✅ CSV saving
- ✅ Proximity alarm triggering

---

## 💡 Quick Example

| | Latitude | Longitude |
|---|---|---|
| **Current location** | `40.7128` | `-74.0060` |
| **Destination** | `34.0522` | `-118.2437` |

The app computes the distance between those coordinates and reports it in meters, along with an alarm check if a threshold is set.

---

## ✅ Summary

This project combines geolocation math, alerting, CSV logging, and a friendly UI into a compact Python tool for tracking nearby locations and distance thresholds.

<div align="center">

**Made with 🐍 Python + 📐 Haversine math**

</div>