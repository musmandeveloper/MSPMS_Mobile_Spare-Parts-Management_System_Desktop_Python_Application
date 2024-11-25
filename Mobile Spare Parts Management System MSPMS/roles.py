



# Roles Controller



from database import get_sqlite_connection, get_mysql_connection



def fetch_roles():
    """Fetch parts from SQLite and MySQL databases"""
    
    fetched_roles = []
    # Dictionary to store fetched roles based on 'name' as value against 'index' as key
    seen_roles = {}  

    try:
        # SQLite Connection
        sqlite_conn = get_sqlite_connection()
        cursor = sqlite_conn.cursor()
        # Fetch roles from SQLite
        cursor.execute("SELECT id, name, description FROM roles")
        sqlite_roles = cursor.fetchall()
        sqlite_conn.close()
        if not sqlite_roles:
            print("No roles table data found in SQLite database.")
        else:    
            print("SQLite Roles Table fetched data: ", sqlite_roles)
            # Fetch Transactions Items
            for idx, role in enumerate(sqlite_roles):
                print("Role tuple inside unpacking loop:", role)
                role_id, role_name, role_description = role
                if role_id in seen_roles:
                    print(f"Skipping duplicate role with Name={role_name}  Bcz it's already fetched from MySQL")
                    continue  # Skip if already added
                # Store date and time of this sqlite fetched transaction in the seen_transactions dictionary
                seen_roles[idx] = (role_name)
                # Append authorization to final un-duplicated fetched_roles list
                fetched_roles.append(role)
            print("Successfully fetched roles from to your connected SQLite database")
    except Exception as e:
        print(f"Error fetching roles from SQLite: {e}")

    try:
        # MySQL Connection
        mysql_conn = get_mysql_connection()
        cursor_mysql = mysql_conn.cursor()
        cursor_mysql.execute("USE mspms_mysql_db")  # Specify your MySQL database
        # Fetch roles from MySQL
        cursor_mysql.execute("SELECT id, name, description FROM roles")
        mysql_roles = cursor_mysql.fetchall()
        mysql_conn.close()
        if not mysql_roles:
            print("No roles table data found in MySQL database.")
        else:    
            print("MySQL Roles Table fetched data: ", mysql_roles)
            for role in mysql_roles:
                role_id, role_name, role_description = role
                # Check if this (role_name,permission_name) pair already exists in the seen_roles dictionary
                if any((role_name) == rn for rn in seen_roles.values()):
                    print(f"Skipping duplicate role with Role-Name:{role_name} fetched from MySQL as it's already fetched from SQLite")
                    continue  # Skip if duplicate
                # Append authorization to final un-duplicated fetched_roles list
                fetched_roles.append(role)
            print("Successfully fetched all Roles from your MySQL database")
    except Exception as e:
        print(f"Error fetching roles from MySQL: {e}")

    # Final fetched_roles without duplicates
    print("Final fetched all roles (un-duplicated) from both databases = ", fetched_roles)    
    return fetched_roles 
    


