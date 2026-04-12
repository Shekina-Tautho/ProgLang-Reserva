import sys
from auth import login, register

sys.stdout.reconfigure(encoding='utf-8')


def show_logo():
    print(r"""
██████╗ ███████╗███████╗███████╗██████╗ ██╗   ██╗ █████╗ 
██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗██║   ██║██╔══██╗
██████╔╝█████╗  ███████╗█████╗  ██████╔╝██║   ██║███████║
██╔══██╗██╔══╝  ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══██║
██║  ██║███████╗███████║███████╗██║  ██║ ╚████╔╝ ██║  ██║
╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝
    """)


def customer_menu(username):
    while True:
        print("\n=== CUSTOMER MENU ===")
        print("1. View Lodgings")
        print("2. Search Lodgings")
        print("3. Make Reservation")
        print("4. View My Bookings")
        print("5. Cancel Booking")
        print("6. Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            print("\nViewing lodgings (feature coming next)...\n")
        elif choice == "2":
            print("\nSearch lodgings (coming soon)...\n")
        elif choice == "3":
            print("\nReservation feature coming soon...\n")
        elif choice == "4":
            print("\nView bookings coming soon...\n")
        elif choice == "5":
            print("\nCancel booking coming soon...\n")
        elif choice == "6":
            print("\nLogging out...\n")
            break
        else:
            print("\nInvalid choice. Try again.\n")


def main():
    show_logo()
    print("Welcome to RESERVA Booking System\n")

    while True:
        print("== MAIN MENU ==")
        print("1. Log In")
        print("2. Register")
        print("3. Exit\n")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            user = login()
            if user:
                print(f"\nWelcome, {user}!\n")
                customer_menu(user)

        elif choice == "2":
            register()

        elif choice == "3":
            print("\nExiting system...\n")
            break

        else:
            print("\nInvalid input. Please try again.\n")


if __name__ == "__main__":
    main()