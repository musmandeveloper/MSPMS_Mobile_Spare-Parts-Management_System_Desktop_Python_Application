



# Users controller, backend file 



# users.py

from database import get_sqlite_connection, get_mysql_connection



def fetch_users():
    """Fetch users from SQLite and MySQL databases"""
    
    fetched_users = []
    # Dictionary to store fetched roles based on 'username' as value against 'index' as key
    seen_users = {}  

    try:
        print("Now Fetching Users from your connected SQLite database")
        # SQLite Connection
        sqlite_conn = get_sqlite_connection()
        cursor_sqlite = sqlite_conn.cursor()

        # Fetch Users with Role Name instead of Role ID
        cursor_sqlite.execute("""
        SELECT u.id, u.username, u.password, r.name AS role_name, u.full_name, u.cnic, u.gender, u.dob, u.address
        FROM users u
        JOIN roles r ON u.role_id = r.id
        """)
        sqlite_users = cursor_sqlite.fetchall()
        sqlite_conn.close()
        if not sqlite_users:
            print("No users table data found in SQLite database.")
        else:    
            print("SQLite Users Table fetched data: ", sqlite_users)
            # Fetch Transactions Items
            for idx, user in enumerate(sqlite_users):
                print("Role tuple inside unpacking loop:", user)
                user_id, username, password, role, full_name, cnic, gender, dob, address = user
                if username in seen_users:
                    print(f"Skipping duplicate user with Username={username}  Bcz it's already fetched from MySQL")
                    continue  # Skip if already added
                # Store username of this sqlite fetched user in the seen_users dictionary
                seen_users[idx] = (username)
                # Append user to final un-duplicated fetched_users list
                fetched_users.append(user)
            print("Successfully fetched users from to your connected SQLite database")            
    except Exception as e:
        print(f"Error fetching users from SQLite: {e}")

    try:
        print("Now Fetching Users from your connected MySQL database")
        # MySQL Connection
        mysql_conn = get_mysql_connection()
        cursor_mysql = mysql_conn.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db")
        # Fetch Users
        cursor_mysql.execute(""" 
        SELECT u.id, u.username, u.password, r.name AS role_name, u.full_name, u.cnic, u.gender, u.dob, u.address
        FROM users u
        JOIN roles r ON u.role_id = r.id
        """)
        mysql_users = cursor_mysql.fetchall()
        mysql_conn.close()
        if not mysql_users:
            print("No users table data found in MySQL database.")
        else:    
            print("MySQL Users Table fetched data: ", mysql_users)
            for user in mysql_users:
                user_id, username, password, role, full_name, cnic, gender, dob, address = user
                # Check if this (user_name,permission_name) pair already exists in the seen_users dictionary
                if any((username) == un for un in seen_users.values()):
                    print(f"Skipping duplicate user with Username={username} fetched from MySQL as it's already fetched from SQLite")
                    continue  # Skip if duplicate
                # Append user to final un-duplicated fetched_users list
                fetched_users.append(user)
            print("Successfully fetched all users from your MySQL database")
    except Exception as e:
        print(f"Error fetching users from MySQL: {e}")

    # Final fetched_users without duplicates
    print("Final fetched all users (un-duplicated) from both databases = ", fetched_users)    
    return fetched_users 


    
