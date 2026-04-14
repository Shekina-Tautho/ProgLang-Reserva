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


def load_bookings():
    data = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            data.append(row)
    return data


def generate_booking_id(bookings):
    return 1 if not bookings else int(bookings[-1][0]) + 1



def is_room_available(lodging_name, check_in, check_out):
    bookings = load_bookings()

    new_in = datetime.strptime(check_in, '%Y-%m-%d')
    new_out = datetime.strptime(check_out, '%Y-%m-%d')

    for booking in bookings:
        existing_lodging = booking[3]
        existing_status = booking[8]

        if existing_lodging != lodging_name or existing_status != 'Approved':
            continue

        existing_in = datetime.strptime(booking[5], '%Y-%m-%d')
        existing_out = datetime.strptime(booking[6], '%Y-%m-%d')

        # 🔥 OVERLAP CHECK
        if new_in < existing_out and new_out > existing_in:
            return False

    return True


def make_reservation(username):
    if not path.exists():
        create_bookings_file()

    hotel = browse_hotels()
    if not hotel:
        return

    room = show_rooms(hotel[0])
    if not room:
        return

    while True:
        guests = input('Number of guests: ').strip()
        if guests.isdigit() and int(guests) <= int(room[4]):
            break
        print('Invalid guests count.')

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

        print('Invalid dates. Make sure check-out is after check-in.')

    lodging_name = hotel[1] + ' - ' + room[2]

    if not is_room_available(lodging_name, check_in, check_out):
        print('❌ Room is already booked for those dates.')
        return

    payment_ref = input('Enter payment reference: ').strip()

    bookings = load_bookings()
    booking_id = generate_booking_id(bookings)

    with open(filepath, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            booking_id,
            username,
            hotel[0],
            hotel[1] + ' - ' + room[2],
            guests,
            check_in,
            check_out,
            payment_ref,
            'Pending'
        ])

    print('Reservation submitted successfully!')


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
    booking_id = input('Enter Booking ID to cancel: ').strip()
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
        