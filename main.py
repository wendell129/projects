from waste_management import (
    initialize_files,
    register_user,
    login_user,
    record_waste,
    view_user_data,
)

def main():
    initialize_files()
    print("\n----------------------------------------------")
    print("Welcome to Waste to Cash Management System!")
    print("Let's save Environment!")
    print("----------------------------------------------")
    current_user = None

    while True:
        print("\n---------****************----------")
        print(" MAIN MENU:")
        print("1. Register a new user")
        print("2. Login")
        print("3. Record Waste Collection")
        print("4. View Balance and Transactions")
        print("5. Logout")
        print("6. Exit the app")
        print("---------****************----------")

        try:
            choice = input("Choose an option (1-6): ")

            if choice == "1":
                print("\n-------------------")
                username = input("Enter a unique username: ")
                registered_user = register_user(username)
                if registered_user: 
                    current_user = registered_user
                print("-------------------")

            elif choice == "2":
                print("\n-------------------")
                username = input("Enter your username: ")
                if login_user(username):
                    current_user = username
                print("-------------------")

            elif choice == "3":
                if current_user is None:
                    print("Please log in first.")
                    continue
                print("\n-------------------")
                waste_type = input("Enter waste type (plastic bottle, metal can, glass bottle, paper, electronic waste): ").lower()
                try:
                    weight_kg = float(input("Enter weight in kg: "))
                    record_waste(current_user, waste_type, weight_kg)
                except ValueError:
                    print("Invalid weight entered. Please enter a numeric value.")
                print("-------------------")

            elif choice == "4":
                if current_user is None:
                    print("Please log in first.")
                    continue
                print("\n-------------------")
                view_user_data(current_user)
                print("-------------------")

            elif choice == "5":
                if current_user:
                    print(f"User '{current_user}' has been logged out.")
                    current_user = None
                else:
                    print("No user is currently logged in.")

            elif choice == "6":
                print("\nThank you for using the Waste-to-Cash Management System.")
                print("You just helped our environment!")
                print("COME BACK AGAIN, GOODBYE!")
                break

            else:
                print("Invalid option. Please try again.")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
