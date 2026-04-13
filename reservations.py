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
        writer.writerow(['booking_id', 'username', 'lodging_id', 'lodging_name', 'guests', 'date', 'payment_ref', 'status'])


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
        date = input('Enter date (YYYY-MM-DD): ').strip()
        try:
            d = datetime.strptime(date, '%Y-%m-%d')
            if d.date() >= datetime.today().date():
                break
        except:
            pass
        print('Invalid date.')

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
            date,
            payment_ref,
            'Pending'
        ])

    print('Reservation submitted successfully!')


def view_my_bookings(username):
    if not path.exists():
        return
    for booking in load_bookings():
        if booking[1] == username:
            print(booking)


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
            writer.writerow(['booking_id', 'username', 'lodging_id', 'lodging_name', 'guests', 'date', 'payment_ref', 'status'])
            writer.writerows(updated)
        print('Booking cancelled successfully.')
    else:
        print('Booking not found or not yours.')