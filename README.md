# 🚆 TRAIN-INFO-FETCHER

A comprehensive Python-based **CLI application** to fetch real-time Indian Railways data such as train schedules, live status, seat availability, fare details, coach layout, and station mapping using the [Indian Rail API](https://indianrailapi.com/).

> 🔧 This is a fully functional railway inquiry CLI tool — perfect for travelers, hobbyists, or as a portfolio project for developers.

---

## 🔍 Features

### ✅ **Train Schedule**
- Displays full route with station codes, names, arrival/departure times, and distances.
- Beautifully formatted using tables (`tabulate`).

### ✅ **Live Train Status**
- Real-time train running status.
- Shows current position, delay info, and last updated station.

### ✅ **Seat Availability**
- Shows availability for upcoming days.
- Supports input for class type and journey date.

### ✅ **Fare Inquiry**
- Returns fare amount based on source, destination, class, and quota.
- Output includes currency and quota details.

### ✅ **Coach Layout**
- Visualizes coach structure and features.

### ✅ **Coach Position**
- Displays current coach position if available.

### ✅ **Station Location on Map**
- Opens source and destination stations in Google Maps with one click.

### ✅ **Average Speed Calculation**
- Calculates rough average speed based on time and distance from the route data.

---

## 🛠️ Tech Stack

- **Python 3**
- `requests` — for API communication
- `tabulate` — for CLI tabular output
- `datetime` — time parsing & formatting
- `webbrowser` — for opening Google Maps

---

## 🧪 Sample Usage

```bash
$ python train_info_app.py
=== Indian Railways Info CLI App ===
Enter Train Number: 12222

📅 Fetching Train Schedule...
🛤️ Train Schedule for Train No: 12222
+--------+----------------+------------------+----------+------------+----------------+
| S.No   | Station Code   | Station Name     | Arrival  | Departure  | Distance (km)  |
|--------|----------------|------------------|----------|------------|----------------|
| 1      | HWH            | HOWRAH JN.       | 08:20:00 | 08:20:00   | 0              |
| ...    | ...            | ...              | ...      | ...        | ...            |
+--------+----------------+------------------+----------+------------+----------------+

⚡ Average Speed (approx): 60.5 km/h
🚆 Live Train Status: On Time at BHUSAVAL JN.
...
