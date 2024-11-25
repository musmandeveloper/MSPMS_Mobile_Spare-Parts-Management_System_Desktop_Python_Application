


# Data Synchronization b/w SQLit and MySQL both databses when internet available



# sync.py

from db import get_sqlite_connection, get_mysql_connection

def sync_sqlite_to_mysql():
    sqlite_conn = get_sqlite_connection()
    mysql_conn = get_mysql_connection()

    sqlite_cursor = sqlite_conn.cursor()
    mysql_cursor = mysql_conn.cursor()

    # Fetch data from SQLite
    sqlite_cursor.execute("SELECT * FROM users")
    users = sqlite_cursor.fetchall()

    sqlite_cursor.execute("SELECT * FROM parts")
    parts = sqlite_cursor.fetchall()

    sqlite_cursor.execute("SELECT * FROM transactions")
    transactions = sqlite_cursor.fetchall()

    # Insert data into MySQL
    mysql_cursor.executemany("INSERT INTO users (id, username, password, role) VALUES (%s, %s, %s, %s)", users)
    mysql_cursor.executemany("INSERT INTO parts (id, name, category, quantity, price) VALUES (%s, %s, %s, %s, %s)", parts)
    mysql_cursor.executemany("INSERT INTO transactions (id, part_id, type, quantity, date) VALUES (%s, %s, %s, %s, %s)", transactions)

    mysql_conn.commit()

    sqlite_conn.close()
    mysql_conn.close()

if __name__ == "__main__":
    sync_sqlite_to_mysql()






