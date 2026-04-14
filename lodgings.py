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
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        return [row for row in reader]


def load_rooms():
    with open(room_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        return [row for row in reader]


def display_lodgings(lodgings):
    print('\n=== HOTELS ===')
    for lodge in lodgings:
        print(f"{lodge[0]}. {lodge[1]}")


def search_lodgings():
    if not path.exists():
        create_lodgings_file()

    lodgings = load_lodgings()
    keyword = input("Keyword (or 'b' to go back): ").lower().strip()

    if keyword == 'b':
        return

    results = [l for l in lodgings if keyword in l[1].lower() or keyword in l[4].lower()]
    display_lodgings(results) if results else print('No results found.')


def browse_hotels():
    if not path.exists():
        create_lodgings_file()

    lodgings = load_lodgings()

    while True:
        display_lodgings(lodgings)
        hotel_id = input("Select Hotel ID (or 'b' to go back): ").strip()

        if hotel_id.lower() == 'b':
            return None

        for lodge in lodgings:
            if lodge[0] == hotel_id:
                return lodge

        print('Invalid Hotel ID.')


def show_rooms(hotel_id):
    rooms = load_rooms()

    while True:
        print('\n=== AVAILABLE ROOMS ===')

        choices = []
        for room in rooms:
            if room[1] == hotel_id:
                choices.append(room)
                print(f"{room[0]}. {room[2]} | ₱{room[3]} | Capacity: {room[4]}")

        room_id = input("Select Room ID (or 'b' to go back): ").strip()

        if room_id.lower() == 'b':
            return None

        for room in choices:
            if room[0] == room_id:
                return room

        print('Invalid Room ID.')


def select_room_only(hotel_id):
    rooms = load_rooms()

    while True:
        print("\n=== ROOMS ===")

        available_rooms = []
        for room in rooms:
            if room[1] == hotel_id:
                available_rooms.append(room)
                print(f"{room[0]}. {room[2]} | ₱{room[3]} | Capacity: {room[4]}")

        if not available_rooms:
            print("No rooms available.")
            return None

        print("0. Back")
        choice = input("Select Room ID: ").strip()

        if choice == "0":
            return None

        for room in available_rooms:
            if room[0] == choice:
                return room

        print("Invalid Room ID.")


def view_lodgings():
    if not path.exists():
        create_lodgings_file()

    lodgings = load_lodgings()

    while True:
        display_lodgings(lodgings)
        print("0. Back")

        hotel_id = input("Select Hotel ID: ").strip()

        if hotel_id == "0":
            return None

        selected = None
        for lodge in lodgings:
            if lodge[0] == hotel_id:
                selected = lodge
                break

        if not selected:
            print("Invalid Hotel ID.")
            continue

        room = select_room_only(hotel_id)

        if room:
            return selected, room