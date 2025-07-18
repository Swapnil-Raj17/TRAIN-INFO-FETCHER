import requests
from datetime import datetime
from tabulate import tabulate
import sys
import webbrowser

API_KEY = "a6e95c7150eaf50b84e32dc2c1c14ecd"
BASE_URL = "https://indianrailapi.com/api/v2"

def api_get(api_name, path_segments):
    """
    Constructs URL with API key right after api_name segment.
    api_name: str, e.g. "trainschedule"
    path_segments: list of strings, e.g. ["trainnumber", "11301"]
    """
    url = f"{BASE_URL}/{api_name}/apikey/{API_KEY}/" + "/".join(path_segments)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("ResponseCode") != "200":
            print(f"API Error: {data.get('Message', 'Unknown error')}")
            return None
        return data
    except requests.RequestException as e:
        print(f"Network/API request failed: {e}")
        return None

def get_train_schedule(train_number):
    return api_get("trainschedule", ["trainnumber", train_number])

def get_live_train_status(train_number, date_str):
    return api_get("livetrainstatus", ["trainnumber", train_number, "date", date_str])

def get_seat_availability(train_number, source_code, dest_code, journey_date, class_code):
    return api_get("checkseatavailability", [
        "trainnumber", train_number,
        "trainStartDate", journey_date,
        "from", source_code,
        "to", dest_code,
        "classcode", class_code
    ])

def get_fare(train_number, source_code, dest_code, class_code, quota="GN"):
    return api_get("trainfare", [
        "trainnumber", train_number,
        "from", source_code,
        "to", dest_code,
        "classcode", class_code,
        "quota", quota
    ])

def get_coach_layout(train_number, coach_number):
    return api_get("coachlayout", ["trainnumber", train_number, "coachnumber", coach_number])

def get_coach_position(train_number, coach_number, train_date):
    return api_get("coachposition", ["trainnumber", train_number, "coachnumber", coach_number, "traindate", train_date])

def calculate_average_speed(distance_km, total_hours):
    if total_hours == 0:
        return 0
    return round(distance_km / total_hours, 2)

def display_schedule(route_data):
    headers = ["S.No", "Station Code", "Station Name", "Arrival", "Departure", "Distance (km)"]
    rows = []
    for stop in route_data:
        rows.append([
            stop.get("SerialNo", ""),
            stop.get("StationCode", ""),
            stop.get("StationName", ""),
            stop.get("ArrivalTime", ""),
            stop.get("DepartureTime", ""),
            stop.get("Distance", "")
        ])
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def display_live_status(live_status):
    print("\n🚆 Live Train Status:")
    if not live_status or "TrainPosition" not in live_status:
        print("No live status available.")
        return
    print(f"Current Position: {live_status['TrainPosition']}")
    if 'Position' in live_status:
        print(f"Position: {live_status['Position']}")
    if 'Delay' in live_status:
        print(f"Delay: {live_status['Delay']} minutes")

def display_seat_availability(seat_data):
    print("\n💺 Seat Availability:")
    if not seat_data or "Availability" not in seat_data:
        print("No seat availability data found.")
        return
    avail = seat_data["Availability"]
    headers = ["Date", "Status"]
    rows = [[entry["Date"], entry["Status"]] for entry in avail]
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def display_fare(fare_data):
    print("\n💰 Fare Details:")
    if not fare_data or "Fare" not in fare_data:
        print("No fare data found.")
        return
    print(f"Fare: ₹{fare_data['Fare']}")
    print(f"Currency: {fare_data.get('Currency', 'INR')}")

def display_coach_layout(layout_data):
    print("\n🚋 Coach Layout:")
    if not layout_data or "CoachType" not in layout_data:
        print("No coach layout data found.")
        return
    print(f"Coach Type: {layout_data['CoachType']}")
    print(f"Features: {layout_data.get('Features', 'N/A')}")

def display_station_location(station_code):
    url = f"https://www.google.com/maps/search/{station_code}+railway+station"
    print(f"\n🌍 Station Location on Map: {url}")
    open_map = input("Open this location in your browser? (y/n): ").strip().lower()
    if open_map == 'y':
        webbrowser.open(url)

def main():
    print("=== Indian Railways Info CLI App ===")
    train_no = input("Enter Train Number: ").strip()
    if not train_no.isdigit():
        print("Invalid train number!")
        sys.exit(1)

    print("\n📅 Fetching Train Schedule...")
    schedule = get_train_schedule(train_no)
    if not schedule or "Route" not in schedule:
        print("Failed to get train schedule.")
        sys.exit(1)

    print(f"\n🛤️ Train Schedule for Train No: {train_no}")
    display_schedule(schedule["Route"])

    try:
        first_stop = schedule["Route"][0]
        last_stop = schedule["Route"][-1]
        total_distance = float(last_stop.get("Distance", 0))

        def parse_time(t):
            return datetime.strptime(t, "%H:%M:%S") if t else None

        arrival_first = parse_time(first_stop.get("ArrivalTime"))
        departure_last = parse_time(last_stop.get("DepartureTime"))

        journey_hours = 24 if arrival_first is None or departure_last is None else \
            (departure_last - arrival_first).seconds / 3600

        avg_speed = calculate_average_speed(total_distance, journey_hours)
        print(f"\n⚡ Average Speed (approx): {avg_speed} km/h")
    except Exception as e:
        print(f"Failed to calculate average speed: {e}")

    today = datetime.today().strftime("%d-%m-%Y")
    live_status = get_live_train_status(train_no, today)
    display_live_status(live_status)

    print("\nTo check Seat Availability and Fare, please provide journey details.")
    source_code = input("Enter Source Station Code (e.g., NDLS): ").strip().upper()
    dest_code = input("Enter Destination Station Code (e.g., BCT): ").strip().upper()
    journey_date = input("Enter Journey Date (DD-MM-YYYY): ").strip()
    class_code = input("Enter Class Code (e.g., SL, 3A, 2A, CC): ").strip().upper()

    seat_avail = get_seat_availability(train_no, source_code, dest_code, journey_date, class_code)
    display_seat_availability(seat_avail)

    fare_data = get_fare(train_no, source_code, dest_code, class_code)
    display_fare(fare_data)

    want_coach = input("\nDo you want coach layout and position info? (y/n): ").strip().lower()
    if want_coach == 'y':
        coach_no = input("Enter Coach Number (e.g., B1, S2): ").strip().upper()
        layout_data = get_coach_layout(train_no, coach_no)
        display_coach_layout(layout_data)

        coach_pos = get_coach_position(train_no, coach_no, journey_date)
        if coach_pos:
            print("\n🚋 Coach Position Info:")
            print(coach_pos.get("CoachPosition", "No position data available."))

    display_station_location(source_code)
    display_station_location(dest_code)

    print("\nThank you for using the Indian Railways Info CLI App!")

if __name__ == "__main__":
    main()
