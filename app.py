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