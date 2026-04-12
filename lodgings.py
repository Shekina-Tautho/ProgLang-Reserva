import csv
from pathlib import Path

filepath = 'files/lodgings.csv'
path = Path(filepath)


def create_lodgings_file():
    Path("files").mkdir(exist_ok=True)

    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)

        # Header
        writer.writerow(["id", "name", "price", "capacity", "features"])

        # Sample data
        writer.writerow([1, "Beach Resort", 2500, 4, "WiFi|Pool|Breakfast"])
        writer.writerow([2, "Mountain Cabin", 1800, 3, "Fireplace|View"])
        writer.writerow([3, "City Hotel", 3200, 2, "WiFi|Gym|Breakfast"])
        writer.writerow([4, "Budget Inn", 900, 2, "WiFi"])


def load_lodgings():
    lodgings = []

    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header

        for row in reader:
            lodgings.append(row)

    return lodgings


def display_lodgings(lodgings):
    print("\n=== AVAILABLE LODGINGS ===")

    for lodge in lodgings:
        print(f"""
ID: {lodge[0]}
Name: {lodge[1]}
Price: ₱{lodge[2]}
Capacity: {lodge[3]} persons
Features: {lodge[4].replace('|', ', ')}
-----------------------------""")


def view_lodgings():
    try:
        if not path.exists():
            create_lodgings_file()

        lodgings = load_lodgings()

        if len(lodgings) == 0:
            print("No lodgings available.")
            return

        display_lodgings(lodgings)

    except Exception as e:
        print("Error:", e)


def search_lodgings():
    try:
        if not path.exists():
            create_lodgings_file()

        lodgings = load_lodgings()

        keyword = input("\nEnter search keyword: ").lower().strip()

        if keyword == "":
            print("Search cannot be empty.")
            return

        results = []

        for lodge in lodgings:
            if keyword in lodge[1].lower() or keyword in lodge[4].lower():
                results.append(lodge)

        if results:
            print("\nSearch Results:")
            display_lodgings(results)
        else:
            print("\nNo matching lodgings found.")

    except Exception as e:
        print("Error:", e)