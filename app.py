import csv, os #Load CSV module, Load OS module
from datetime import datetime # Imports datetime class allowing for timestamps

CSV_PATH = "data.csv" #File name for inventory csv
COLUMNS = ["item_id","item_name","quantity","unit","added_by","date_added"] #Headers for columns

USERS_CSV = "users.csv" #File name for users csv
USER_COLUMNS = ["username","password","role"] #Headers for columns

def ensure_csv_ready():
    if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0: #Checks if CSV exists
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f: #Opens file in write mode
            csv.writer(f).writerow(COLUMNS) #Writes column headers into the first line

def ensure_users_ready():
    """Ensures users.csv exists with at least one admin account"""
    if not os.path.exists(USERS_CSV) or os.path.getsize(USERS_CSV) == 0: #Checks if CSV exists
        with open(USERS_CSV, "w", newline="", encoding="utf-8") as f: #Opens file in write mode
            writer = csv.DictWriter(f, fieldnames=USER_COLUMNS) #Writes column headers into the first line
            writer.writeheader()            
            writer.writerow({"username": "admin", "password": "admin123", "role": "admin"}) #Default admin account

def read_all():
    ensure_csv_ready() #Make sure the csv exists before opening it
    with open(CSV_PATH, "r", newline="", encoding="utf-8") as f: #Open the file in read mode
        return list (csv.DictReader(f)) #Read each row as a dictionary
    
def read_users():
    """Read all user accounts from users.csv."""
    ensure_users_ready() #Make sure the csv exists before opening it
    with open(USERS_CSV, "r", newline="", encoding="utf-8") as f: #Open the file in read mode
        return list(csv.DictReader(f)) #Read each row as a dictionary
    
def write_users(users):
    """Overwrite users.csv with new user data."""
    with open(USERS_CSV, "w", newline="", encoding="utf-8") as f: #Opens csv in write mode replacing existing contents
        writer = csv.DictWriter(f, fieldnames=USER_COLUMNS) #Sets up a writer
        writer.writeheader() #Writes column headers
        writer.writerows(users) #Writes users back into file

def next_item_id(): #Generates the next available unique item ID for new inventory ID entries.
    rows = read_all()
    max_id = 0
    for r in rows:
        try:
            max_id = max(max_id, int(r.get("item_id", "0") or "0"))
        except ValueError:
            pass
    return str(max_id + 1)

def append_row(row): #Adds a new record to the inventory csv ensuring the file exists and is formatted first.
    ensure_csv_ready()
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f,fieldnames=COLUMNS)
        w.writerow(row)

def add_item(added_by): #Create a new inventory record with validated data and append it to the csv.
    print("\n--- Add Item ---")
    name = input ("Item name: ").strip()
    while name == "":
        print("Item name cannot be empty.")
        name = input("Item name: ").strip()
    qty_text = input ("Quantity (whole number): ").strip()
    unit = input("Unit (e.g. pcs): ").strip() or "pcs"
    try:
        qty = int(qty_text)
        if qty <= 0:
            print ("Quantity must be greater than 0.\n")
            return
    except ValueError:
        print ("Quantity must be a whole number.\n")
        return
    row ={
        "item_id":next_item_id(),
        "item_name":name,
        "quantity":str(qty),
        "unit":unit,
        "added_by":added_by,
        "date_added":datetime.now().strftime("%Y-%m-%d"),
    }
    append_row(row)
    print("Item added.\n")

def list_items(): #Display all record in the inventory in a readable format.
    print("\n------------------------ All Items ------------------------")
    rows = read_all()
    if not rows:
        print("(no items)\n")
        return
    print(f"{'ID':<4} {'Name':<16}{'Qty':<5} {'Unit':<8} {'Added By':<10} {'Date':<12}")
    print("-" * 59)
    for r in rows:
        print(f"{r.get('item_id',''):<4} "
          f"{r.get('item_name',''):<15} "
          f"{r.get('quantity',''):<5} "
          f"{r.get('unit',''):<8} "
          f"{r.get('added_by',''):<10} "
          f"{r.get('date_added',''):<12}")
        
