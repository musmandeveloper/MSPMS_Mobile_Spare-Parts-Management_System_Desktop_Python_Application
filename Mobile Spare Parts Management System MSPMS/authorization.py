



# Authorization Controller



from database import get_sqlite_connection, get_mysql_connection



def fetch_authorizations():
    """Fetch authorizations from SQLite and MySQL databases"""
    
    fetched_authorizations = []
    # Dictionary to track (role_name,permission_name) pairs with index keys, to avoid duplicate transactions 
    # even their IDs in both database are different, until date time is same then it means both 
    # are same transaction, So we find duplicates based on Date Time of each transaction
    seen_authorizations = {} 

    try:
        # SQLite Connection
        print("Now fetching authorizations from your connected SQLite database")        
        sqlite_conn = get_sqlite_connection()
        cursor_sqlite = sqlite_conn.cursor()
        cursor_sqlite.execute(
            """SELECT a.id, r.name AS role_name, p.name AS permission_name
               FROM authorizations a
               JOIN roles r ON a.role_id = r.id
               JOIN permissions p ON a.permission_id = p.id
            """)
        sqlite_authorizations = cursor_sqlite.fetchall()
        sqlite_conn.close()
        if not sqlite_authorizations:
            print("No authorizations table data found in SQLite database.")
        else:    
            print("Authorizations Table fetched data: ", sqlite_authorizations)
            # Fetch Transactions Items
            for idx, authorization in enumerate(sqlite_authorizations):
                print("Authorization tuple inside unpacking loop:", authorization)
                authorization_id, role_name, permission_name = authorization
                if authorization_id in seen_authorizations:
                    print(f"Skipping duplicate authorization with ID {authorization_id}  Bcz it's already fetched from MySQL")
                    continue  # Skip if already added
                # Store date and time of this sqlite fetched transaction in the seen_transactions dictionary
                seen_authorizations[idx] = (role_name,permission_name)
                # Append authorization to final un-duplicated fetched_authorizations list
                fetched_authorizations.append(authorization)
            print("Successfully fetched authorizations from to your connected SQLite database")
    except Exception as e:
        print(f"Error fetching authorizations from SQLite: {e}")

    try:
        # MySQL Connection
        print("Now fetching authorizations from your connected MySQL database")                
        mysql_conn = get_mysql_connection()
        cursor_mysql = mysql_conn.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db") 
        cursor_mysql.execute(
            """SELECT a.id, r.name AS role_name, p.name AS permission_name
               FROM authorizations a
               JOIN roles r ON a.role_id = r.id
               JOIN permissions p ON a.permission_id = p.id
            """)
        mysql_authorizations = cursor_mysql.fetchall()
        mysql_conn.close()
        if not mysql_authorizations:
            print("No authorizations table data found in MySQL database.")
        else:
            print("Authorizations all fetched data from MySQL: ", mysql_authorizations)
            for authorization in mysql_authorizations:
                authorization_id, role_name, permission_name = authorization
                # Check if this (role_name,permission_name) pair already exists in the seen_authorizations dictionary
                if any((role_name,permission_name) == rn_pn for rn_pn in seen_authorizations.values()):
                    print(f"Skipping duplicate authorization with Role-Name: {role_name} and Permission-Name: {permission_name} fetched from MySQL as it's already fetched from SQLite")
                    continue  # Skip if duplicate
                # Append authorization to final un-duplicated fetched_authorizations list
                fetched_authorizations.append(authorization)
            print("Successfully fetched all Authorizations from your MySQL database")
    except Exception as e:
        print(f"Error fetching authorizations from MySQL: {e}")

    # Final fetched_authorizations without duplicates
    print("Final fetched all authorizations (un-duplicated) from both databases = ", fetched_authorizations)
    return fetched_authorizations




