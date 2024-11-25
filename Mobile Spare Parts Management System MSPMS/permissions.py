



# Permissions Controller



from database import get_sqlite_connection, get_mysql_connection



def fetch_permissions():
    """Fetch permissions from SQLite and MySQL databases"""
    
    fetched_permissions = []
    # Dictionary to store fetched permissions based on 'name' as value against 'index' as key
    seen_permissions = {}  

    try:
        # SQLite Connection
        sqlite_conn = get_sqlite_connection()
        cursor = sqlite_conn.cursor()
        # Fetch permissions from SQLite
        cursor.execute("SELECT id, name, description FROM permissions")
        sqlite_permissions = cursor.fetchall()
        sqlite_conn.close()
        if not sqlite_permissions:
            print("No permissions table data found in SQLite database.")
        else:    
            print("SQLite Permissions Table fetched data: ", sqlite_permissions)
            # Fetch Transactions Items
            for idx, permission in enumerate(sqlite_permissions):
                print("Permission tuple inside unpacking loop:", permission)
                permission_id, permission_name, permission_description = permission
                if permission_id in seen_permissions:
                    print(f"Skipping duplicate permission with Name={permission_name}  Bcz it's already fetched from MySQL")
                    continue  # Skip if already added
                # Store permission name of this sqlite fetched permission in the seen_permissions dictionary
                seen_permissions[idx] = (permission_name)
                # Append permission to final un-duplicated fetched_permissions list
                fetched_permissions.append(permission)
            print("Successfully fetched permissions from to your connected SQLite database")
    except Exception as e:
        print(f"Error fetching permissions from SQLite: {e}")

    try:
        # MySQL Connection
        mysql_conn = get_mysql_connection()
        cursor_mysql = mysql_conn.cursor()
        cursor_mysql.execute("USE mspms_mysql_db")  # Specify your MySQL database
        # Fetch permissions from MySQL
        cursor_mysql.execute("SELECT id, name, description FROM permissions")
        mysql_permissions = cursor_mysql.fetchall()
        mysql_conn.close()
        if not mysql_permissions:
            print("No permissions table data found in MySQL database.")
        else:    
            print("MySQL Permissions Table fetched data: ", mysql_permissions)
            for permission in mysql_permissions:
                permission_id, permission_name, permission_description = permission
                # Check if this permission_name already exists in the seen_permissions dictionary
                if any((permission_name) == pn for pn in seen_permissions.values()):
                    print(f"Skipping duplicate permission with Permission-Name:{permission_name} fetched from MySQL as it's already fetched from SQLite")
                    continue  # Skip if duplicate
                # Append permission to final un-duplicated fetched_permissions list
                fetched_permissions.append(permission)
            print("Successfully fetched all Permissions from your MySQL database")
    except Exception as e:
        print(f"Error fetching permissions from MySQL: {e}")

    # Final fetched_permissions without duplicates
    print("Final fetched all permissions (un-duplicated) from both databases = ", fetched_permissions)    
    return fetched_permissions
    


