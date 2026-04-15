import csv
from pathlib import Path
from ui import header, error, success

filepath = 'files/bookings.csv'
path = Path(filepath)


# =========================
# LOAD BOOKINGS (SAFE)
# =========================
def load_bookings():
    if not path.exists():
        return []

    bookings = []

    try:
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                # SAFE: skip corrupted rows
                if len(row) < 9:
                    continue
                bookings.append(row)

    except Exception:
        return []

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
    bookings = load_bookings()

    if not bookings:
        error("No bookings found.")
        return

    header("📊 ADMIN BOOKINGS DASHBOARD")

    print(f"{'ID':<5} | {'USER':<12} | {'LODGING':<25} | {'STATUS':<18} | {'PAYMENT':<15}")
    print("-" * 90)

    for b in bookings:
        status = status_icons.get(b[8], b[8])
        print(f"{b[0]:<5} | {b[1]:<12} | {b[3]:<25} | {status:<18} | {b[7]:<15}")

    print("-" * 90)


# =========================
# FILTER BY STATUS
# =========================
def view_bookings_by_status(status_filter):
    bookings = load_bookings()

    header(f"📊 BOOKINGS - {status_filter}")

    found = False

    print(f"{'ID':<5} | {'USER':<12} | {'LODGING':<25} | {'STATUS':<18} | {'PAYMENT':<15}")
    print("-" * 90)

    for b in bookings:
        if len(b) < 9:
            continue

        if b[8] == status_filter:
            found = True
            status = status_icons.get(b[8], b[8])
            print(f"{b[0]:<5} | {b[1]:<12} | {b[3]:<25} | {status:<18} | {b[7]:<15}")

    if not found:
        error("No records found.")

    print("-" * 90)


# =========================
# UPDATE BOOKING STATUS
# =========================
def update_booking_status():
    bookings = load_bookings()

    if not bookings:
        error("No bookings found.")
        return

    while True:
        booking_id = input("Enter Booking ID (or 'b' to go back): ").strip()

        if booking_id.lower() == 'b':
            return

        if not booking_id.isdigit():
            error("Booking ID must be numeric.")
            continue

        target = None

        for b in bookings:
            if len(b) < 9:
                continue
            if b[0] == booking_id:
                target = b
                break

        if not target:
            error("Invalid Booking ID.")
            continue

        if target[8] != "Paid":
            error("Only PAID bookings can be approved or rejected.")
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
            error("Invalid choice.")
            continue

        # update safely
        for b in bookings:
            if b[0] == booking_id:
                b[8] = new_status
                break

        try:
            with open(filepath, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "booking_id", "username", "lodging_id", "lodging_name",
                    "guests", "check_in", "check_out", "payment_ref", "status"
                ])
                writer.writerows(bookings)

            success(f"Booking {new_status} successfully.")

        except Exception:
            error("Failed to update booking file.")

        return


# =========================
# ADMIN MENU
# =========================
def admin_menu():
    while True:
        print("\n" + "=" * 55)
        print("         🛠 ADMIN DASHBOARD")
        print("=" * 55)
        print("1. View All Bookings")
        print("2. Pending Payments")
        print("3. Paid Bookings")
        print("4. Approved Bookings")
        print("5. Rejected Bookings")
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
            view_bookings_by_status("Approved")
        elif choice == "5":
            view_bookings_by_status("Rejected")
        elif choice == "6":
            update_booking_status()
        elif choice == "7":
            print("Logging out...")
            break
        else:
            error("Invalid choice.")