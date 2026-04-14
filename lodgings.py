import csv
from pathlib import Path

filepath = 'files/lodgings.csv'
room_file = 'files/rooms.csv'
path = Path(filepath)


def create_lodgings_file():
    Path('files').mkdir(exist_ok=True)
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'price', 'capacity', 'features'])
        writer.writerow([1, 'Beach Resort', 2500, 4, 'WiFi|Pool|Breakfast'])
        writer.writerow([2, 'Mountain Cabin', 1800, 3, 'Fireplace|View'])
        writer.writerow([3, 'City Hotel', 3200, 2, 'WiFi|Gym|Breakfast'])
        writer.writerow([4, 'Budget Inn', 900, 2, 'WiFi'])


def load_lodgings():
    data = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            data.append(row)
    return data


def load_rooms():
    data = []
    with open(room_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            data.append(row)
    return data


def display_lodgings(lodgings):
    print('\n=== HOTELS ===')
    for lodge in lodgings:
        print(f"{lodge[0]}. {lodge[1]}")


def search_lodgings():
    if not path.exists():
        create_lodgings_file()
    lodgings = load_lodgings()
    keyword = input('Keyword: ').lower().strip()
    results = []
    for lodge in lodgings:
        if keyword in lodge[1].lower() or keyword in lodge[4].lower():
            results.append(lodge)
    display_lodgings(results) if results else print('No results found.')


def browse_hotels():
    if not path.exists():
        create_lodgings_file()

    lodgings = load_lodgings()

    while True:
        display_lodgings(lodgings)
        print("0. Back")

        hotel_id = input("Select Hotel ID (or 'b' to go back): ").strip()

        if hotel_id == "0" or hotel_id.lower() == 'b':
            return None

        for lodge in lodgings:
            if lodge[0] == hotel_id:
                return lodge

        print('Invalid Hotel ID.')


def show_rooms(hotel_id):
    rooms = load_rooms()
    choices = []
    print('\n=== AVAILABLE ROOMS ===')
    for room in rooms:
        if room[1] == hotel_id:
            choices.append(room)
            print(f"{room[0]}. {room[2]} | ₱{room[3]} | Capacity: {room[4]}")
    room_id = input('Choose Room ID: ').strip()
    for room in choices:
        if room[0] == room_id:
            return room
    print('Invalid Room ID.')
    return None

def view_lodgings():
    if not path.exists():
        create_lodgings_file()
    lodgings = load_lodgings()
    display_lodgings(lodgings)