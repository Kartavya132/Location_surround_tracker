import func.function as fnf
from sys import exit


def print_header(header):
    """Print a clean header banner for the app."""
    print("=" * 60)
    print(header.center(60))
    print("=" * 60)


def main():
    print_header("Welcome to GPS radius checker")
    gps_choice = (
        input("Do you want to enter your current coordinates manually? ")
        .strip()
        .lower()
    )

    if gps_choice in {"yes", "yaah", "y", "1", "yeah", "sure"}:
        current = fnf.manual_location_entry()
        if current.get("status") == "error":
            return
    else:
        print("Current coordinates were not entered.")
        return

    destination_choice = (
        input("Do you want to enter the destination coordinates manually? ")
        .strip()
        .lower()
    )
    if destination_choice in {"yes", "y", "1", "yeah", "sure"}:
        destination = fnf.manual_destination_entry()
        if destination.get("status") == "error":
            return

        distance = fnf.calculate_distance_in_meters(
            current["location"], destination["location"]
        )
        print(f"Distance from current location to destination: {distance:.0f} meters")

        alarm_result = fnf.prompt_distance_alarm(
            current["location"], destination["location"]
        )
        if alarm_result.get("status") == "success":
            print(
                f"Alarm triggered: {alarm_result.get('alarm_triggered')} | "
                f"Threshold: {alarm_result.get('threshold_meters')} m"
            )
        else:
            print(alarm_result.get("message", "Unable to set the alarm threshold."))

        csv_result = fnf.save_destination_to_csv(
            current["location"],
            destination["location"],
            distance,
        )
        if csv_result.get("status") == "success":
            print(f"Destination saved in location.csv: {csv_result.get('file_path')}")
        else:
            print(csv_result.get("message"))


if __name__ == "__main__":
    main()
