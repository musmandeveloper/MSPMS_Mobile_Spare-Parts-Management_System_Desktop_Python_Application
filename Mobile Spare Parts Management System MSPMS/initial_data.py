



# Initial Data for Databases



# Note: Use and Run this file only during Development and Testing, Remove this file from project before Deployment.
# Also delete data_inerted.txt file which created as running this file.



# initial_data.py


from database import get_mysql_connection, get_sqlite_connection

def insert_initial_data():

    # Define the initial data

    roles = [
        (1, 'Admin', 'a  admin, manager or owner of the shop/organization'),
        (2, 'Salesman', 'a worker on the shop/organization'),
    ]
    
    permissions = [
        (1, 'manage roles', 'create,read,update,delete roles'),
        (2, 'manage permissions', 'create,read,update,delete permissions'),
        (3, 'manage authorizations', 'create,read,update,delete authorizations'),
        (4, 'manage users', 'create,read,update,delete users'),
        (5, 'manage spare-parts', 'create,read,update,delete spare-parts'),
        (6, 'record,view and update transactions', 'create,read,update transactions'),
        (7, 'delete transactions ', 'delete transactions'),
    ] 

    authorizations = [
        (1, 1, 1),
        (2, 1, 2),
        (3, 1, 3),
        (4, 1, 4),
        (5, 1, 5),
        (6, 1, 6),
        (7, 1, 7),
        (8, 2, 6),
    ] 

    users = [
        (1, 'admin', 'Admin@123', '1', 'Admin Full Name', 'xxxxxxxxxxxxxx', 'Male', '30-09-2000', 'Full Address'),
        (2, 'salesman', 'Salesman@123', '2', 'Salesman Full Name', 'xxxxxxxxxxxxxx', 'Male', '30-09-2000', 'Full Address'),
    ]

    spare_parts = [
        (1, 'Brake Pad', 'Brakes', 150.00, 200.00),
        (2, 'Air Filter', 'Filters', 75.00, 120.00)
    ]

    transactions = []

    transaction_items = []


    # Insert data into SQLite
    print("Now Inserting initial data into connected SQLite Database")
    conn_sqlite = get_sqlite_connection()
    if conn_sqlite:
        try:
            # Enable foreign key constraint enforcement
            conn_sqlite.execute('PRAGMA foreign_keys = ON;')
            
            cursor_sqlite = conn_sqlite.cursor()
            cursor_sqlite.execute("DELETE FROM roles")
            cursor_sqlite.execute("DELETE FROM permissions")
            cursor_sqlite.execute("DELETE FROM authorizations")
            cursor_sqlite.execute("DELETE FROM users")
            cursor_sqlite.execute("DELETE FROM spare_parts")
            cursor_sqlite.execute("DELETE FROM transactions")
            cursor_sqlite.execute("DELETE FROM transaction_items")

            cursor_sqlite.executemany("INSERT INTO roles (id, name, description) VALUES (?, ?, ?)", roles)
            cursor_sqlite.executemany("INSERT INTO permissions (id, name, description) VALUES (?, ?, ?)", permissions)
            cursor_sqlite.executemany("INSERT INTO authorizations (id, role_id, permission_id) VALUES (?, ?, ?)", authorizations)
            cursor_sqlite.executemany("INSERT INTO users (id, username, password, role_id, full_name, cnic, gender, dob, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", users)
            cursor_sqlite.executemany("INSERT INTO spare_parts (id, name, category, purchase_price, sale_price) VALUES (?, ?, ?, ?, ?)", spare_parts)
            cursor_sqlite.executemany("INSERT INTO transactions (id, date, time, type, user_id, grand_total_price) VALUES (?, ?, ?, ?, ?, ?)", transactions)
            cursor_sqlite.executemany("INSERT INTO transaction_items (id, transaction_id, spare_part_id, spare_part_name, spare_part_category, quantity, purchase_price, sale_price, total_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", transaction_items)
            conn_sqlite.commit()
            conn_sqlite.close()
            print("Initial data successfully inserted into your connected SQLite Database")
            with open('initial_data_inserted.txt', 'a') as f:
                f.write("Successfully Initial Data inserted into your connected SQLite Database\n")
        except Exception as sqlite_error:
            print(f"Error inserting data into your connected SQLite Database: {sqlite_error}")
            with open('initial_data_inserted.txt', 'a') as f:
                f.write(f"Error inserting data your connected SQLite Database: {sqlite_error}\n")
            conn_sqlite.close()
    else:
        print("Error connecting to SQLite")


    # Insert data into MySQL
    print("Now Inserting initial data into connected MySQL Database")
    conn_mysql = get_mysql_connection()
    if conn_mysql:
        try:
            cursor_mysql = conn_mysql.cursor()
            # Below specify the name of your MySQL database you have to insert intial data
            cursor_mysql.execute("USE mspms_mysql_db")  
            cursor_mysql.execute("DELETE FROM roles")
            cursor_mysql.execute("DELETE FROM permissions")
            cursor_mysql.execute("DELETE FROM authorizations")
            cursor_mysql.execute("DELETE FROM users")
            cursor_mysql.execute("DELETE FROM spare_parts")
            cursor_mysql.execute("DELETE FROM transactions")
            cursor_mysql.execute("DELETE FROM transaction_items")
            
            cursor_mysql.executemany("INSERT INTO roles (id, name, description) VALUES (%s, %s, %s)", roles)
            cursor_mysql.executemany("INSERT INTO permissions (id, name, description) VALUES (%s, %s, %s)", permissions)
            cursor_mysql.executemany("INSERT INTO authorizations (id, role_id, permission_id) VALUES (%s, %s, %s)", authorizations)
            cursor_mysql.executemany("INSERT INTO users (id, username, password, role_id, full_name, cnic, gender, dob, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", users)
            cursor_mysql.executemany("INSERT INTO spare_parts (id, name, category, purchase_price, sale_price) VALUES (%s, %s, %s, %s, %s)", spare_parts)
            cursor_mysql.executemany("INSERT INTO transactions (id, date, time, type, user_id, grand_total_price) VALUES (%s, %s, %s, %s, %s, %s)", transactions)
            cursor_mysql.executemany("INSERT INTO transaction_items (id, transaction_id, spare_part_id, spare_part_name, spare_part_category, quantity, purchase_price, sale_price, total_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", transaction_items)
            conn_mysql.commit()
            conn_mysql.close()
            print("Initial data successfully inserted into your connected MySQL Database")
            with open('initial_data_inserted.txt', 'a') as f:
                f.write("Successfully Initial data inserted into your connected MySQL Database\n")
        except Exception as mysql_error:
            print(f"Error inserting data into your connected MySQL Database: {mysql_error}")
            with open('initial_data_inserted.txt', 'a') as f:
                f.write(f"Error inserting data into your connected MySQL Database: {mysql_error}\n")
            conn_mysql.close()



if __name__ == "__main__":
    insert_initial_data()



