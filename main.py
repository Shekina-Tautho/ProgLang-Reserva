import sys
from auth import login, register
from lodgings import view_lodgings, search_lodgings
from reservations import make_reservation, view_my_bookings, cancel_booking, pay_for_booking
from admin import admin_menu

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

    print("\n            🏨 BOOKING SYSTEM")
    print("--------------------------------------------------")


def show_landing_menu():
    print("\n[1] Log In")
    print("[2] Register")
    print("[3] Exit")
    print("\n--------------------------------------------------")


def customer_menu(username):
    while True:
        print("\n" + "=" * 50)
        print(f"        👤 CUSTOMER DASHBOARD")
        print("=" * 50)
        print(f"Welcome, {username}")
        print("-" * 50)

        print("\n--- BOOKINGS ---")
        print("[1] Browse Hotels")
        print("[2] Search Lodgings")
        print("[3] Make Reservation")

        print("\n--- MANAGE ---")
        print("[4] View My Bookings")
        print("[5] Cancel Booking")
        print("[6] Pay for Booking")

        print("\n--- ACCOUNT ---")
        print("[7] Logout")

        print("\n" + "-" * 50)

        choice = input("Enter choice (1-7): ").strip()

        if choice == '1':
            result = view_lodgings()
            if result:
                hotel, room = result
                make_reservation(username, hotel, room)

        elif choice == '2':
            search_lodgings()

        elif choice == '3':
            make_reservation(username)

        elif choice == '4':
            view_my_bookings(username)

        elif choice == '5':
            cancel_booking(username)

        elif choice == '6':
            pay_for_booking(username)

        elif choice == '7':
            print("Logging out...\n")
            break

        else:
            print("❌ Invalid choice. Please select from the menu.")


def main():
    while True:
        show_logo()
        show_landing_menu()

        choice = input("Enter choice (1-3): ").strip()

        if choice == '1':
            result = login()
            if result:
                username, role = result

                if role == 'admin':
                    admin_menu()
                else:
                    customer_menu(username)

        elif choice == '2':
            register()

        elif choice == '3':
            print("\nThank you for using Reserva!\n")
            break

        else:
            print("❌ Invalid choice. Please select 1–3.")


if __name__ == '__main__':
    main()