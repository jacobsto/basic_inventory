import csv, os #Load CSV module, Load OS module
from datetime import datetime # Imports datetime class allowing for timestamps

CSV_PATH = "data.csv" #File name for inventory csv
COLUMNS = ["item_id","item_name","quantity","unit","added_by","date_added"] #Headers for columns