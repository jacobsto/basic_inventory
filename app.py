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