import csv
from pathlib import Path

# File path
filepath = 'files/users.csv'
path = Path(filepath)


def create_csv():
    Path("files").mkdir(exist_ok=True)  # ensure folder exists

    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'password', 'role'])


def load_csv():
    rows = []
    with open(filepath, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # skip header

        for row in csvreader:
            rows.append(row)

    return rows


def register():
    while True:
        print("\n=== REGISTER ===")

        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        # ✅ Validation
        if username == "" or password == "":
            print("Fields cannot be empty.\n")
            continue

        try:
            if path.exists():
                rows = load_csv()

                for row in rows:
                    if row[0] == username:
                        print("Username already exists.\n")
                        return

                # Save user
                with open(filepath, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([username, password, "user"])

                print("Account created successfully!\n")
                return

            else:
                create_csv()
                print("System initialized. Please register again.\n")

        except Exception as e:
            print("Error:", e)


def login():
    while True:
        print("\n=== LOGIN ===")

        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        if username == "" or password == "":
            print("Fields cannot be empty.\n")
            continue

        try:
            if path.exists():
                rows = load_csv()

                for row in rows:
                    if row[0] == username and row[1] == password:
                        print("Login successful!\n")
                        return username, row[2]  # return role

                print("Invalid credentials.\n")

            else:
                create_csv()
                print("No users found. Please register first.\n")

        except Exception as e:
            print("Error:", e)