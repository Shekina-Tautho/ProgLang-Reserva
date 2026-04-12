import csv
from pathlib import Path
from datetime import datetime
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
            "payment_ref",
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
    return int(bookings[-1][0]) + 1


# ✅ DATE VALIDATION
def is_valid_date(date_text):
    try:
        booking_date = datetime.strptime(date_text, "%Y-%m-%d")
        today = datetime.today()

        if booking_date.date() < today.date():
            print("❌ Cannot book a past date.")
            return False

        return True

    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        return False


# ✅ CAPACITY CHECK
def check_capacity(lodging_id, guests):
    lodgings = load_lodgings()

    for lodge in lodgings:
        if lodge[0] == lodging_id:
            capacity = int(lodge[3])
            return int(guests) <= capacity

    return False


# ✅ RECEIPT DISPLAY
def show_receipt(data):
    print("\n" + "=" * 40)
    print("        BOOKING RECEIPT")
    print("=" * 40)
    print(f"Booking ID : {data['id']}")
    print(f"User       : {data['user']}")
    print(f"Lodging    : {data['lodging']}")
    print(f"Guests     : {data['guests']}")
    print(f"Date       : {data['date']}")
    print(f"Payment Ref: {data['payment']}")
    print(f"Status     : {data['status']}")
    print("=" * 40 + "\n")


def make_reservation(username):
    try:
        if not path.exists():
            create_bookings_file()

        lodgings = load_lodgings()

        print("\n=== MAKE RESERVATION ===")

        for lodge in lodgings:
            print(f"{lodge[0]}. {lodge[1]} (Capacity: {lodge[3]})")

        # ✅ LODGING ID VALIDATION
        while True:
            lodging_id = input("Enter lodging ID: ").strip()
            if lodging_id:
                break
            print("❌ Lodging ID is required.")

        # ✅ GUEST VALIDATION LOOP
        while True:
            guests = input("Number of guests: ").strip()

            if not guests:
                print("❌ Guests is required.")
                continue

            if not guests.isdigit():
                print("❌ Guests must be a number.")
                continue

            break

        # ✅ DATE VALIDATION LOOP (FIXED)
        while True:
            date = input("Enter date (YYYY-MM-DD): ").strip()

            if not date:
                print("❌ Date is required.")
                continue

            if is_valid_date(date):
                break  # ONLY breaks if valid

        # ✅ PAYMENT VALIDATION LOOP
        while True:
            payment_ref = input("Enter payment reference: ").strip()

            if payment_ref:
                break

            print("❌ Payment reference is required.")

        # ✅ CAPACITY CHECK
        if not check_capacity(lodging_id, guests):
            print("❌ Exceeded lodging capacity.")
            return

        bookings = load_bookings()
        booking_id = generate_booking_id(bookings)

        lodging_name = ""
        for lodge in lodgings:
            if lodge[0] == lodging_id:
                lodging_name = lodge[1]
                break

        # SAVE BOOKING
        with open(filepath, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                booking_id,
                username,
                lodging_id,
                lodging_name,
                guests,
                date,
                payment_ref,
                "Pending"
            ])

        print("\n✅ Reservation submitted successfully!\n")

        # RECEIPT
        show_receipt({
            "id": booking_id,
            "user": username,
            "lodging": lodging_name,
            "guests": guests,
            "date": date,
            "payment": payment_ref,
            "status": "Pending"
        })

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

                print("=" * 40)
                print(f"Booking ID : {booking[0]}")
                print(f"Lodging    : {booking[3]}")
                print(f"Guests     : {booking[4]}")
                print(f"Date       : {booking[5]}")
                print(f"Payment Ref: {booking[6]}")
                print(f"Status     : {booking[7]}")
                print("=" * 40)

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
                continue
            updated.append(booking)

        if not found:
            print("❌ Booking not found or not yours.")
            return

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

        print("✅ Booking cancelled successfully.")

    except Exception as e:
        print("Error:", e)