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