def add_user(username, password, role_name, full_name, cnic, gender, dob, address):
    """Add a part to SQLite and MySQL databases"""
    
    try:
        # Add into SQLite
        print("Now Adding User to your connected SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # First, check if the received username already exists in the users table or not
        cursor_sqlite.execute(
            """
            SELECT id FROM users 
            WHERE username = ?
            """, (username,)
        )
        result = cursor_sqlite.fetchone()
        # Now getting role id of the received role_name
        cursor_sqlite.execute(
            """
            SELECT id FROM roles 
            WHERE name = ?
            """, (role_name,)
        )
        role_id = cursor_sqlite.fetchone()
        conn_sqlite.close()
        if not role_id:
            # If not, insert as the new role, and get its newly stored id
            # Open New Connection and Commit and Close it, before again open main Connection & using that 
            conn_sqlite = get_sqlite_connection()
            cursor_sqlite = conn_sqlite.cursor()
            dummy_role_description =  'no description'
            cursor_sqlite.execute(
                """
                INSERT INTO roles (name, description) 
                VALUES (?, ?)
                """, (role_name, dummy_role_description)
            )
            sqlite_role_id = cursor_sqlite.lastrowid  # Get the last inserted role ID
            conn_sqlite.commit()
            conn_sqlite.close()
        else:
            # If role with that "role_name' is existed in SQLite, so just get its role_id
            sqlite_role_id = role_id[0] if role_id else None
        # Again Open Connection
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()                
        if result:
            # If the user exists, get the existing user_id
            new_user_id = result[0]
            print(f"The user with name={name}, found in SQLite with ID={new_user_id}, No need to store again in SQLite")
        else:
            # If not, insert the new user
            cursor_sqlite.execute(
            """
            SELECT id FROM roles 
            WHERE name = ?
            """, (role_name,)
            )
            sqlite_role_id = cursor_sqlite.fetchone()
            sqlite_role_id = sqlite_role_id[0]
            cursor_sqlite.execute(
                """
                INSERT INTO users (username, password, role_id, full_name, cnic, gender, dob, address) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (username, password, sqlite_role_id, full_name, cnic, gender, dob, address)
            )
            new_user_id = cursor_sqlite.lastrowid  # Get the last inserted user ID  
            print(f"Successfully User added with id={new_user_id} into your connected SQLite database")
        conn_sqlite.commit()
        conn_sqlite.close()
    except Exception as e:
        print(f"Error adding user into your connected SQLite database: {e}")
    
    try:
        # Add into MySQL
        print("Now Adding User to your connected MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db")
        # First, check if the received username already exists in the users table or not
        cursor_mysql.execute(
            """
            SELECT id FROM users 
            WHERE username = %s
            """, (username,)
        )
        result = cursor_mysql.fetchone()
        # Now getting role id of the received role_name
        cursor_mysql.execute(
            """
            SELECT id FROM roles 
            WHERE name = %s
            """, (role_name,)
        )
        role_id = cursor_mysql.fetchone()
        conn_mysql.close()
        if not role_id:
            # If not, insert as the new role, and get its newly stored id
            # Open New Connection and Commit and Close it, before again open main Connection & using that 
            conn_mysql = get_mysql_connection()
            cursor_mysql = conn_mysql.cursor()
            # Below specify the name of your connected MySQL database
            cursor_mysql.execute("USE mspms_mysql_db") 
            dummy_role_description =  'no description'
            cursor_mysql.execute(
                """
                INSERT INTO roles (name, description) 
                VALUES (%s, %s)
                """, (role_name, dummy_role_description)
            )
            mysql_role_id = cursor_mysql.lastrowid  # Get the last inserted role ID
            conn_mysql.commit()
            conn_mysql.close()
        else:
            # If role with that "role_name' is existed in SQLite, so just get its role_id
            mysql_role_id = role_id[0] if role_id else None
        # Again Open Connection
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db")        
        if result:
            # If the user exists, get the existing user_id
            new_user_id = result[0]
            print(f"The user with name={name}, found in MySQL with ID={new_user_id}, No need to store it again")
        else:
            # If not, insert the new user
            cursor_mysql.execute(
            """
            SELECT id FROM roles 
            WHERE name = %s
            """, (role_name,)
            )
            role_id = cursor_mysql.fetchone()
            mysql_role_id = role_id[0]
            cursor_mysql.execute(
                """
                INSERT INTO users (username, password, role_id, full_name, cnic, gender, dob, address) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (username, password, mysql_role_id, full_name, cnic, gender, dob, address)
            )
            new_user_id = cursor_mysql.lastrowid  # Get the last inserted user ID  
            print(f"Successfully User added with id={new_user_id} into your connected MySQL database")        
        conn_mysql.commit()
        conn_mysql.close()
        print("Successfully User added into your connected MySQL database")
    except Exception as e:
        print(f"Error adding user into your connected MySQL database: {e}")



def update_user(id, username, password, role_name, full_name, cnic, gender, dob, address):
    """Update a user to SQLite and MySQL databases"""

    try:
        # Update into SQLite
        print("Updating User to your connected SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # First, check if the received username already exists in the users table or not
        cursor_sqlite.execute(
            """
            SELECT id FROM users 
            WHERE username = ?
            """, (username,)
        )
        result = cursor_sqlite.fetchone()
        # Now getting role id of the received role_name
        cursor_sqlite.execute(
            """
            SELECT id FROM roles 
            WHERE name = ?
            """, (role_name,)
        )
        role_id = cursor_sqlite.fetchone()
        conn_sqlite.close()
        if not role_id:
            # If not, insert as the new role, and get its newly stored id
            # Open New Connection and Commit and Close it, before again open main Connection & using that 
            conn_sqlite = get_sqlite_connection()
            cursor_sqlite = conn_sqlite.cursor()
            dummy_role_description =  'no description'
            cursor_sqlite.execute(
                """
                INSERT INTO roles (name, description) 
                VALUES (?, ?)
                """, (role_name, dummy_role_description)
            )
            sqlite_role_id = cursor_sqlite.lastrowid  # Get the last inserted role ID
            conn_sqlite.commit()
            conn_sqlite.close()
        else:
            # If role with that "role_name' is existed in SQLite, so just get its role_id
            sqlite_role_id = role_id[0] if role_id else None
        # Again Open Connection
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # Now either will update or insert as new
        if result:
            # If the user exists, get the existing user_id
            new_user_id = result[0]
            print(f"The user with username={username}, found in SQLite with ID={new_user_id}, So now just updating it with new data")
            # Update existing user
            cursor_sqlite.execute(
                """
                UPDATE users 
                SET username=?, password=?, role_id=?, full_name=?, cnic=?, gender=?, dob=?, address=?
                WHERE id = ?
                """, (username, password, sqlite_role_id, full_name, cnic, gender, dob, address, new_user_id)
            )
            print(f"Successfully User updated with id={new_user_id} into your connected SQLite database")
        else:
            # If not, insert as the new user
            cursor_sqlite.execute(
                """
                INSERT INTO users (username, password, role_id, full_name, cnic, gender, dob, address) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (username, password, sqlite_role_id, full_name, cnic, gender, dob, address)
            )
            new_user_id = cursor_sqlite.lastrowid  # Get the last inserted user ID  
            print(f"Successfully User added with id={new_user_id} into your connected SQLite database")
        conn_sqlite.commit()
        conn_sqlite.close()
    except Exception as e:
        print(f"Error updating user into your connected SQLite database: {e}")

    try:
        # Update into MySQL
        print("Updating User to your connected MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db")  
        # First, check if the received username already exists in the users table or not
        cursor_mysql.execute(
            """
            SELECT id FROM users 
            WHERE username = %s
            """, (username,)
        )
        result = cursor_mysql.fetchone()
        # Now getting role id of the received role_name
        cursor_mysql.execute(
            """
            SELECT id FROM roles 
            WHERE name = %s
            """, (role_name,)
        )
        role_id = cursor_mysql.fetchone()
        conn_mysql.close()
        if not role_id:
            # If not, insert as the new role, and get its newly stored id
            # Open New Connection and Commit and Close it, before again open main Connection & using that 
            conn_mysql = get_mysql_connection()
            cursor_mysql = conn_mysql.cursor()
            # Below specify the name of your connected MySQL database
            cursor_mysql.execute("USE mspms_mysql_db") 
            dummy_role_description =  'no description'
            cursor_mysql.execute(
                """
                INSERT INTO roles (name, description) 
                VALUES (%s, %s)
                """, (role_name, dummy_role_description)
            )
            mysql_role_id = cursor_mysql.lastrowid  # Get the last inserted role ID
            conn_mysql.commit()
            conn_mysql.close()
        else:
            # If role with that "role_name' is existed in SQLite, so just get its role_id
            mysql_role_id = role_id[0] if role_id else None
        # Again Open Connection
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db")  
        # Now either will update or insert as new
        if result:
            # If the user exists, get the existing user_id
            new_user_id = result[0]
            print(f"The user with username={username}, found in MySQL with ID={new_user_id}, So now just updating it with new data")
            # Update existing user
            cursor_mysql.execute(
                """
                UPDATE users 
                SET username=%s, password=%s, role_id=%s, full_name=%s, cnic=%s, gender=%s, dob=%s, address=%s
                WHERE id = %s
                """, (username, password, mysql_role_id, full_name, cnic, gender, dob, address, new_user_id)
            )
            print(f"Successfully User updated with id={new_user_id} into your connected MySQL database")
        else:
            # If not, insert as the new user
            cursor_mysql.execute(
                """
                INSERT INTO users (username, password, role_id, full_name, cnic, gender, dob, address) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (username, password, mysql_role_id, full_name, cnic, gender, dob, address)
            )
            new_user_id = cursor_mysql.lastrowid  # Get the last inserted user ID  
            print(f"Successfully User added with id={new_user_id} into your connected MySQL database")
        conn_mysql.commit()
        conn_mysql.close()
    except Exception as e:
        print(f"Error updating user into your connected MySQL database: {e}")



def delete_user(username):
    """Delete a user from SQLite and MySQL databases"""

    try:
        # Delete from SQLite
        print("Deleting User to your connected SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # First, check if the received role name already exists in the roles table or not
        cursor_sqlite.execute(
            """
            SELECT id FROM users 
            WHERE username = ?
            """, (username,)
        )
        result = cursor_sqlite.fetchone()
        if result:
            # If the user exists, get the existing user_id
            sqlite_user_id = result[0]
            print(f"The user with username={username}, found in SQLite with ID={sqlite_user_id}, So just deleting it")
            # Delete the existing user
            cursor_sqlite.execute("DELETE FROM users WHERE id=?", (sqlite_user_id,))
        else:
            print(f"No user with username={username} existed in SQLite, So We can't delete it")      
        conn_sqlite.commit()
        conn_sqlite.close()
    except Exception as e:
        print(f"Error deleting user from your connected SQLite database: {e}")

    try:
        # Delete from MySQL
        print("Deleting User to your connected MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db")  
         # First, check if the received role name already exists in the roles table or not
        cursor_mysql.execute(
            """
            SELECT id FROM users 
            WHERE username = %s
            """, (username,)
        )
        result = cursor_mysql.fetchone()
        if result:
            # If the user exists, get the existing user_id
            mysql_user_id = result[0]
            print(f"The user with username={username}, found in MySQL with ID={mysql_user_id}, So just deleting it")
            # Delete the existing user
            cursor_mysql.execute("DELETE FROM users WHERE id=%s", (mysql_user_id,))
        else:
            print(f"No user with username={username} existed in MySQL, So we can't delete it")
        conn_mysql.commit()
        conn_mysql.close()
    except Exception as e:
        print(f"Error deleting user from your connected MySQL database: {e}")


