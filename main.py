from auth import verify_password
from database import (
    create_entry,
    get_entries,
    get_user,
    init_db,
    register_user,
)


def main():
    # 1. Ensure database tables exist right when the app starts
    init_db()

    # 2. Track who is currently logged in (None means nobody is logged in)
    current_user = None

    print("==============================")
    print("   Welcome to Your Journal   ")
    print("==============================")

    # 3. The main application loop keeps the program running
    while True:
        if current_user is None:
            # --- LOGGED OUT MENU ---
            print("\n1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Choose an option (1-3): ").strip()

            if choice == "1":
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()
                if register_user(username, password):
                    print("Registration successful! You can now log in.")
                else:
                    print("Registration failed. Try a different username.")

            elif choice == "2":
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()

                user_record = get_user(username)
                if user_record:
                    user_id, db_username, db_hash = user_record
                    if verify_password(password, db_hash):
                        current_user = (user_id, db_username)
                        print(f"\nWelcome back, {db_username}!")
                    else:
                        print("Incorrect password.")
                else:
                    print("Username not found.")

            elif choice == "3":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

        else:
            # --- LOGGED IN MENU ---
            user_id, username = current_user
            print(f"\n--- Journal Menu ({username}) ---")
            print("1. View Entries")
            print("2. Write New Entry")
            print("3. Logout")
            choice = input("Choose an option (1-3): ").strip()

            if choice == "1":
                entries = get_entries(user_id)
                if not entries:
                    print("\nNo journal entries found yet.")
                else:
                    print(f"\n--- Your Journal Entries ({len(entries)}) ---")
                    for entry_id, title, content, created_at in entries:
                        print(f"\n[{created_at}] {title}")
                        print("-" * 40)
                        print(content)
                        print("-" * 40)

            elif choice == "2":
                title = input("Entry title: ").strip()
                content = input("Entry content: ").strip()
                if title and content:
                    create_entry(user_id, title, content)
                    print("Entry saved successfully!")
                else:
                    print("Title and content cannot be empty.")

            elif choice == "3":
                print(f"Logged out {username}.")
                current_user = None

            else:
                print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()