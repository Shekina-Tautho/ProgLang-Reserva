import csv
from pathlib import Path

filepath = 'files/bookings.csv'
path = Path(filepath)


# =========================
# LOAD BOOKINGS
# =========================
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


# =========================
# STATUS ICONS
# =========================
status_icons = {
    "Pending Payment": "🟡 Pending",
    "Paid": "💳 Paid",
    "Approved": "🟢 Approved",
    "Rejected": "🔴 Rejected"
}


# =========================
# VIEW ALL BOOKINGS
# =========================
def view_all_bookings():
    if not path.exists():
        print("No bookings found.")
        return

    bookings = load_bookings()

    print("\n" + "=" * 110)
    print(" " * 40 + "📊 ADMIN BOOKINGS DASHBOARD")
    print("=" * 110)

    print(f"{'ID':<5} | {'USER':<12} | {'LODGING':<25} | {'STATUS':<18} | {'PAYMENT':<15}")
    print("-" * 110)

    for b in bookings:
        status = status_icons.get(b[8], b[8])

        print(f"{b[0]:<5} | {b[1]:<12} | {b[3]:<25} | {status:<18} | {b[7]:<15}")

    print("=" * 110)


# =========================
# FILTER VIEW (ALL STATUSES)
# =========================
def view_bookings_by_status(status_filter):
    bookings = load_bookings()

    print("\n" + "=" * 110)
    print(f" 📊 BOOKINGS - {status_filter.upper()}")
    print("=" * 110)

    print(f"{'ID':<5} | {'USER':<12} | {'LODGING':<25} | {'STATUS':<18} | {'PAYMENT':<15}")
    print("-" * 110)

    found = False

    for b in bookings:
        if b[8] == status_filter:
            found = True
            status = status_icons.get(b[8], b[8])
            print(f"{b[0]:<5} | {b[1]:<12} | {b[3]:<25} | {status:<18} | {b[7]:<15}")

    if not found:
        print("No records found.")

    print("=" * 110)


# =========================
# UPDATE BOOKING STATUS
# =========================
def update_booking_status():
    if not path.exists():
        print("No bookings found.")
        return

    bookings = load_bookings()

    while True:
        booking_id = input("Enter Booking ID (or 'b' to go back): ").strip()

        if booking_id.lower() == 'b':
            return

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

        print("\nBooking found:")
        print(f"Lodging : {target[3]}")
        print(f"Status  : {target[8]}")

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

        for b in bookings:
            if b[0] == booking_id:
                b[8] = new_status
                break

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


# =========================
# ADMIN MENU (FINAL UPGRADE)
# =========================
def admin_menu():
    while True:
        print("\n" + "=" * 55)
        print("         🛠 ADMIN DASHBOARD")
        print("=" * 55)
        print("1. View All Bookings")
        print("2. View Pending Payments")
        print("3. View Paid Bookings")
        print("4. View Approved Bookings")   # ✅ ADDED
        print("5. View Rejected Bookings")   # ✅ ADDED
        print("6. Approve / Reject Booking")
        print("7. Logout")
        print("=" * 55)

        choice = input("Enter choice: ").strip()

        if choice == "1":
            view_all_bookings()

        elif choice == "2":
            view_bookings_by_status("Pending Payment")

        elif choice == "3":
            view_bookings_by_status("Paid")

        elif choice == "4":
            view_bookings_by_status("Approved")   # ✅ NEW

        elif choice == "5":
            view_bookings_by_status("Rejected")   # ✅ NEW

        elif choice == "6":
            update_booking_status()

        elif choice == "7":
            print("Logging out...")
            break

        else:
            print("Invalid choice.")