import sys
from auth import login, register
from lodgings import view_lodgings, search_lodgings
from reservations import make_reservation, view_my_bookings, cancel_booking
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


def customer_menu(username):
    while True:
        print('\n=== CUSTOMER MENU ===')
        print('1. Browse Hotels')
        print('2. Search Lodgings')
        print('3. Make Reservation')
        print('4. View My Bookings')
        print('5. Cancel Booking')
        print('6. Logout')

        choice = input('Enter choice: ').strip()

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
            break

        else:
            print('Invalid choice.')


def main():
    show_logo()
    while True:
        print('\n1. Log In')
        print('2. Register')
        print('3. Exit')

        choice = input('Enter choice: ').strip()

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
            break


if __name__ == '__main__':
    main()