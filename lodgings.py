import csv
from pathlib import Path
from ui import header, card, input_prompt, error, success

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
    from ui import list_item

    print("\n=== HOTELS ===\n")

    for lodge in lodgings:
        features = lodge[4].split("|")
        feature_text = " | ".join(features)

        list_item(
            lodge[0],  # ID
            lodge[1],  # NAME
            f"{feature_text}"
        )


def search_lodgings():
    from ui import header, error, input_prompt, card

    if not path.exists():
        create_lodgings_file()

    lodgings = load_lodgings()

    header("Search Hotels")

    keyword = input_prompt("Enter keyword (or 'b' to go back)").lower()

    if keyword == 'b':
        return

    results = [
        l for l in lodgings
        if keyword in l[1].lower() or keyword in l[4].lower()
    ]

    if not results:
        error("No results found.")
        return

    for lodge in results:
        features = lodge[4].split("|")

        card(
            lodge[1],
            [
                f"Hotel ID: {lodge[0]}",
                f"₱{lodge[2]} / night",
                f"Capacity: {lodge[3]} guests",
                f"Features: {' | '.join(features)}"
            ]
        )


def browse_hotels():
    from ui import header, card, input_prompt, error, success

    if not path.exists():
        create_lodgings_file()

    lodgings = load_lodgings()

    while True:
        header("Available Hotels")

        for lodge in lodgings:
            features = lodge[4].split("|")

            card(
                lodge[1],
                [
                    f"Hotel ID: {lodge[0]}",
                    f"₱{lodge[2]} / night",
                    f"Features: {' | '.join(features)}"
                ]
            )

        hotel_id = input_prompt("Enter Hotel ID (or 'b' to go back)")

        if hotel_id.lower() == 'b':
            return None

        for lodge in lodgings:
            if lodge[0] == hotel_id:
                success(f"Selected {lodge[1]}")
                return lodge

        error("Invalid Hotel ID")


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
    from ui import header, card, input_prompt, error

    rooms = load_rooms()

    while True:
        header("Available Rooms")

        available_rooms = []

        for room in rooms:
            if room[1] == hotel_id:
                available_rooms.append(room)

                card(
                    room[2],  # room type (optional title)
                    [
                        f"Room ID: {room[0]}",
                        f"₱{room[3]} / night",
                        f"Capacity: {room[4]} guests"
                    ]
                )

        if not available_rooms:
            error("No rooms available.")
            return None

        choice = input_prompt("Select Room ID (or 'b' to go back)")

        if choice.lower() == "b":
            return None

        for room in available_rooms:
            if room[0] == choice:
                return room

        error("Invalid Room ID")


def view_lodgings():
    if not path.exists():
        create_lodgings_file()

    lodgings = load_lodgings()

    while True:
        display_lodgings(lodgings)

        hotel_id = input("Select Hotel ID (or 'b' to go back): ").strip()

        if hotel_id == "b":
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