import winsound

from .request import (
    calculate_distance_in_meters,
    google_maps_destination_lookup,
    location_check,
    save_destination_to_csv,
    validate_location_result,
)


def manual_destination_entry():
    """Ask the user to enter a destination coordinate pair manually."""
    print("\nEnter destination coordinates manually")
    try:
        latitude = float(input("Destination latitude: "))
        longitude = float(input("Destination longitude: "))
    except ValueError:
        print("Invalid input. Please enter numeric destination coordinates.")
        return {
            "status": "error",
            "message": "Destination coordinates must be numeric.",
        }

    location = (latitude, longitude)
    print(f"Destination saved: {location}")

    return {
        "status": "success",
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
    }


def manual_location_entry():
    """Ask the user to enter location details manually and return a coordinate pair."""
    print("\nEnter your location manually")
    try:
        latitude = float(input("Latitude: "))
        longitude = float(input("Longitude: "))
    except ValueError:
        print("Invalid input. Please enter numeric latitude and longitude values.")
        return {
            "status": "error",
            "message": "Latitude and longitude must be numeric.",
        }

    location = (latitude, longitude)
    print(f"Manual location saved: {location}")

    return {
        "status": "success",
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
    }


def check_location():
    """Fetch the current location and simplify it into one calculation-friendly variable."""
    result = location_check()

    if result.get("status") == "error":
        print("Location check failed:", result.get("message", "Unknown error"))
        return result

    if not validate_location_result(result):
        print(
            "Location check failed: invalid result received from the location service."
        )
        return {
            "status": "error",
            "message": "Location result is invalid or incomplete.",
        }

    location = result.get("location")

    print("Current location details:")
    print(f"IP: {result.get('ip')}")
    print(f"City: {result.get('city')}")
    print(f"Region: {result.get('region')}")
    print(f"Country: {result.get('country')}")
    print(f"Simple location: {location}")
    print(f"Latitude: {result.get('latitude')}")
    print(f"Longitude: {result.get('longitude')}")
    print(f"Timezone: {result.get('timezone')}")

    return {
        "status": result.get("status"),
        "location": location,
        "latitude": result.get("latitude"),
        "longitude": result.get("longitude"),
    }


def check_distance_alarm(current_location, destination, user_distance_meters):
    """Trigger an alarm when the current distance is less than a user-set threshold."""
    try:
        threshold_meters = float(user_distance_meters)
    except (TypeError, ValueError):
        return {
            "status": "error",
            "message": "Alarm distance must be numeric.",
        }

    if threshold_meters < 0:
        return {
            "status": "error",
            "message": "Alarm distance cannot be negative.",
        }

    distance_meters = calculate_distance_in_meters(current_location, destination)
    alarm_triggered = distance_meters < threshold_meters

    if alarm_triggered:
        try:
            winsound.Beep(1000, 500)
        except Exception:
            print("\a")

    return {
        "status": "success",
        "current_location": current_location,
        "destination": destination,
        "distance_meters": distance_meters,
        "threshold_meters": threshold_meters,
        "alarm_triggered": alarm_triggered,
        "message": (
            "Alarm triggered: you are within the user-defined distance."
            if alarm_triggered
            else "Distance is above the alarm threshold."
        ),
    }


def prompt_distance_alarm(current_location, destination):
    """Ask the user for the distance threshold and check whether the alarm should trigger."""
    try:
        user_distance = float(input("Set alarm distance in meters: "))
    except ValueError:
        return {
            "status": "error",
            "message": "Alarm distance must be numeric.",
        }

    return check_distance_alarm(current_location, destination, user_distance)


def track_destination():
    """Ask the user for the current and destination coordinates manually and compute the distance."""
    current_location = manual_location_entry()
    if current_location.get("status") == "error":
        return current_location

    destination = manual_destination_entry()
    if destination.get("status") == "error":
        return destination

    distance_meters = calculate_distance_in_meters(
        current_location["location"], destination["location"]
    )

    print("Destination location details:")
    print(f"Current location: {current_location.get('location')}")
    print(f"Destination coordinates: {destination.get('location')}")
    print(f"Distance from current location: {distance_meters:.0f} meters")

    alarm_result = prompt_distance_alarm(
        current_location["location"], destination["location"]
    )
    if alarm_result.get("status") == "success":
        print(
            f"Alarm threshold reached: {alarm_result.get('alarm_triggered')} | "
            f"Distance: {alarm_result.get('distance_meters'):.0f} meters"
        )
    else:
        print(alarm_result.get("message", "Unable to set the alarm threshold."))

    saved = save_destination_to_csv(
        current_location["location"],
        destination["location"],
        distance_meters,
    )
    if saved.get("status") == "success":
        print(f"Saved destination route to {saved.get('file_path')}")
    else:
        print(saved.get("message", "Unable to save route to CSV."))

    return {
        "status": "success",
        "current_location": current_location.get("location"),
        "destination": destination.get("location"),
        "latitude": destination.get("latitude"),
        "longitude": destination.get("longitude"),
        "distance_meters": distance_meters,
        "alarm": alarm_result,
        "csv": saved,
    }
