import csv
from pathlib import Path

# File path
filepath = 'files/users.csv'
path = Path(filepath)


# =========================
# CREATE CSV
# =========================
def create_csv():
    Path("files").mkdir(exist_ok=True)

    # Create only if it doesn't exist or is empty
    if path.exists():
        return

    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'password', 'role'])


# =========================
# LOAD CSV (SAFE)
# =========================
def load_csv():
    try:
        if not path.exists():
            return []

        with open(filepath, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader, None)  # safe skip header

            return [row for row in csvreader if len(row) >= 3]

    except Exception:
        return []


# =========================
# REGISTER
# =========================
def register():
    while True:
        print("\n=== REGISTER ===")

        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        # Validation
        if not username or not password:
            print("Fields cannot be empty.\n")
            continue

        if len(username) < 3:
            print("Username must be at least 3 characters.\n")
            continue

        if len(password) < 4:
            print("Password must be at least 4 characters.\n")
            continue

        try:
            create_csv()
            rows = load_csv()

            # check duplicates
            for row in rows:
                if row[0] == username:
                    print("Username already exists.\n")
                    return

            # save user
            with open(filepath, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, password, "user"])

            print("Account created successfully!\n")
            return

        except PermissionError:
            print("File is currently open. Close it and try again.\n")

        except Exception as e:
            print("Unexpected error:", e)


# =========================
# LOGIN
# =========================
def login():
    while True:
        print("\n=== LOGIN ===")

        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        if not username or not password:
            print("Fields cannot be empty.\n")
            continue

        try:
            create_csv()
            rows = load_csv()

            for row in rows:
                if row[0] == username and row[1] == password:
                    print("Login successful!\n")
                    return username, row[2]  # role

            print("Invalid credentials.\n")

        except Exception as e:
            print("Error:", e)