import csv
from pathlib import Path
from datetime import datetime
from lodgings import browse_hotels, select_room_only
from ui import header, card, input_prompt, error, success

filepath = 'files/bookings.csv'
path = Path(filepath)


# =========================
# INIT FILE
# =========================
def create_bookings_file():
    Path('files').mkdir(exist_ok=True)
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'booking_id', 'username', 'lodging_id', 'lodging_name',
            'guests', 'check_in', 'check_out', 'payment_ref', 'status'
        ])


def load_bookings():
    try:
        if not path.exists():
            return []

        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)
            return [row for row in reader]

    except FileNotFoundError:
        return []
    except Exception:
        return []


def generate_booking_id(bookings):
    return 1 if not bookings else int(bookings[-1][0]) + 1


# =========================
# AVAILABILITY CHECK
# =========================
def is_room_available(lodging_name, check_in, check_out):
    bookings = load_bookings()

    new_in = datetime.strptime(check_in, '%Y-%m-%d')
    new_out = datetime.strptime(check_out, '%Y-%m-%d')

    for booking in bookings:
        if booking[3] != lodging_name or booking[8] != 'Approved':
            continue

        existing_in = datetime.strptime(booking[5], '%Y-%m-%d')
        existing_out = datetime.strptime(booking[6], '%Y-%m-%d')

        if new_in < existing_out and new_out > existing_in:
            return False

    return True


# =========================
# MAKE RESERVATION
# =========================
def make_reservation(username, hotel=None, room=None):
    if not path.exists():
        create_bookings_file()

    header("📌 New Reservation")

    if not hotel:
        hotel = browse_hotels()
        if not hotel:
            return

    if not room:
        room = select_room_only(hotel[0])
        if not room:
            return

    success(f"Selected {hotel[1]} - {room[2]}")

    # STEP 2: GUESTS
    while True:
        guests = input_prompt("Enter number of guests")
        if guests.isdigit():
            g = int(guests)
            if 1 <= g <= int(room[4]):
                break
        error("Invalid guest count. Must not exceed room capacity.")

    # STEP 3: DATES
    while True:
        check_in = input_prompt("Check-in date (YYYY-MM-DD)")
        check_out = input_prompt("Check-out date (YYYY-MM-DD)")

        try:
            in_date = datetime.strptime(check_in, '%Y-%m-%d')
            out_date = datetime.strptime(check_out, '%Y-%m-%d')

            if in_date.date() >= datetime.today().date() and out_date > in_date:
                break
        except ValueError:
            error("Invalid format. Use YYYY-MM-DD.")
            continue

        error("Invalid dates.")

    lodging_name = f"{hotel[1]} - {room[2]}"
    price_per_night = int(room[3])
    nights = (out_date - in_date).days
    total = price_per_night * nights

    header("🧾 Booking Summary")

    card(
        lodging_name,
        [
            f"💰 ₱{price_per_night} / night",
            f"🌙 Nights: {nights}",
            f"🧾 Total: ₱{total}"
        ]
    )

    confirm = input_prompt("Confirm reservation? (y/n)").lower()

    if confirm != 'y':
        error("Reservation cancelled.")
        return

    if not is_room_available(lodging_name, check_in, check_out):
        error("Room is already booked for selected dates.")
        return

    # ✅ FIX: PROPER SAVE
    bookings = load_bookings()
    booking_id = generate_booking_id(bookings)

    new_booking = [
        booking_id,
        username,
        hotel[0],
        lodging_name,
        g,
        check_in,
        check_out,
        "",
        "Pending Payment"
    ]

    try:
        with open(filepath, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_booking)

        success("Reservation submitted successfully!")

    except Exception as e:
        error(f"Failed to save reservation: {e}")


