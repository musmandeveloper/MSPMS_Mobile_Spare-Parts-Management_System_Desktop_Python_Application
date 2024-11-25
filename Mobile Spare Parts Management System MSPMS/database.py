



# Databases Connection and Tables Schemas


import os
import sys
import sqlite3
import mysql.connector
from mysql.connector import Error
import time


# SQLite connection parameters
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sqlite_db_folder = os.path.join(BASE_DIR, 'local_database')
if not os.path.exists(sqlite_db_folder):
    os.makedirs(sqlite_db_folder)
sqlite_database = 'local_database/mspms_sqlite_db.sqlite'

# MySQL connection parameters
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
}
mysql_database = 'mspms_mysql_db'


def get_sqlite_connection():
    database_exists = os.path.exists(sqlite_database)
    try:
        conn = sqlite3.connect(sqlite_database)
        print("SQLite connection established successfully.")
        if not database_exists:
            print(f"SQLite Database mspms_sqlite_db.sqlite created successfully.")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite: {e}")
        return None

def get_mysql_connection():
    try:
        conn = mysql.connector.connect(**mysql_config)
        print("MySQL connection established successfully")
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_mysql_database():
    conn = get_mysql_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {mysql_database}")
            print(f"MySQL Database {mysql_database} created successfully bcz it was not existed before.")
            conn.commit()
        except Error as e:
            print(f"Error creating database: {e}")
        finally:
            cursor.close()
            conn.close()



def create_tables():
    # SQLite database table creation
    try:
        sqlite_conn = get_sqlite_connection()

        if sqlite_conn:
            sqlite_cursor = sqlite_conn.cursor()

            # SQLite SQL statements
            sqlite_tables = [
                # Add all your SQLite CREATE TABLE statements here
                """
                CREATE TABLE IF NOT EXISTS roles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP                        
                );      
                """,
                """
                CREATE TABLE IF NOT EXISTS permissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP                        
                );       
                """,
                """
                CREATE TABLE IF NOT EXISTS authorizations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role_id INTEGER NOT NULL,
                    permission_id INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
                    FOREIGN KEY (role_id) REFERENCES roles(id),
                    FOREIGN KEY (permission_id) REFERENCES permissions(id)                      
                );       
                """,
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    role_id INTEGER NOT NULL,
                    full_name TEXT NOT NULL,
                    cnic TEXT NULL,
                    gender TEXT NULL,
                    dob DATE NULL,
                    address TEXT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,            
                    FOREIGN KEY (role_id) REFERENCES roles(id)                    
                );       
                """,
                """
                CREATE TABLE IF NOT EXISTS spare_parts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    purchase_price REAL NOT NULL,
                    sale_price REAL NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP                        
                );       
                """,
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE NOT NULL,
                    time TIME NOT NULL,
                    type TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    grand_total_price REAL NOT NULL,
                    paid_price REAL NOT NULL,
                    balance_price REAL NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,            
                    FOREIGN KEY (user_id) REFERENCES users(id)                        
                );       
                """,
                """
                CREATE TABLE IF NOT EXISTS transaction_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_id INTEGER NOT NULL,
                    spare_part_id INTEGER NOT NULL,
                    spare_part_name TEXT NOT NULL,
                    spare_part_category TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    purchase_price REAL NOT NULL,
                    sale_price REAL NOT NULL,
                    total_price REAL NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,            
                    FOREIGN KEY (transaction_id) REFERENCES transactions(id),
                    FOREIGN KEY (spare_part_id) REFERENCES spare_parts(id)                       
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE NOT NULL,
                    report_name TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
                """,
                # Add other table creation queries for SQLite here...
            ]

            # Execute the table creation statements for SQLite
            for table_sql in sqlite_tables:
                sqlite_cursor.execute(table_sql)

            sqlite_conn.commit()
            print(f"All tables created successfully in SQLite database.")
        else:
            print(f"SQLite connection failed, skipping SQLite table creation.")
    
    except sqlite3.Error as e:
        print(f"Error creating SQLite database or tables: {e}")
    
    finally:
        if sqlite_cursor:
            sqlite_cursor.close()
        if sqlite_conn:
            sqlite_conn.close()

    # MySQL database table creation
    mysql_conn = None
    mysql_cursor = None
    try:
        create_mysql_database()
        mysql_config_with_db = mysql_config.copy()
        mysql_config_with_db['database'] = mysql_database
        mysql_conn = mysql.connector.connect(**mysql_config_with_db)

        if mysql_conn.is_connected():
            mysql_cursor = mysql_conn.cursor()

            # MySQL SQL statements
            mysql_tables = [
                # Add all your MySQL CREATE TABLE statements here
                """
                CREATE TABLE IF NOT EXISTS roles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description VARCHAR(255) NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP                
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS permissions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description VARCHAR(255) NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP                
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS authorizations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    role_id INT NOT NULL,
                    permission_id INT NOT NULL,
                    FOREIGN KEY (role_id) REFERENCES roles(id),
                    FOREIGN KEY (permission_id) REFERENCES permissions(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP                
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role_id INT NOT NULL,
                    full_name VARCHAR(255) NOT NULL,
                    cnic VARCHAR(255) NULL,
                    gender VARCHAR(50) NULL,
                    dob DATE NULL,
                    address VARCHAR(255) NULL,
                    FOREIGN KEY (role_id) REFERENCES roles(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP                
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS spare_parts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    category VARCHAR(255) NOT NULL,
                    purchase_price DECIMAL(10, 2) NOT NULL,
                    sale_price DECIMAL(10, 2) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP                
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date DATE NOT NULL,
                    time TIME NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    user_id INT NOT NULL,
                    grand_total_price DECIMAL(10, 2) NOT NULL,
                    paid_price DECIMAL(10, 2) NOT NULL,
                    balance_price DECIMAL(10, 2) NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP                
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS transaction_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    transaction_id INT NOT NULL,
                    spare_part_id INT NOT NULL,
                    spare_part_name VARCHAR(255) NOT NULL,
                    spare_part_category VARCHAR(255) NOT NULL,
                    quantity INT NOT NULL,
                    purchase_price DECIMAL(10, 2) NOT NULL,
                    sale_price DECIMAL(10, 2) NOT NULL,
                    total_price DECIMAL(10, 2) NOT NULL,
                    FOREIGN KEY (transaction_id) REFERENCES transactions(id),
                    FOREIGN KEY (spare_part_id) REFERENCES spare_parts(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS reports (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date DATE NOT NULL,
                    report_name VARCHAR(255) NOT NULL,
                    file_data LONGBLOB NOT NULL,
                    file_path VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                );
                """,
                # Add other table creation queries for MySQL here...
            ]

            # Execute the table creation statements for MySQL
            for table_sql in mysql_tables:
                mysql_cursor.execute(table_sql)

            mysql_conn.commit()
            print(f"All tables created successfully in MySQL database.")
        else:
            print(f"Failed to connect to MySQL.")
    
    except Error as e:
        print(f"Error creating MySQL database or tables: {e}")

    finally:
        if mysql_cursor:
            mysql_cursor.close()
        if mysql_conn:
            mysql_conn.close()



if __name__ == "__main__":
    create_tables()
    time.sleep(5)  # Keep the window open till for 5 seconds


