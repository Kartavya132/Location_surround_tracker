from .request import location_check, validate_location_result


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
