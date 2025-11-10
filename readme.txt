Fylde Aero - Inventory Management Tool

ABOUT THE PROGRAM

The tool is used through a text interface called the command line.

This program allows you to:
• View items in the inventory
• Add new items to the inventory
• Delete items from the inventory
• Manage other users (Admin only)

BEFORE YOU START

You will need:
• A computer running Windows 11 (tested), also works on macOS/Linux
• Python 3 installed on the computer
• The file "app.py" saved on the computer - obtained by right clicking the "Inventory System" ZIP file and clicking Extract All

STARTING THE PROGRAM

Follow these steps:
Open the folder where the program is saved (likely called "Inventory System")
Right click inside the folder
Select the option "Open in terminal"
Type the exact message in the window that opens and press enter:

  python app.py

LOGGING IN

You will be asked for a username and password.
As this is the first time running the program, the only account will be the admin account.
Use these exact credentials:
Username: admin
Password: admin123

This is the default admin account.

MENUS

Unprivileged

1. List items
2. Quit

Privileged

1. Add item
2. List items
3. Delete item
4. Quit

Admin

1. Add item
2. List item
3. Delete item
4. Manage users
5. Quit

ADDING AN ITEM

Choose "Add item" from the menu
Type the name of the item you're adding
Type the quantity of the item (as a whole number)
Type the unit (e.g. pcs)
The item will be saved to the inventory CSV

You will see item added when it has been successful or an error message if a field has incorrectly been entered.

LISTING ALL ITEMS

Choose "List items" from the menu
A table will appear showing Item ID, Item Name, Quantity, Unit, Added By, Date Added.
You will then be taken back to the menu

DELETING AN ITEM

Choose "Delete item" from the menu
The app will list the items
Type the ID of the item you want to delete
If the ID exists the item will be deleted from the inventory
A confirmation message will appear
If the ID does not exist an error message will say so

ADMIN USER MANAGEMENT

Admins can: 
• List all users
• Add new users
• Change user roles

The app will prompt the admin to enter the information needed.

DATA STORAGE

data.csv - holds the inventory data with headers: item_id, item_name, quantity, unit, added_by, date_added.
users.csv - holds the users data with headers: username, password, role.

Deleting these files will erase all data stored on the files.

• If the files are deleted, new CSVs will be created next time the program is run.

TROUBLESHOOTING

Admin
Common errors:

• When adding a new user, if the username already exists, the user will not be added.
• When changing the user role, if the role or username is incorrect the role will not be updated.
• CSV missing or corrupted - delete the file and re-run the program.

Other Users

• Login Fails - Check spelling and cases.
• Quantity errors - Integers must be greater than 0 and not written as "one".

ENDING THE PROGRAM

Choose quit from the menu.
All data added to the CSVs are automatically saved.