def add_authorization(role_name, permissions_name):
    """Add a authorization to SQLite and MySQL databases"""

    try:
        # Add into SQLite
        print("Now adding Received Permissions assigned to selected Role-Name into your connected SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # Check if the received role_name already exists in the roles table
        cursor_sqlite.execute(
            """
            SELECT id FROM roles 
            WHERE name = ?
            """, (role_name,)
        )
        result_role = cursor_sqlite.fetchone()
        if not result_role:
            # If the role does not exist, insert it and get the saved role_id
            description = "No description"  # Define a default description if needed
            cursor_sqlite.execute(
                """
                INSERT INTO roles (name, description) 
                VALUES (?, ?)
                """, (role_name, description)
            )
            sqlite_role_id = cursor_sqlite.lastrowid  # Get the last inserted role ID
            conn_sqlite.commit()
            print(f"Role '{role_name}' added to SQLite with ID={sqlite_role_id}.")
        else:
            sqlite_role_id = result_role[0]
            print(f"Role '{role_name}' already exists with ID={sqlite_role_id}.")
        # Process permissions
        sqlite_permissions_id = []
        for permission_name in permissions_name:
            cursor_sqlite.execute(
                """
                SELECT id FROM permissions 
                WHERE name = ?
                """, (permission_name,)
            )
            result_permission = cursor_sqlite.fetchone()
            if not result_permission:
                # If the permission does not exist, insert it and get the new assigned id
                cursor_sqlite.execute(
                    """
                    INSERT INTO permissions (name, description) 
                    VALUES (?, ?)
                    """, (permission_name, 'no description')
                )
                sqlite_permissions_id.append(cursor_sqlite.lastrowid)  # Append the last inserted row ID
                conn_sqlite.commit()
                print(f"Permission '{permission_name}' added to SQLite.")
            else:
                sqlite_permissions_id.append(result_permission[0])  # Add the existing permission ID
        # Insert role and permissions into the authorizations table
        for sqlite_permission_id in sqlite_permissions_id:
            cursor_sqlite.execute(
                """
                INSERT INTO authorizations (role_id, permission_id) 
                VALUES (?, ?)
                """, (sqlite_role_id, sqlite_permission_id)
            )
            conn_sqlite.commit()
        conn_sqlite.close()
        print(f"Successfully added into authorizations the selected role='{role_name}' with selected permissions={permissions_name} in SQLite.")
    except Exception as e:
        print(f"Error adding authorization to SQLite database: {e}")

    try:
        # Add into MySQL
        print("Now adding received Permissions assigned to selected Role-Name into your connected MySQL database")
        conn_mysql = get_mysql_connection()  # Function to get MySQL connection
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db") 
        # Check if the received role_name already exists in the roles table
        cursor_mysql.execute(
            """
            SELECT id FROM roles 
            WHERE name = %s
            """, (role_name,)
        )
        result_role = cursor_mysql.fetchone()
        if not result_role:
            # If the role does not exist, insert it and get the saved role_id
            description = "No description"  # Define a default description if needed
            cursor_mysql.execute(
                """
                INSERT INTO roles (name, description) 
                VALUES (%s, %s)
                """, (role_name, description)
            )
            mysql_role_id = cursor_mysql.lastrowid  # Get the last inserted role ID
            conn_mysql.commit()
            print(f"Role '{role_name}' added to MySQL with ID={mysql_role_id}.")
        else:
            mysql_role_id = result_role[0]
            print(f"Role '{role_name}' already exists with ID={mysql_role_id}.")        
        # Process permissions
        mysql_permissions_id = []
        for permission_name in permissions_name:
            cursor_mysql.execute(
                """
                SELECT id FROM permissions 
                WHERE name = %s
                """, (permission_name,)
            )
            result_permission = cursor_mysql.fetchone()            
            if not result_permission:
                # If the permission does not exist, insert it and get the new assigned id
                cursor_mysql.execute(
                    """
                    INSERT INTO permissions (name, description) 
                    VALUES (%s, %s)
                    """, (permission_name, 'no description')
                )
                mysql_permissions_id.append(cursor_mysql.lastrowid)  # Append the last inserted row ID
                conn_mysql.commit()
                print(f"Permission '{permission_name}' added to MySQL.")
            else:
                mysql_permissions_id.append(result_permission[0])  # Add the existing permission ID
        # Insert role and permissions into the authorizations table
        for mysql_permission_id in mysql_permissions_id:
            cursor_mysql.execute(
                """
                INSERT INTO authorizations (role_id, permission_id) 
                VALUES (%s, %s)
                """, (mysql_role_id, mysql_permission_id)
            )
            conn_mysql.commit()        
        conn_mysql.close()
        print(f"Successfully added into authorizations the selected role='{role_name}' with selected permissions={permissions_name} in MySQL.")
    except Exception as e:
        print(f"Error adding authorization to MySQL database: {e}")




# fetch old permissions assigned to a role_name
def fetch_assigned_permissions(role_name):
    """Fetch all permissions assigned to a given role_name from SQLite and MySQL databases without duplicates"""
    
    assigned_permissions = []
    # Dictionary to track duplicates, storing permission-name as value against index as key
    seen_permissions = {}

    # Fetch assigned permissions from SQLite
    try:
        print(f"Fetching assigned permissions for role_name='{role_name}' from SQLite database...")
        sqlite_conn = get_sqlite_connection()
        cursor_sqlite = sqlite_conn.cursor()
        # Fetch role_id using role_name
        cursor_sqlite.execute("SELECT id FROM roles WHERE name = ?", (role_name,))
        role_id = cursor_sqlite.fetchone()[0]  # Assuming role_name is unique
        query = "SELECT permission_id FROM authorizations WHERE role_id = ?"
        cursor_sqlite.execute(query, (role_id,))
        sqlite_permissions = cursor_sqlite.fetchall()
        sqlite_conn.close()
        # Insert SQLite fetched permissions into seen_permissions dictionary
        for idx, perm in enumerate(sqlite_permissions):
            permission_id = perm[0]
            if permission_id not in seen_permissions:
                seen_permissions[idx] = permission_id
                assigned_permissions.append(permission_id)
            else:
                print(f"Skipping duplicate permission ID={permission_id} from SQLite")
        print(f"Successfully fetched {len(sqlite_permissions)} assigned old permissions from SQLite for role_id {role_id}")
    except Exception as e:
        print(f"Error fetching permissions from SQLite for role_name={role_name} is: {e}")
    # Fetch assigned permissions from MySQL
    try:
        print(f"Fetching assigned permissions for role_name='{role_name}' from MySQL database...")
        mysql_conn = get_mysql_connection()
        cursor_mysql = mysql_conn.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db") 
        # Fetch role_id using role_name
        cursor_mysql.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
        role_id = cursor_mysql.fetchone()[0]  # Assuming role_name is unique
        query_mysql = "SELECT permission_id FROM authorizations WHERE role_id = %s"
        cursor_mysql.execute(query_mysql, (role_id,))
        mysql_permissions = cursor_mysql.fetchall()
        mysql_conn.close()
        # Insert MySQL fetched permissions after checking for duplicates
        for mysql_perm in mysql_permissions:
            permission_id = mysql_perm[0]
            # Check if permission already exists in seen_permissions
            if permission_id in seen_permissions.values():
                print(f"Skipping duplicate permission ID={permission_id} fetched from MySQL as it's already fetched from SQLite")
            else:
                seen_permissions[len(seen_permissions)] = permission_id
                assigned_permissions.append(permission_id)
        print(f"Successfully fetched {len(mysql_permissions)} assigned old permissions from MySQL for role_id {role_id}")
    except Exception as e:
        print(f"Error fetching permissions from MySQL for selected role_name={role_name} is: {e}")

    # Final list of assigned permissions without duplicates
    print(f"Final old assigned permissions (un-duplicated) for selected role_name={role_name} are: {assigned_permissions}")
    return assigned_permissions





def update_authorization(authorization_id, role_name, permission_names):
    """Update a authorization to SQLite and MySQL databases"""

    try:
        # Step 1: Get or insert role_id for the received role_name in SQLite
        print(f"Fetching role_id for role_name '{role_name}' from SQLite...")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        cursor_sqlite.execute("SELECT id FROM roles WHERE name = ?", (role_name,))
        result = cursor_sqlite.fetchone()
        if result is None:
            print(f"Role '{role_name}' not found in SQLite. First Inserting new role in roles table in SQLite...")
            cursor_sqlite.execute("INSERT INTO roles (name) VALUES (?)", (role_name,))
            conn_sqlite.commit()
            cursor_sqlite.execute("SELECT id FROM roles WHERE name = ?", (role_name,))
            result = cursor_sqlite.fetchone()
        sqlite_role_id = result[0]  # Get the fetched or newly inserted role_id
        print(f"SQLite role_id for '{role_name}' = {sqlite_role_id}")
        # Step 2: Get or insert permission_ids for each permission_name in SQLite
        sqlite_permissions_ids = []
        for permission_name in permission_names:
            cursor_sqlite.execute("SELECT id FROM permissions WHERE name = ?", (permission_name,))
            result = cursor_sqlite.fetchone()
            if result is None:
                print(f"Permission '{permission_name}' not found in SQLite. Inserting new permission...")
                cursor_sqlite.execute("INSERT INTO permissions (name) VALUES (?)", (permission_name,))
                conn_sqlite.commit()
                cursor_sqlite.execute("SELECT id FROM permissions WHERE name = ?", (permission_name,))
                result = cursor_sqlite.fetchone()
            sqlite_permissions_ids.append(result[0])  # Add the permission_id to the list
        # Step 3: Delete authorizations for the role_id where permission_id is not in the new permission_ids
        print(f"Deleting old authorizations for role_id '{sqlite_role_id}' where permission_id is not in the new list...")
        cursor_sqlite.execute(
            "DELETE FROM authorizations WHERE role_id = ? AND permission_id NOT IN ({})".format(
                ",".join("?" * len(sqlite_permissions_ids))
            ),
            [sqlite_role_id] + sqlite_permissions_ids
        )
        conn_sqlite.commit()
        # Step 4: Insert or update authorizations for the new permissions
        print(f"Inserting/updating authorizations for role_id '{sqlite_role_id}' with new permission_ids...")
        for permission_id in sqlite_permissions_ids:
            cursor_sqlite.execute(
                "REPLACE INTO authorizations (role_id, permission_id) VALUES (?, ?)",
                (sqlite_role_id, permission_id)
            )
        conn_sqlite.commit()
        conn_sqlite.close()
        print("Successfully updated authorizations in SQLite")
    except Exception as e:
        print(f"Error updating authorizations in SQLite: {e}")


    try:
        # Step 1: Get or insert role_id for the received role_name in MySQL
        print(f"Fetching role_id for role_name '{role_name}' from MySQL...")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        cursor_mysql.execute("USE mspms_mysql_db")
        cursor_mysql.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
        result = cursor_mysql.fetchone()
        if result is None:
            print(f"Role '{role_name}' not found in MySQL. First Inserting new role in roles table in MySQL...")
            cursor_mysql.execute("INSERT INTO roles (name) VALUES (%s)", (role_name,))
            conn_mysql.commit()
            cursor_mysql.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
            result = cursor_mysql.fetchone()
        mysql_role_id = result[0]  # Get the fetched or newly inserted role_id
        print(f"MySQL role_id for '{role_name}' = {mysql_role_id}")
        # Step 2: Get or insert permission_ids for each permission_name in MySQL
        mysql_permissions_ids = []
        for permission_name in permission_names:
            cursor_mysql.execute("SELECT id FROM permissions WHERE name = %s", (permission_name,))
            result = cursor_mysql.fetchone()
            if result is None:
                print(f"Permission '{permission_name}' not found in MySQL. Inserting new permission...")
                cursor_mysql.execute("INSERT INTO permissions (name) VALUES (%s)", (permission_name,))
                conn_mysql.commit()
                cursor_mysql.execute("SELECT id FROM permissions WHERE name = %s", (permission_name,))
                result = cursor_mysql.fetchone()
            mysql_permissions_ids.append(result[0])  # Add the permission_id to the list
        # Step 3: Delete authorizations for the role_id where permission_id is not in the new permission_ids
        print(f"Deleting old authorizations for role_id '{mysql_role_id}' where permission_id is not in the new list...")
        cursor_mysql.execute(
            "DELETE FROM authorizations WHERE role_id = %s AND permission_id NOT IN ({})".format(
                ",".join("%s" for _ in mysql_permissions_ids)
            ),
            [mysql_role_id] + mysql_permissions_ids
        )
        conn_mysql.commit()
        # Step 4: Insert or update authorizations for the new permissions
        print(f"Inserting/updating authorizations for role_id '{mysql_role_id}' with new permission_ids...")
        for permission_id in mysql_permissions_ids:
            cursor_mysql.execute(
                "REPLACE INTO authorizations (role_id, permission_id) VALUES (%s, %s)",
                (mysql_role_id, permission_id)
            )
        conn_mysql.commit()
        conn_mysql.close()
        print("Successfully updated authorizations in MySQL")
    except Exception as e:
        print(f"Error updating authorizations in MySQL: {e}")



def delete_authorization(role_name): 
    """Delete an authorization from SQLite database based on the role_name"""

    try:
        # Step 1: Get role_id for the received role_name in SQLite
        print(f"Fetching role_id for role_name '{role_name}' from SQLite...")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        cursor_sqlite.execute("SELECT id FROM roles WHERE name = ?", (role_name,))
        result = cursor_sqlite.fetchone()
        if result is None:
            print(f"Error: Role '{role_name}' not found in SQLite roles table.")
            return  # Exit function if role_name not found
        sqlite_role_id = result[0]  # Get the fetched role_id
        print(f"SQLite role_id for '{role_name}' = {sqlite_role_id}")
        # Step 2: Check if any authorizations exist for the fetched role_id
        cursor_sqlite.execute("SELECT id FROM authorizations WHERE role_id = ?", (sqlite_role_id,))
        authorization_results = cursor_sqlite.fetchall()
        if not authorization_results:
            print(f"No permissions were assigned or added in SQLite for role '{role_name}'.")
        else:
            # Step 3: Delete authorizations for the fetched role_id
            print(f"Deleting all authorizations for role_id '{sqlite_role_id}' in SQLite...")
            cursor_sqlite.execute("DELETE FROM authorizations WHERE role_id = ?", (sqlite_role_id,))
            conn_sqlite.commit()
            print(f"Successfully deleted authorizations for role '{role_name}' in SQLite.")        
        conn_sqlite.close()
    except Exception as e:
        print(f"Error deleting authorizations for role '{role_name}' from SQLite: {e}")


    try:
        # Connect to MySQL and select the appropriate database
        print("Deleting authorization from your connected MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()       
        # Step 1: Use the MySQL database
        cursor_mysql.execute("USE mspms_mysql_db")     
        # Step 2: Get role_id for the received role_name in MySQL
        print(f"Fetching role_id for role_name '{role_name}' from MySQL...")
        cursor_mysql.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
        result = cursor_mysql.fetchone()        
        if result is None:
            print(f"Error: Role '{role_name}' not found in MySQL roles table.")
            return  # Exit function if role_name not found
        mysql_role_id = result[0]  # Get the fetched role_id
        print(f"MySQL role_id for '{role_name}' = {mysql_role_id}")
        # Step 3: Check if any authorizations exist for the fetched role_id
        cursor_mysql.execute("SELECT id FROM authorizations WHERE role_id = %s", (mysql_role_id,))
        authorization_results = cursor_mysql.fetchall()
        if not authorization_results:
            print(f"No permissions were assigned or added in MySQL for role '{role_name}'.")
        else:
            # Step 4: Delete authorizations for the fetched role_id
            print(f"Deleting all authorizations for role_id '{mysql_role_id}' in MySQL...")
            cursor_mysql.execute("DELETE FROM authorizations WHERE role_id = %s", (mysql_role_id,))
            conn_mysql.commit()
            print(f"Successfully deleted authorizations for role '{role_name}' in MySQL.")
        conn_mysql.close()
    except Exception as e:
        print(f"Error deleting authorizations for role '{role_name}' from MySQL: {e}")