# =========================
# PAYMENT
# =========================
def pay_for_booking(username):
    try:
        bookings = load_bookings()

        if not bookings:
            error("No bookings found.")
            return

        header("💳 Payment")

        booking_id = input_prompt("Enter Booking ID to pay (or 'b' to go back)")

        if not booking_id.strip():
            error("Booking ID cannot be empty.")
            return

        if booking_id.lower() == 'b':
            return

        updated = []
        found = False

        for booking in bookings:

            # SAFE CHECK: prevent crash if row is corrupted
            if len(booking) < 9:
                updated.append(booking)
                continue

            if booking[0] == booking_id and booking[1] == username:
                found = True

                if booking[8] != "Pending Payment":
                    error("This booking is not awaiting payment.")
                    updated.append(booking)
                    continue

                card(
                    f"Booking #{booking[0]}",
                    [
                        f"🏨 {booking[3]}",
                        f"📅 {booking[5]} → {booking[6]}",
                        f"📌 Status: {booking[8]}"
                    ]
                )

                payment_ref = input_prompt("Enter payment reference")

                while payment_ref.strip() == "":
                    error("Payment reference cannot be empty.")
                    payment_ref = input_prompt("Enter payment reference")

                booking[7] = payment_ref
                booking[8] = "Paid"

                success("Payment successful!")

            updated.append(booking)

        if not found:
            error("Booking not found or not yours.")
            return

        # SAFE FILE WRITE
        try:
            with open(filepath, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "booking_id", "username", "lodging_id", "lodging_name",
                    "guests", "check_in", "check_out", "payment_ref", "status"
                ])
                writer.writerows(updated)

        except PermissionError:
            error("File is currently in use. Try again.")
        except Exception:
            error("Unexpected error while saving payment.")

    except Exception:
        error("Something went wrong during payment processing.")


# =========================
# VIEW BOOKINGS
# =========================
def view_my_bookings(username):
    bookings = load_bookings()

    if not bookings:
        error("No bookings found.")
        return

    header("📊 My Bookings")

    status_icons = {
        "Pending Payment": "🟡 Pending Payment",
        "Paid": "💳 Paid",
        "Approved": "🟢 Approved",
        "Rejected": "🔴 Rejected"
    }

    found = False

    for booking in bookings:
        if booking[1] == username:
            found = True

            card(
                f"Booking #{booking[0]}",
                [
                    f"🏨 {booking[3]}",
                    f"👥 Guests: {booking[4]}",
                    f"📅 {booking[5]} → {booking[6]}",
                    f"💳 Payment: {booking[7] or 'N/A'}",
                    f"📌 Status: {status_icons.get(booking[8], booking[8])}"
                ]
            )
            print()

    if not found:
        error("You have no bookings yet.")
        print("👉 Try making a reservation first.\n")


# =========================
# CANCEL BOOKING
# =========================
def cancel_booking(username):
    bookings = load_bookings()

    if not bookings:
        error("No bookings found.")
        return

    header("❌ Cancel Booking")

    booking_id = input_prompt("Enter Booking ID (or 'b' to go back)")

    if booking_id.lower() == 'b':
        return

    updated = []
    found = False
    cancelled = False

    for booking in bookings:
        if booking[0] == booking_id and booking[1] == username:
            found = True

            card(
                f"Booking #{booking[0]}",
                [
                    f"🏨 {booking[3]}",
                    f"📅 {booking[5]} → {booking[6]}",
                    f"📌 Status: {booking[8]}"
                ]
            )

            if booking[8] in ["Approved", "Rejected"]:
                error("Cannot cancel processed booking.")
                updated.append(booking)
                continue

            confirm = input_prompt("Confirm cancellation? (y/n)").lower()

            if confirm == 'y':
                cancelled = True
                success("Booking cancelled.")
                continue
            else:
                updated.append(booking)
                continue

        updated.append(booking)

    if not found:
        error("Booking not found or not yours.")
        return

    if cancelled:
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'booking_id', 'username', 'lodging_id', 'lodging_name',
                'guests', 'check_in', 'check_out', 'payment_ref', 'status'
            ])
            writer.writerows(updated)