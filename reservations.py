import csv
from pathlib import Path
from lodgings import load_lodgings

filepath = 'files/bookings.csv'
path = Path(filepath)


def create_bookings_file():
    Path("files").mkdir(exist_ok=True)

    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "booking_id",
            "username",
            "lodging_id",
            "lodging_name",
            "guests",
            "date",
            "status"
        ])


def load_bookings():
    bookings = []

    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            bookings.append(row)

    return bookings


def generate_booking_id(bookings):
    if not bookings:
        return 1
    else:
        return int(bookings[-1][0]) + 1


def check_capacity(lodging_id, guests):
    lodgings = load_lodgings()

    for lodge in lodgings:
        if lodge[0] == lodging_id:
            capacity = int(lodge[3])

            if int(guests) > capacity:
                return False

    return True


def make_reservation(username):
    try:
        if not path.exists():
            create_bookings_file()

        lodgings = load_lodgings()

        print("\n=== MAKE RESERVATION ===")

        for lodge in lodgings:
            print(f"{lodge[0]}. {lodge[1]} (Capacity: {lodge[3]})")

        lodging_id = input("Enter lodging ID: ").strip()
        guests = input("Number of guests: ").strip()
        date = input("Enter date (YYYY-MM-DD): ").strip()

        # ✅ Validation
        if lodging_id == "" or guests == "" or date == "":
            print("All fields are required.")
            return

        if not guests.isdigit():
            print("Guests must be a number.")
            return

        if not check_capacity(lodging_id, guests):
            print("Exceeded lodging capacity.")
            return

        bookings = load_bookings()
        booking_id = generate_booking_id(bookings)

        # Get lodging name
        lodging_name = ""
        for lodge in lodgings:
            if lodge[0] == lodging_id:
                lodging_name = lodge[1]
                break

        # Save booking
        with open(filepath, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                booking_id,
                username,
                lodging_id,
                lodging_name,
                guests,
                date,
                "Pending"
            ])

        print("\nReservation submitted! Status: Pending\n")

    except Exception as e:
        print("Error:", e)


def view_my_bookings(username):
    try:
        if not path.exists():
            print("No bookings found.")
            return

        bookings = load_bookings()

        print("\n=== MY BOOKINGS ===")

        found = False

        for booking in bookings:
            if booking[1] == username:
                found = True
                print(f"""
Booking ID: {booking[0]}
Lodging: {booking[3]}
Guests: {booking[4]}
Date: {booking[5]}
Status: {booking[6]}
-----------------------------""")

        if not found:
            print("No bookings yet.")

    except Exception as e:
        print("Error:", e)


def cancel_booking(username):
    try:
        if not path.exists():
            print("No bookings found.")
            return

        bookings = load_bookings()

        booking_id = input("Enter Booking ID to cancel: ").strip()

        updated = []
        found = False

        for booking in bookings:
            if booking[0] == booking_id and booking[1] == username:
                found = True
                continue  # remove it
            updated.append(booking)

        if not found:
            print("Booking not found or not yours.")
            return

        # Rewrite file
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "booking_id",
                "username",
                "lodging_id",
                "lodging_name",
                "guests",
                "date",
                "status"
            ])
            writer.writerows(updated)

        print("Booking cancelled successfully.")

    except Exception as e:
        print("Error:", e)