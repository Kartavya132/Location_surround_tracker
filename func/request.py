import csv
import math
from pathlib import Path

import requests


def _coerce_float(value):
    """Convert numeric strings to floats while rejecting invalid or boolean values."""
    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        try:
            return float(stripped)
        except ValueError:
            return None

    return None


def validate_location_result(result):
    """Validate a location result before accepting it as correct."""
    if not isinstance(result, dict):
        return False

    if result.get("status") != "success":
        return result.get("status") == "error"

    required_fields = [
        "ip",
        "latitude",
        "longitude",
        "city",
        "region",
        "country",
        "postal_code",
        "timezone",
        "location",
    ]

    for key in required_fields:
        if key not in result or result[key] is None:
            return False

    latitude = _coerce_float(result["latitude"])
    longitude = _coerce_float(result["longitude"])
    if latitude is None or longitude is None:
        return False

    location_value = result["location"]

    if isinstance(location_value, (tuple, list)):
        if len(location_value) != 2:
            return False
        if (
            _coerce_float(location_value[0]) is None
            or _coerce_float(location_value[1]) is None
        ):
            return False
        return True

    if isinstance(location_value, dict):
        if (
            _coerce_float(location_value.get("latitude")) is None
            or _coerce_float(location_value.get("longitude")) is None
        ):
            return False
        return True

    return False


def location_check():
    """Return the current approximate location of the device using public IP geolocation."""
    try:
        ip_response = requests.get("https://api.ipify.org?format=json", timeout=5)
        ip_response.raise_for_status()
        ip_data = ip_response.json()

        if not isinstance(ip_data, dict):
            return {
                "status": "error",
                "message": "Could not detect the public IP address.",
            }

        public_ip = ip_data.get("ip")
        if not public_ip:
            return {
                "status": "error",
                "message": "Could not detect the public IP address.",
            }

        geo_response = requests.get(f"https://ipapi.co/{public_ip}/json/", timeout=10)
        geo_response.raise_for_status()
        data = geo_response.json()

        if not isinstance(data, dict):
            return {
                "status": "error",
                "message": "Received an invalid response from the location service.",
            }

        if data.get("error"):
            return {
                "status": "error",
                "message": data.get("reason", "Unable to determine location."),
            }

        latitude = _coerce_float(data.get("latitude"))
        longitude = _coerce_float(data.get("longitude"))
        if latitude is None or longitude is None:
            return {
                "status": "error",
                "message": "Location result is invalid or incomplete.",
            }

        result = {
            "status": "success",
            "ip": public_ip,
            "latitude": latitude,
            "longitude": longitude,
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country_name"),
            "postal_code": data.get("postal"),
            "timezone": data.get("timezone"),
            "location": (latitude, longitude),
        }

        if not validate_location_result(result):
            return {
                "status": "error",
                "message": "Location result is invalid or incomplete.",
            }

        return result

    except requests.RequestException as exc:
        return {
            "status": "error",
            "message": f"Network error while fetching location: {exc}",
        }
    except ValueError:
        return {
            "status": "error",
            "message": "Received an invalid response from the location service.",
        }


def calculate_distance_in_meters(start_point, end_point):
    """Return the distance in meters between two latitude/longitude coordinate pairs."""
    if not isinstance(start_point, (tuple, list)) or len(start_point) != 2:
        raise ValueError("start_point must be a (latitude, longitude) tuple or list")
    if not isinstance(end_point, (tuple, list)) or len(end_point) != 2:
        raise ValueError("end_point must be a (latitude, longitude) tuple or list")

    lat1 = _coerce_float(start_point[0])
    lon1 = _coerce_float(start_point[1])
    lat2 = _coerce_float(end_point[0])
    lon2 = _coerce_float(end_point[1])

    if None in {lat1, lon1, lat2, lon2}:
        raise ValueError("Coordinates must be numeric latitude/longitude values.")

    earth_radius_m = 6371000.0
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return earth_radius_m * c


def _parse_coordinate_pair(value):
    """Accept a coordinate pair as a tuple, list, or string like 'lat, lon'."""
    if isinstance(value, (tuple, list)) and len(value) == 2:
        lat = _coerce_float(value[0])
        lon = _coerce_float(value[1])
        if lat is not None and lon is not None:
            return (lat, lon)
        return None

    if isinstance(value, str):
        cleaned = value.strip().replace("(", "").replace(")", "")
        if not cleaned:
            return None

        if "," in cleaned:
            pieces = cleaned.split(",")
        else:
            pieces = cleaned.split()

        if len(pieces) != 2:
            return None

        lat = _coerce_float(pieces[0])
        lon = _coerce_float(pieces[1])
        if lat is not None and lon is not None:
            return (lat, lon)

    return None


def google_maps_destination_lookup(destination):
    """This simplified version accepts manually supplied coordinates instead of a Google API lookup."""
    if destination is None:
        return {
            "status": "error",
            "message": "Destination coordinate is required.",
        }

    coordinates = _parse_coordinate_pair(destination)
    if coordinates is None:
        return {
            "status": "error",
            "message": "Enter destination coordinates as latitude, longitude.",
        }

    latitude, longitude = coordinates
    return {
        "status": "success",
        "destination": destination,
        "latitude": latitude,
        "longitude": longitude,
        "location": (latitude, longitude),
        "google_maps_url": None,
    }


def save_destination_to_csv(
    current_location,
    destination,
    distance_meters,
    file_path="location.csv",
):
    """Save current and destination coordinates and computed distance into a CSV file."""
    try:
        current_latitude = _coerce_float(current_location[0])
        current_longitude = _coerce_float(current_location[1])
        destination_latitude = _coerce_float(destination[0])
        destination_longitude = _coerce_float(destination[1])
        distance_value = _coerce_float(distance_meters)

        if None in {
            current_latitude,
            current_longitude,
            destination_latitude,
            destination_longitude,
            distance_value,
        }:
            return {
                "status": "error",
                "message": "Invalid coordinates or distance provided.",
            }

        csv_path = Path(file_path)
        csv_path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "current_latitude",
            "current_longitude",
            "destination_latitude",
            "destination_longitude",
            "distance_meters",
        ]

        file_exists = csv_path.exists()
        with csv_path.open("a", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(
                {
                    "current_latitude": current_latitude,
                    "current_longitude": current_longitude,
                    "destination_latitude": destination_latitude,
                    "destination_longitude": destination_longitude,
                    "distance_meters": distance_value,
                }
            )

        return {
            "status": "success",
            "file_path": str(csv_path),
            "distance_meters": distance_value,
        }
    except (TypeError, ValueError, OSError) as exc:
        return {
            "status": "error",
            "message": f"Unable to save destination to CSV: {exc}",
        }


if __name__ == "__main__":
    print("Oops You came in wrong file\nGo to main.py")
