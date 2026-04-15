import csv
from pathlib import Path
from ui import header, card, input_prompt, error, success

filepath = 'files/lodgings.csv'
room_file = 'files/rooms.csv'
path = Path(filepath)


# =========================
# INIT DATA
# =========================
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


# =========================
# DISPLAY HOTELS (CLICKABLE LIST)
# =========================
def display_lodgings(lodgings):
    from ui import list_item

    header("🏨 Hotels")

    for lodge in lodgings:
        features = " | ".join(lodge[4].split("|"))

        list_item(
            lodge[0],
            lodge[1],
            f"🌟 {features}"
        )

    print()
    print("Type a Hotel ID to continue, or 'b' to go back.\n")


# =========================
# SEARCH HOTELS
# =========================
def search_lodgings():
    if not path.exists():
        create_lodgings_file()

    lodgings = load_lodgings()

    header("🔍 Search Hotels")

    keyword = input_prompt("Enter keyword (or 'b' to go back)").lower()

    if keyword == 'b':
        return

    results = [
        l for l in lodgings
        if keyword in l[1].lower() or keyword in l[4].lower()
    ]

    if not results:
        error("No results found. Try another keyword.")
        return

    header(f"🔍 Results for: '{keyword}'")

    for lodge in results:
        features = " | ".join(lodge[4].split("|"))

        card(
            f"🏨 {lodge[1]}",
            [
                f"🆔 ID: {lodge[0]}",
                f"🌟 {features}"
            ]
        )
        print()

    print("Enter a Hotel ID to view rooms, or 'b' to go back.\n")


# =========================
# BROWSE HOTELS (CARD STYLE)
# =========================
def browse_hotels():
    if not path.exists():
        create_lodgings_file()

    lodgings = load_lodgings()

    while True:
        header("🏨 Available Hotels")

        for lodge in lodgings:
            features = " | ".join(lodge[4].split("|"))

            card(
                f"🏨 {lodge[1]}",
                [
                    f"🆔 ID: {lodge[0]}",
                    f"🌟 {features}"
                ]
            )
            print()

        hotel_id = input_prompt("Enter Hotel ID to view rooms (or 'b' to go back)")

        if hotel_id.lower() == 'b':
            return None

        for lodge in lodgings:
            if lodge[0] == hotel_id:
                success(f"Selected {lodge[1]}")
                print("Loading available rooms...\n")
                return lodge

        error("Invalid Hotel ID. Please try again.")


# =========================
# ROOMS DISPLAY
# =========================
def select_room_only(hotel_id):
    rooms = load_rooms()

    while True:
        header("📍 Hotels > Rooms")

        available_rooms = []

        for room in rooms:
            if room[1] == hotel_id:
                available_rooms.append(room)

                card(
                    f"🛏 {room[2]}",
                    [
                        f"🆔 Room ID : {room[0]}",
                        f"💰 ₱{room[3]} / night",
                        f"👥 Capacity: {room[4]} guests"
                    ]
                )
                print()

        if not available_rooms:
            error("No rooms available for this hotel. Try another one.")
            return None

        choice = input_prompt("Enter Room ID to continue (or 'b' to go back)")

        if choice.lower() == "b":
            return None

        for room in available_rooms:
            if room[0] == choice:
                success(f"Selected {room[2]}")
                return room

        error("Invalid Room ID. Please try again.")


# =========================
# MAIN FLOW
# =========================
def view_lodgings():
    if not path.exists():
        create_lodgings_file()

    lodgings = load_lodgings()

    while True:
        display_lodgings(lodgings)

        hotel_id = input_prompt("Enter Hotel ID")

        if hotel_id.lower() == "b":
            return None

        selected = None
        for lodge in lodgings:
            if lodge[0] == hotel_id:
                selected = lodge
                break

        if not selected:
            error("Invalid Hotel ID. Please try again.")
            continue

        success(f"Selected {selected[1]}")
        print("Loading available rooms...\n")

        room = select_room_only(hotel_id)

        if room:
            return selected, room