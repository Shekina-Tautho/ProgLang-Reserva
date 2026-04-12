import csv
from pathlib import Path

filepath = 'files/lodgings.csv'
path = Path(filepath)


def create_lodgings_file():
    Path("files").mkdir(exist_ok=True)

    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["id", "name", "price", "capacity", "features"])

        writer.writerow([1, "Beach Resort", 2500, 4, "WiFi|Pool|Breakfast"])
        writer.writerow([2, "Mountain Cabin", 1800, 3, "Fireplace|View"])
        writer.writerow([3, "City Hotel", 3200, 2, "WiFi|Gym|Breakfast"])
        writer.writerow([4, "Budget Inn", 900, 2, "WiFi"])


def load_lodgings():
    lodgings = []

    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            lodgings.append(row)

    return lodgings


# ✅ CLEAN CARD DISPLAY
def display_lodgings(lodgings):
    print("\n=== AVAILABLE LODGINGS ===")

    for lodge in lodgings:
        print("=" * 40)
        print(f"ID: {lodge[0]}")
        print(f"Name: {lodge[1]}")
        print(f"Price: ₱{lodge[2]}")
        print(f"Capacity: {lodge[3]} persons")
        print(f"Features: {lodge[4].replace('|', ', ')}")
        print("=" * 40)


def view_lodgings():
    try:
        if not path.exists():
            create_lodgings_file()

        lodgings = load_lodgings()

        # 🔥 SORT OPTION
        print("\nSort by:")
        print("1. Default")
        print("2. Price (Low to High)")
        print("3. Price (High to Low)")
        choice = input("Enter choice: ").strip()

        if choice == "2":
            lodgings = sorted(lodgings, key=lambda x: int(x[2]))
        elif choice == "3":
            lodgings = sorted(lodgings, key=lambda x: int(x[2]), reverse=True)

        display_lodgings(lodgings)

    except Exception as e:
        print("Error:", e)


def search_lodgings():
    try:
        if not path.exists():
            create_lodgings_file()

        lodgings = load_lodgings()

        print("\n=== SEARCH LODGINGS ===")

        keyword = input("Keyword (name/features): ").lower().strip()
        min_price = input("Min price (optional): ").strip()
        max_price = input("Max price (optional): ").strip()
        capacity = input("Capacity (optional): ").strip()

        results = []

        for lodge in lodgings:
            price = int(lodge[2])
            cap = int(lodge[3])

            # 🔍 keyword filter
            if keyword and keyword not in lodge[1].lower() and keyword not in lodge[4].lower():
                continue

            # 💰 price filter
            if min_price and price < int(min_price):
                continue
            if max_price and price > int(max_price):
                continue

            # 👥 capacity filter
            if capacity and cap < int(capacity):
                continue

            results.append(lodge)

        if results:
            print("\nFiltered Results:")
            display_lodgings(results)
        else:
            print("\nNo matching lodgings found.")

    except Exception as e:
        print("Error:", e)