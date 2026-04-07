import sys
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


def main():
    show_logo()
    print("Welcome to RESERVA Booking System\n")

    while True:
        print("== MAIN MENU ==")
        print("1. Log In")
        print("2. Register")
        print("3. Exit\n")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            print("\nLog In feature coming soon...\n")
            break
        elif choice == "2":
            print("\nRegister Feature coming soon...\n")
            break
        elif choice == "3":
            print("\nExiting system...\n")
            break
        else:
            print("\nInvalid input. Please try again.\n")
        
if __name__ == "__main__":
    main()