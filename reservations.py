import csv
from pathlib import Path
from datetime import datetime
from lodgings import browse_hotels, show_rooms

filepath = 'files/bookings.csv'
path = Path(filepath)


def create_bookings_file():
    Path('files').mkdir(exist_ok=True)
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'booking_id', 'username', 'lodging_id', 'lodging_name',
            'guests', 'check_in', 'check_out', 'payment_ref', 'status'
        ])


def load_bookings():
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        return [row for row in reader]


def generate_booking_id(bookings):
    return 1 if not bookings else int(bookings[-1][0]) + 1


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


def make_reservation(username, hotel=None, room=None):
    if not path.exists():
        create_bookings_file()

    # STEP 1: SELECT HOTEL & ROOM (if not passed)
    if not hotel:
        hotel = browse_hotels()
        if not hotel:
            return

    if not room:
        room = show_rooms(hotel[0])
        if not room:
            return

    # STEP 2: INPUT GUESTS
    while True:
        guests = input('Number of guests: ').strip()
        if guests.isdigit() and int(guests) <= int(room[4]):
            guests = int(guests)
            break
        print('Invalid guests count.')

    # STEP 3: INPUT DATES
    while True:
        check_in = input('Enter check-in date (YYYY-MM-DD): ').strip()
        check_out = input('Enter check-out date (YYYY-MM-DD): ').strip()

        try:
            in_date = datetime.strptime(check_in, '%Y-%m-%d')
            out_date = datetime.strptime(check_out, '%Y-%m-%d')

            if in_date.date() >= datetime.today().date() and out_date > in_date:
                break
        except:
            pass

        print('Invalid dates.')

    # STEP 4: COMPUTE PRICE
    lodging_name = hotel[1] + ' - ' + room[2]
    price_per_night = int(room[3])
    nights = (out_date - in_date).days
    total = price_per_night * nights

    print("\n=== BOOKING SUMMARY ===")
    print(f"Lodging     : {lodging_name}")
    print(f"Price/night : ₱{price_per_night}")
    print(f"Nights      : {nights}")
    print(f"Total       : ₱{total}")

    # STEP 5: CONFIRMATION
    confirm = input("\nConfirm reservation? (y/n): ").strip().lower()

    if confirm != 'y':
        print("Reservation cancelled.")
        return

    # STEP 6: CHECK AVAILABILITY
    if not is_room_available(lodging_name, check_in, check_out):
        print('❌ Room is already booked.')
        return

    # STEP 7: GENERATE ID
    bookings = load_bookings()
    booking_id = generate_booking_id(bookings)

    # STEP 8: WRITE TO FILE
    with open(filepath, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            booking_id,
            username,
            hotel[0],
            lodging_name,
            guests,
            check_in,
            check_out,
            "",  # payment_ref later
            "Pending Payment"
        ])

    print("\nReservation submitted successfully!")
    

def view_my_bookings(username):
    if not path.exists():
        print("No bookings found.")
        return

    bookings = load_bookings()
    found = False

    print("\n=== MY BOOKINGS ===\n")

    for booking in bookings:
        if booking[1] == username:
            found = True

            print("=" * 50)
            print(f" Booking ID : {booking[0]}")
            print(f" Lodging   : {booking[3]}")
            print(f" Guests    : {booking[4]}")
            print(f" Check-in  : {booking[5]}")
            print(f" Check-out : {booking[6]}")
            print(f" Payment   : {booking[7]}")
            print(f" Status    : {booking[8]}")
            print("=" * 50)
            print()

    if not found:
        print("You have no bookings.")
        
        
def cancel_booking(username):
    if not path.exists():
        return

    bookings = load_bookings()

    booking_id = input("Enter Booking ID to cancel (or 'b' to go back): ").strip()

    if booking_id.lower() == 'b':
        return

    updated = []
    found = False

    for booking in bookings:
        if booking[0] == booking_id and booking[1] == username:
            found = True
            continue
        updated.append(booking)

    if found:
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'booking_id',
                'username',
                'lodging_id',
                'lodging_name',
                'guests',
                'check_in',
                'check_out',
                'payment_ref',
                'status'
            ])
            writer.writerows(updated)

        print('Booking cancelled successfully.')
    else:
        print('Booking not found or not yours.')