import requests


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

    if not (
        isinstance(result["latitude"], (int, float))
        and isinstance(result["longitude"], (int, float))
    ):
        return False

    location_value = result["location"]

    if isinstance(location_value, (tuple, list)):
        if len(location_value) != 2:
            return False
        if not (
            isinstance(location_value[0], (int, float))
            and isinstance(location_value[1], (int, float))
        ):
            return False
        return True

    if isinstance(location_value, dict):
        if not (
            isinstance(location_value.get("latitude"), (int, float))
            and isinstance(location_value.get("longitude"), (int, float))
        ):
            return False
        return True

    return False


def location_check():
    """Return the current approximate location of the device using public IP geolocation."""
    try:
        ip_response = requests.get("https://api.ipify.org?format=json", timeout=5)
        ip_response.raise_for_status()
        public_ip = ip_response.json().get("ip")

        if not public_ip:
            return {
                "status": "error",
                "message": "Could not detect the public IP address.",
            }

        geo_response = requests.get(f"https://ipapi.co/{public_ip}/json/", timeout=10)
        geo_response.raise_for_status()
        data = geo_response.json()

        if data.get("error"):
            return {
                "status": "error",
                "message": data.get("reason", "Unable to determine location."),
            }

        latitude = data.get("latitude")
        longitude = data.get("longitude")

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


if __name__ == "__main__":
    print("Oops You came in wrong file\nGo to main.py")