def add_role(name, description):
    """Add a role to SQLite and MySQL databases"""
    
    try:
        # Add into SQLite
        print("Now adding Role into your connected SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # First, check if the received role name already exists in the roles table or not
        cursor_sqlite.execute(
            """
            SELECT id FROM roles 
            WHERE name = ?
            """, (name,)
        )
        result = cursor_sqlite.fetchone()
        if result:
            # If the role exists, get the existing role_id
            new_role_id = result[0]
            print(f"The role with name={name}, found in SQLite with ID={new_role_id}, No need to store again in SQLite")
        else:
            # If not, insert the new part
            cursor_sqlite.execute(
                """
                INSERT INTO roles (name, description) 
                VALUES (?, ?)
                """, (name, description)
            )
            new_role_id = cursor_sqlite.lastrowid  # Get the last inserted role ID  
            print(f"Successfully Role added with id={new_role_id} into your connected SQLite database")            
        conn_sqlite.commit()
        conn_sqlite.close()
    except Exception as e:
        print(f"Error adding role into your connected SQLite database: {e}")
    
    try:
        # Add into MySQL
        print("Now adding Role into your connected MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db") 
        # First, check if the received role name already exists in the roles table or not
        cursor_mysql.execute(
            """
            SELECT id FROM roles 
            WHERE name = %s
            """, (name,)
        )
        result = cursor_mysql.fetchone()
        if result:
            # If the role exists, get the existing role_id
            new_role_id = result[0]
            print(f"The role with name={name}, found in SQLite with ID={new_role_id}, No need to store again in MySQL")
        else:
            # If not, insert the new role
            cursor_mysql.execute(
                """
                INSERT INTO roles (name, description) 
                VALUES (%s, %s)
                """, (name, description)
            ) 
            new_role_id = cursor_mysql.lastrowid  # Get the last inserted role ID       
            print(f"Successfully Role added with id={new_role_id} into your connected MySQL database")
        conn_mysql.commit()
        conn_mysql.close()
    except Exception as e:
        print(f"Error adding role into to your connected MySQL database: {e}")
    


def update_role(role_id, name, description):
    """Update a role into SQLite and MySQL databases"""
    
    try:
        # Update into SQLite
        print("Updating Role to your connected SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # First, check if the received role name already exists in the roles table or not
        cursor_sqlite.execute(
            """
            SELECT id FROM roles 
            WHERE name = ?
            """, (name,)
        )
        result = cursor_sqlite.fetchone()
        if result:
            # If the role exists, get the existing role_id
            new_role_id = result[0]
            print(f"The role with name={name}, found in SQLite with ID={new_role_id}, So just updating its Name and Description")
            # Update existing transaction items
            cursor_sqlite.execute(
                """
                UPDATE roles 
                SET name = ?, description = ?
                WHERE new_role_id = ?
                """, (name, description, new_role_id))
        else:
            # If not, insert the new role
            cursor_sqlite.execute(
                """
                INSERT INTO roles (name, description) 
                VALUES (?, ?)
                """, (name, description)
            ) 
            new_role_id = cursor_sqlite.lastrowid  # Get the last inserted role ID
            print(f"Role is newly inserted with id={new_role_id} into your connected SQLite database")
        conn_sqlite.commit()
        conn_sqlite.close()
    except Exception as e:
        print(f"Error updating role into your connected SQLite database: {e}")

    try:
        # Update into MySQL
        print("Updating Role to your connected MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db")  
       # First, check if the received role name already exists in the roles table or not
        cursor_mysql.execute(
            """
            SELECT id FROM roles 
            WHERE name = %s
            """, (name,)
        )
        result = cursor_mysql.fetchone()
        if result:
            # If the role exists, get the existing role_id
            new_role_id = result[0]
            print(f"The role with name={name}, found in SQLite with ID={new_role_id}, So just updating its Name and Description")
            # Update existing transaction items
            cursor_mysql.execute(
                """
                UPDATE roles 
                SET name = %s, description = %s
                WHERE new_role_id = %s
                """, (name, description, new_role_id))
        else:
            # If not, insert the new role
            cursor_mysql.execute(
                """
                INSERT INTO roles (name, description) 
                VALUES (%s, %s)
                """, (name, description)
            ) 
            new_role_id = cursor_mysql.lastrowid  # Get the last inserted role ID
            print(f"Role is newly inserted with id={new_role_id} into your connected MySQL database")        
        conn_mysql.commit()
        conn_mysql.close()
    except Exception as e:
        print(f"Error updating role to your connected MySQL database: {e}")
    


def delete_role(name):
    """Delete a role from SQLite and MySQL databases"""
    
    try:
        # Delete from SQLite
        print("Deleting Role from your connected SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # First, check if the received role name already exists in the roles table or not
        cursor_sqlite.execute(
            """
            SELECT id FROM roles 
            WHERE name = ?
            """, (name,)
        )
        result = cursor_sqlite.fetchone()
        if result:
            # If the role exists, get the existing role_id
            sqlite_role_id = result[0]
            print(f"The role with name={name}, found in SQLite with ID={sqlite_role_id}, So just deleting it")
            # Delete the existing role
            cursor_sqlite.execute("DELETE FROM roles WHERE id=?", (sqlite_role_id,))
        else:
            print(f"No role with name={name} existed in SQLite, So We can't delete it from SQLite roles table")
        conn_sqlite.commit()
        conn_sqlite.close()
    except Exception as e:
        print(f"Error deleting role from your connected SQLite database: {e}")

    try:
        # Delete from MySQL
        print("Deleting Role from your connected MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db")  
        # First, check if the received role name already exists in the roles table or not
        cursor_mysql.execute(
            """
            SELECT id FROM roles 
            WHERE name = %s
            """, (name,)
        )
        result = cursor_mysql.fetchone()
        if result:
            # If the role exists, get the existing role_id
            mysql_role_id = result[0]
            print(f"The role with name={name}, found in MySQL with ID={mysql_role_id}, So just deleting it")
            # Delete the existing role
            cursor_mysql.execute("DELETE FROM roles WHERE id=%s", (mysql_role_id,))
        else:
            print(f"No role with name={name} existed in MySQL, So We can't delete it from MySQL roles table")        
        conn_mysql.commit()
        conn_mysql.close()
    except Exception as e:
        print(f"Error deleting role from your connected MySQL database: {e}")
    







