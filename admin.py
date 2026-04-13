import csv
from pathlib import Path

filepath = 'files/bookings.csv'
path = Path(filepath)


def load_bookings():
    bookings = []

    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            bookings.append(row)

    return bookings


def view_all_bookings():
    try:
        if not path.exists():
            print("No bookings found.")
            return

        bookings = load_bookings()

        print("\n=== ALL BOOKINGS ===")

        # Table Header
        print(f"{'ID':<5} | {'User':<15} | {'Lodging':<20} | {'Guests':<6} | {'Check-in':<12} | {'Check-out':<12} | {'Payment Ref':<15} | {'Status':<10}")
        print("-" * 120)

        # Table Rows
        for booking in bookings:
            print(f"{booking[0]:<5} | {booking[1]:<15} | {booking[3]:<20} | {booking[4]:<6} | {booking[5]:<12} | {booking[6]:<12} | {booking[7]:<15} | {booking[8]:<10}")

    except Exception as e:
        print("Error:", e)


def update_booking_status():
    try:
        if not path.exists():
            print("No bookings found.")
            return

        bookings = load_bookings()

        booking_id = input("Enter Booking ID: ").strip()

        print("1. Approve")
        print("2. Reject")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            new_status = "Approved"
        elif choice == "2":
            new_status = "Rejected"
        else:
            print("Invalid choice.")
            return

        updated = []
        found = False

        for booking in bookings:
            if booking[0] == booking_id:
                booking[8] = new_status
                found = True
            updated.append(booking)

        if not found:
            print("Booking ID not found.")
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
                "payment_ref",
                "status"
            ])
            writer.writerows(updated)

        print(f"Booking {new_status} successfully.")

    except Exception as e:
        print("Error:", e)


def admin_menu():
    while True:
        print("\n=== ADMIN MENU ===")
        print("1. View All Bookings")
        print("2. Approve / Reject Booking")
        print("3. Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            view_all_bookings()

        elif choice == "2":
            update_booking_status()

        elif choice == "3":
            print("\nLogging out...\n")
            break

        else:
            print("Invalid choice.")