def add_permission(name, description):
    """Add a permission to SQLite and MySQL databases"""
    
    try:
        # Add into SQLite
        print("Now adding Permission into your connected SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # First, check if the received permission name already exists in the permissions table or not
        cursor_sqlite.execute(
            """
            SELECT id FROM permissions 
            WHERE name = ?
            """, (name,)
        )
        result = cursor_sqlite.fetchone()
        if result:
            # If the permission exists, get the existing permission_id
            new_permission_id = result[0]
            print(f"The permission with name={name}, found in SQLite with ID={new_permission_id}, No need to store again in SQLite")
        else:
            # If not, insert the new permission
            cursor_sqlite.execute(
                """
                INSERT INTO permissions (name, description) 
                VALUES (?, ?)
                """, (name, description)
            )
            new_permission_id = cursor_sqlite.lastrowid  # Get the last inserted permission ID
            print(f"Successfully Permission added with id={new_permission_id} into your connected SQLite database")
        conn_sqlite.commit()
        conn_sqlite.close()
    except Exception as e:
        print(f"Error adding permission into your connected SQLite database: {e}")

    try:
        # Add into MySQL
        print("Now adding Permission into your connected MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db") 
        # First, check if the received permission name already exists in the permissions table or not
        cursor_mysql.execute(
            """
            SELECT id FROM permissions 
            WHERE name = %s
            """, (name,)
        )
        result = cursor_mysql.fetchone()
        if result:
            # If the permission exists, get the existing permission_id
            new_permission_id = result[0]
            print(f"The permission with name={name}, found in MySQL with ID={new_permission_id}, No need to store again in MySQL")
        else:
            # If not, insert the new permission
            cursor_mysql.execute(
                """
                INSERT INTO permissions (name, description) 
                VALUES (%s, %s)
                """, (name, description)
            )        
            new_permission_id = cursor_mysql.lastrowid  # Get the last inserted permission ID
            print(f"Successfully Permission added with id={new_permission_id} into your connected MySQL database")
        conn_mysql.commit()
        conn_mysql.close()
    except Exception as e:
        print(f"Error adding permission into to your connected MySQL database: {e}")
    


def update_permission(permission_id, name, description):
    """Update a permission into SQLite and MySQL databases"""
    
    try:
        # Update into SQLite
        print("Updating Permission to your connected SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # First, check if the received permission name already exists in the permissions table or not
        cursor_sqlite.execute(
            """
            SELECT id FROM permissions 
            WHERE name = ?
            """, (name,)
        )
        result = cursor_sqlite.fetchone()
        if result:
            # If the permission exists, get the existing permission_id
            new_permission_id = result[0]
            print(f"The permission with name={name}, found in SQLite with ID={new_permission_id}, So just updating its Name and Description")
            # Update existing permission
            cursor_sqlite.execute(
                """
                UPDATE permissions 
                SET name = ?, description = ?
                WHERE id = ?
                """, (name, description, new_permission_id)
            )
        else:
            # If not, insert the new permission
            cursor_sqlite.execute(
                """
                INSERT INTO permissions (name, description) 
                VALUES (?, ?)
                """, (name, description)
            )
            new_permission_id = cursor_sqlite.lastrowid  # Get the last inserted permission ID
            print(f"Permission is newly inserted with id={new_permission_id} into your connected SQLite database")
        conn_sqlite.commit()
        conn_sqlite.close()
    except Exception as e:
        print(f"Error updating permission into your connected SQLite database: {e}")

    try:
        # Update into MySQL
        print("Updating Permission to your connected MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db")
        # First, check if the received permission name already exists in the permissions table or not
        cursor_mysql.execute(
            """
            SELECT id FROM permissions 
            WHERE name = %s
            """, (name,)
        )
        result = cursor_mysql.fetchone()
        if result:
            # If the permission exists, get the existing permission_id
            new_permission_id = result[0]
            print(f"The permission with name={name}, found in MySQL with ID={new_permission_id}, So just updating its Name and Description")
            # Update existing permission
            cursor_mysql.execute(
                """
                UPDATE permissions 
                SET name = %s, description = %s
                WHERE id = %s
                """, (name, description, new_permission_id)
            )
        else:
            # If not, insert the new permission
            cursor_mysql.execute(
                """
                INSERT INTO permissions (name, description) 
                VALUES (%s, %s)
                """, (name, description)
            )
            new_permission_id = cursor_mysql.lastrowid  # Get the last inserted permission ID
            print(f"Permission is newly inserted with id={new_permission_id} into your connected MySQL database")
        conn_mysql.commit()
        conn_mysql.close()
    except Exception as e:
        print(f"Error updating permission to your connected MySQL database: {e}")
    
   

def delete_permission(name):
    """Delete a permission from SQLite and MySQL databases"""
    
    try:
        # Delete from SQLite
        print("Deleting Permission from your connected SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # First, check if the received permission name already exists in the permissions table or not
        cursor_sqlite.execute(
            """
            SELECT id FROM permissions 
            WHERE name = ?
            """, (name,)
        )
        result = cursor_sqlite.fetchone()
        if result:
            # If the permission exists, get the existing permission_id
            sqlite_permission_id = result[0]
            print(f"The permission with name={name}, found in SQLite with ID={sqlite_permission_id}, So just deleting it")
            # Delete the existing permission
            cursor_sqlite.execute("DELETE FROM permissions WHERE id=?", (sqlite_permission_id,))
        else:
            print(f"No permission with name={name} existed in SQLite, So We can't delete it from SQLite permissions table")
        conn_sqlite.commit()
        conn_sqlite.close()
    except Exception as e:
        print(f"Error deleting permission from your connected SQLite database: {e}")

    try:
        # Delete from MySQL
        print("Deleting Permission from your connected MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db")
        # First, check if the received permission name already exists in the permissions table or not
        cursor_mysql.execute(
            """
            SELECT id FROM permissions 
            WHERE name = %s
            """, (name,)
        )
        result = cursor_mysql.fetchone()
        if result:
            # If the permission exists, get the existing permission_id
            mysql_permission_id = result[0]
            print(f"The permission with name={name}, found in MySQL with ID={mysql_permission_id}, So just deleting it")
            # Delete the existing permission
            cursor_mysql.execute("DELETE FROM permissions WHERE id=%s", (mysql_permission_id,))
        else:
            print(f"No permission with name={name} existed in MySQL, So We can't delete it from MySQL permissions table")
        conn_mysql.commit()
        conn_mysql.close()
    except Exception as e:
        print(f"Error deleting permission from your connected MySQL database: {e}")
    
