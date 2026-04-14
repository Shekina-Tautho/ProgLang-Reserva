import csv
from pathlib import Path

filepath = 'files/bookings.csv'
path = Path(filepath)


def load_bookings():
    if not path.exists():
        return []

    bookings = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            bookings.append(row)

    return bookings


def view_all_bookings():
    if not path.exists():
        print("No bookings found.")
        return

    bookings = load_bookings()

    print("\n=== ALL BOOKINGS ===\n")

    print(f"{'ID':<5} | {'User':<12} | {'Lodging':<25} | {'Status':<10} | {'Payment':<15}")
    print("-" * 80)

    for b in bookings:
        print(f"{b[0]:<5} | {b[1]:<12} | {b[3]:<25} | {b[8]:<10} | {b[7]:<15}")


def update_booking_status():
    if not path.exists():
        print("No bookings found.")
        return

    bookings = load_bookings()

    while True:
        booking_id = input("Enter Booking ID (or 'b' to go back): ").strip()

        if booking_id.lower() == 'b':
            return

        # find booking
        target = None
        for b in bookings:
            if b[0] == booking_id:
                target = b
                break

        if not target:
            print("❌ Invalid Booking ID. Try again.")
            continue
        
        if target[8] != "Paid":
            print("❌ Only PAID bookings can be approved or rejected.")
            return

        # ONLY PAID CAN BE APPROVED/REJECTED
        if target[8] != "Paid":
            print("❌ Only PAID bookings can be approved or rejected.")
            return

        print("\nBooking found:")
        print(f"Lodging : {target[3]}")
        print(f"Status   : {target[8]}")

        print("\n1. Approve")
        print("2. Reject")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            new_status = "Approved"
        elif choice == "2":
            new_status = "Rejected"
        else:
            print("❌ Invalid choice.")
            continue

        # update booking
        for b in bookings:
            if b[0] == booking_id:
                b[8] = new_status
                break

        # write back
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "booking_id",
                "username",
                "lodging_id",
                "lodging_name",
                "guests",
                "check_in",
                "check_out",
                "payment_ref",
                "status"
            ])
            writer.writerows(bookings)

        print(f"✅ Booking {new_status} successfully.")
        return


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