def delete_item(): # Remove an item from the inventory by entering the ID for authorised users.
    print("\n--- Delete Item ---")
    rows = read_all()
    if not rows:
        print("No items to delete.\n")
        return

    list_items()  # show current items
    item_id = input("Enter the ID of the item to delete: ").strip()

    # Filter out the row with the matching ID
    updated_rows = [r for r in rows if r.get("item_id") != item_id]

    if len(updated_rows) == len(rows):
        print(f"No item found with ID {item_id}.\n")
        return

    # Overwrite CSV with the updated list
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(updated_rows)
    print(f"Item with ID {item_id} deleted successfully.\n")

def manage_users(): #Allow the admin to view and manage user accounts.
    """Allow admin to view and edit user access levels."""
    while True:
        print("\n--- User Management ---")
        print("1) List users")
        print("2) Add user")
        print("3) Change user role")
        print("4) Back to main menu")

        choice = input("Choose (1/2/3/4): ").strip()
        users = read_users()

        if choice == "1":
            print(f"\n{'Username':<15}{'Role':<12}")
            print("-" * 27)
            for u in users:
                print(f"{u['username']:<15}{u['role']:<12}")

        elif choice == "2":
            new_user = input("New username: ").strip()
            while new_user == "":
                print("Username cannot be empty.")
                new_user = input("New username: ").strip()
            if any(u["username"] == new_user for u in users):
                print("User already exists.\n")
                continue
            new_pass = input("Password: ").strip()
            while new_pass == "":
                print("Password cannot be empty.")
                new_pass = input("Password: ").strip()
            new_role = input("Role (admin/privileged/unprivileged): ").strip().lower()
            if new_role not in ["admin", "privileged", "unprivileged"]:
                print("Invalid role.\n")
                continue
            users.append({"username": new_user, "password": new_pass, "role": new_role})
            write_users(users)
            print("User added successfully.\n")

        elif choice == "3":
            username = input("Username to modify: ").strip()
            user = next((u for u in users if u["username"] == username), None)
            if not user:
                print("User not found.\n")
                continue
            new_role = input("New role (admin/privileged/unprivileged): ").strip().lower()
            if new_role not in ["admin", "privileged", "unprivileged"]:
                print("Invalid role.\n")
                continue
            user["role"] = new_role
            write_users(users)
            print("Role updated successfully.\n")

        elif choice == "4":
            break
        else:
            print("Invalid choice.\n")

def login(): #Authenticate the user and return their identity and role.
    """Prompt for login until successful. Returns (username, role)."""
    users = read_users()
    while True:
        print("\n--- Login ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        for u in users:
            if u["username"] == username and u["password"] == password:
                print(f"\nWelcome, {username}! Role: {u['role'].capitalize()}\n")
                return u["username"], u["role"]

        print("Invalid username or password. Please try again.\n")

def main(): #Main menu, prepare files, authenticate and send user to the correct menu.
    ensure_csv_ready()
    ensure_users_ready()

    username, role = login()

    if role == "unprivileged":
        # Read-only mode
        while True:
            print("View-Only Menu")
            print("1) List items")
            print("2) Quit")
            choice = input("Choose (1/2): ").strip()
            if choice == "1":
                list_items()
            elif choice == "2":
                print("Goodbye!")
                break
            else:
                print("Unknown option.\n")

    elif role == "privileged":
        # Normal inventory access
        while True:
            print("Basic Inventory")
            print("1) Add item")
            print("2) List items")
            print("3) Delete item")
            print("4) Quit")
            choice = input("Choose (1/2/3/4): ").strip()

            if choice == "1":
                add_item(username)
            elif choice == "2":
                list_items()
            elif choice == "3":
                delete_item()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Unknown option.\n")

    elif role == "admin":
        # Full control
        while True:
            print("Admin Menu")
            print("1) Add item")
            print("2) List items")
            print("3) Delete item")
            print("4) Manage users")
            print("5) Quit")
            choice = input("Choose (1/2/3/4/5): ").strip()

            if choice == "1":
                add_item(username)
            elif choice == "2":
                list_items()
            elif choice == "3":
                delete_item()
            elif choice == "4":
                manage_users()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Unknown option.\n")

if __name__ == "__main__":
    main()