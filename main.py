import func.function as fnf
from sys import exit


def print_header(header):
    """Print a clean header banner for the app."""
    print("=" * 60)
    print(header.center(60))
    print("=" * 60)


def main():
    print_header("Welcome to GPS radius checker")
    gps_choice = input("Do you want us to check your current location : ")
    if (
        ("Yes" in gps_choice)
        or ("yaah" in gps_choice)
        or ("1" in gps_choice)
        or ("y" in gps_choice)
    ):
        fnf.check_location()
    elif (
        ("No" in gps_choice)
        or ("na" in gps_choice)
        or ("0" in gps_choice)
        or ("n" in gps_choice)
    ):
        fnf.manual_location_entry()


if __name__ == "__main__":
    main()
