


# Inventory Controller, Backend Functions 


from database import get_sqlite_connection, get_mysql_connection



def fetch_parts():
    """Fetch parts from SQLite and MySQL databases"""

    fetched_parts = []
    # Dictionary to track (name,category) pairs with index keys, to avoid duplicate parts
    seen_parts = {} 

    try:
        print("Now Fetching Spare-Parts from your connected SQLite database")
        # SQLite Connection
        sqlite_conn = get_sqlite_connection()
        cursor_sqlite = sqlite_conn.cursor()
        # Fetch Parts
        cursor_sqlite.execute("SELECT id, name, category, purchase_price, sale_price FROM spare_parts")
        sqlite_parts = cursor_sqlite.fetchall()
        sqlite_conn.close()
        if not sqlite_parts:
            print("No spare_parts table data found in SQLite database.")
        else:    
            print("Spare-Parts all fetched data from SQLite: ", sqlite_parts) 
            for idx, part in enumerate(sqlite_parts):
                part_id, name, category, purchase_price, sale_price = part
                # Store the (name, category) pair in seen_parts dictionary against the part ID
                seen_parts[idx] = (name,category)
                # Append part to final un-duplicated fetched parts list
                fetched_parts.append(part)  
            print("Successfully fetched all Spare-Parts from your SQLite database")
    except Exception as e:
        print(f"Error fetching spare parts from SQLite: {e}")

    try:
        print("Now Fetching Spare-Parts from your connected MySQL database")
        # MySQL Connection
        mysql_conn = get_mysql_connection()
        cursor_mysql = mysql_conn.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db")
        # Fetch Parts
        cursor_mysql.execute("SELECT id, name, category, purchase_price, sale_price FROM spare_parts")
        mysql_parts = cursor_mysql.fetchall()
        mysql_conn.close()
        if not mysql_parts:
            print("No spare_parts table data found in MySQL database.")
        else:
            print("Spare-Parts all fetched data from MySQL: ", mysql_parts)
            for part in mysql_parts:
                part_id, name, category, purchase_price, sale_price = part
                # Check if this (name, category) pair already exists in the seen_parts dictionary
                if any((name, category) == nc for nc in seen_parts.values()):
                    print(f"Skipping duplicate part with Name: {name} and Category: {category} fetched from MySQL as it's already fetched from SQLite")
                    continue  # Skip if duplicate
                # Append the part only if it's not duplicate to final un-duplicated fetched parts list
                fetched_parts.append(part)  
            print("Successfully fetched all Spare-Parts from your MySQL database")
    except Exception as e:
        print(f"Error fetching spare parts from MySQL: {e}")

    # Final fetched spare-parts without duplicates
    print("Final fetched all spare-parts (un-duplicated) from both databases = ", fetched_parts)
    return fetched_parts



def add_part(name, category, purchase_price, sale_price):
    """Add a part to SQLite and MySQL databases"""
    
    try:
        # Add into SQLite
        print("Now adding Spare-Part into spare-parts to your connected SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        cursor_sqlite.execute("INSERT INTO spare_parts (name, category, purchase_price, sale_price) VALUES (?, ?, ?, ?)", (name, category, purchase_price, sale_price))
        conn_sqlite.commit()
        conn_sqlite.close()
        print("Spare-Part added into spare-parts to your connected SQLite database successfully")
    except Exception as e:
        print(f"Error adding spare-part into spare-parts to your connected SQLite database: {e}")
    
    try:
        # Add into MySQL
        print("Now adding Spare-Part into spare-parts to your connected MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db")  
        cursor_mysql.execute("INSERT INTO spare_parts (name, category, purchase_price, sale_price) VALUES (%s, %s, %s, %s)", (name, category, purchase_price, sale_price))
        conn_mysql.commit()
        conn_mysql.close()
        print("Spare-Part added into spare-parts to your connected MySQL database successfully")
    except Exception as e:
        print(f"Error adding spare-part into spare-parts to your connected MySQL database: {e}")


def add_purchased_items_sqlite(purchased_items):
    """Add purchased parts into spare_parts to SQLite database"""

    stored_purchased_items = []

    for purchased_item in purchased_items:
        print("Received Purchased Items :", purchased_items)
        print("Unpacking the Received Purchased Items to store into spare_parts Table.")
        name, category, quantity, purchase_price, sale_price, total_price = purchased_item
        # Safely convert quantity to int, regardless of whether it was passed as a string or int
        quantity = int(quantity)
        
        try:
            # Add into SQLite
            print("Now adding Purchased Items into spare-parts to your connected SQLite database")
            # SQLite Connection
            conn_sqlite = get_sqlite_connection()
            cursor_sqlite = conn_sqlite.cursor()
            # Check if item already exists
            cursor_sqlite.execute("SELECT id FROM spare_parts WHERE name = ? AND category = ?", (name, category))
            existing_item = cursor_sqlite.fetchone()
            # Extracting the id from the fetched tuple
            existing_item= existing_item[0]  # Use the first element of the tuple
            # If Item Already Existed
            if existing_item:
                print("This item already exists, so just updating purchase and sale price in spare-parts Table in SQLite ")
                existing_id = existing_item
                # Update the existing item information
                cursor_sqlite.execute("""
                    UPDATE spare_parts 
                    SET purchase_price = ?, sale_price = ?
                    WHERE id = ?
                """, (purchase_price, sale_price, existing_id))
                print("Data updated successfully, now appending in stored_purchased_items List")
                stored_purchased_items.append((existing_id, name, category, quantity, sale_price, total_price, purchase_price))
            else:
                # Insert as a new item
                print("Inserting as new Spare-Part in spare-parts Table in SQLite")
                cursor_sqlite.execute("""
                    INSERT INTO spare_parts (name, category, purchase_price, sale_price)
                    VALUES (?, ?, ?, ?)
                """, (name, category, purchase_price, sale_price))
                print("Data stored successfully, now appending in stored_purchased_items List to then store it in transaction_items Table")
                stored_purchased_items.append((cursor_sqlite.lastrowid, name, category, quantity, sale_price, total_price, purchase_price))
            conn_sqlite.commit()
            conn_sqlite.close()
            print("Successfully added the Purchased Items into spare-parts to your connected SQLite database")
        except Exception as e:
            print(f"Error adding Purchased Items into spare-parts to your connected SQLite database: {e}")
    # Returning purchased-items stored in SQLite
    print("Returning purchased-items stored in SQLite:", stored_purchased_items)
    return stored_purchased_items



def add_purchased_items_mysql(purchased_items):
    """Add purchased parts into spare_parts to MySQL database"""

    stored_purchased_items = []

    for purchased_item in purchased_items:
        print("Received Purchased Items :", purchased_items)
        print("Unpacking the Received Purchased Items to store into spare_parts Table.")
        name, category, quantity, purchase_price, sale_price, total_price = purchased_item
        # Safely convert quantity to int, regardless of whether it was passed as a string or int
        quantity = int(quantity)        

        try:
            # Add into MySQL
            print("Now adding Purchased Items into spare-parts to your connected MySQL database")
            conn_mysql = get_mysql_connection()
            cursor_mysql = conn_mysql.cursor()
            # Below specify the name of your connected MySQL database
            cursor_mysql.execute("USE mspms_mysql_db") 
            # Check if item already exists
            cursor_mysql.execute("SELECT id FROM spare_parts WHERE name = %s AND category = %s", (name, category))
            existing_item = cursor_mysql.fetchone()
            # Extracting the id from the fetched tuple
            existing_item= existing_item[0]  # Use the first element of the tuple
            # If Item is already existing
            if existing_item:
                # Update the existing item
                print("This item already exists, so just updating purchase and sale price in spare-parts Table in MySQL")               
                existing_id = existing_item
                cursor_mysql.execute("""
                    UPDATE spare_parts 
                    SET purchase_price = %s, sale_price = %s
                    WHERE id = %s
                """, (purchase_price, sale_price, existing_id))
                print("Data updated successfully, now appending in stored_purchased_items List")
                # Check if item is already in stored_purchased_items
                # if not any(item[0] == existing_id for item in stored_purchased_items):
                stored_purchased_items.append((existing_id, name, category, quantity, sale_price, total_price, purchase_price))
            else:
                # Insert as a new item
                print("Inserting as new Spare-Part in spare-parts Table in MySQL")
                cursor_mysql.execute("""
                    INSERT INTO spare_parts (name, category, purchase_price, sale_price)
                    VALUES (%s, %s, %s, %s)
                """, (name, category, purchase_price, sale_price))
                print("Data stored successfully, now appending in stored_purchased_items List to then store it in transaction_items Table")
                if not any(item[0] == cursor_mysql.lastrowid for item in stored_purchased_items):
                    stored_purchased_items.append((cursor_mysql.lastrowid, name, category, quantity, sale_price, total_price, purchase_price))
            conn_mysql.commit()
            conn_mysql.close()
            print("Successfully added the Purchased Items into spare-parts to your connected MySQL database")
        except Exception as e:
            print(f"Error adding Purchased Items into spare-parts to your connected MySQL database: {e}")
     
    # Returning purchased items stored in MySQL
    print("Returning purchased-items stored in MySQL:", stored_purchased_items)
    return stored_purchased_items


def add_purchased_items_from_update_for_sqlite(purchased_items):
    """Add purchased parts into spare_parts to SQLite and MySQL databases"""

    stored_purchased_items = []

    for purchased_item in purchased_items:
        print("Received Purchased Items :", purchased_items)
        print("Unpacking the Received Purchased Items to store into spare_parts Table.")
        name, category, quantity, purchase_price, sale_price, total_price = purchased_item
        # Safely convert quantity to int, regardless of whether it was passed as a string or int
        quantity = int(quantity)

        # SQLite Connection
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()

        # Check if item already exists
        cursor_sqlite.execute("SELECT id FROM spare_parts WHERE name = ? AND category = ?", (name, category))
        existing_id = cursor_sqlite.fetchone()

        try:
            # Add into SQLite
            print("Now adding Purchased Items into spare-parts Table in MySQLite database")

            if existing_id:
                print("This item already exists, so just updating purchase and sale price")
                # Update the existing item information
                cursor_sqlite.execute("""
                    UPDATE spare_parts 
                    SET purchase_price = ?, sale_price = ?
                    WHERE id = ?
                """, (purchase_price, sale_price, existing_id))
                print("Data updated successfully, now appending in stored_purchased_items List")
                stored_purchased_items.append((existing_id, name, category, quantity, sale_price, total_price, purchase_price))
            else:
                # Insert as a new item
                print("Inserting as new Spare-Part")
                cursor_sqlite.execute("""
                    INSERT INTO spare_parts (name, category, purchase_price, sale_price)
                    VALUES (?, ?, ?, ?)
                """, (name, category, purchase_price, sale_price))
                print("Data stored successfully, now appending in stored_purchased_items List")
                stored_purchased_items.append((cursor_sqlite.lastrowid, name, category, quantity, sale_price, total_price, purchase_price,))

            print("Successfully added the Purchased Items into spare-parts to your connected SQLite database")
        except Exception as e:
            print(f"Error adding Purchased Items into spare-parts to your connected SQLite database: {e}")

        # Close SQLite Connection
        conn_sqlite.commit()
        conn_sqlite.close()
        
    # Returning un-duplicated stored purchased items from SQLite database
    print("Returning stored purchased-items data from SQLite:", stored_purchased_items)
    return stored_purchased_items



def add_purchased_items_from_update_for_mysql(purchased_items):
    """Add purchased parts into spare_parts to SQLite and MySQL databases"""

    stored_purchased_items = []

    for purchased_item in purchased_items:
        print("Received Purchased Items :", purchased_items)
        print("Unpacking the Received Purchased Items to store into spare_parts Table.")
        name, category, quantity, purchase_price, sale_price, total_price = purchased_item
        # Safely convert quantity to int, regardless of whether it was passed as a string or int
        quantity = int(quantity)

        # MySQL Connection
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db") 

        # Check if item already exists
        cursor_mysql.execute("SELECT id FROM spare_parts WHERE name = %s AND category = %s", (name, category))
        existing_id = cursor_mysql.fetchone()

        try:
            # Add into MySQL
            print("Now adding Purchased Items into spare-parts Table in MySQL database")

            if existing_id:
                print("This item already exists, so just updating purchase and sale price")
                # Update the existing item information
                cursor_mysql.execute("""
                    UPDATE spare_parts 
                    SET purchase_price = %s, sale_price = %s
                    WHERE id = %s
                """, (purchase_price, sale_price, existing_id))
                print("Data updated successfully, now appending in stored_purchased_items List")
                stored_purchased_items.append((existing_id, name, category, quantity, sale_price, total_price, purchase_price))
            else:
                # Insert as a new item
                print("Inserting as new Spare-Part")
                cursor_mysql.execute("""
                    INSERT INTO spare_parts (name, category, purchase_price, sale_price)
                    VALUES (%s, %s, %s, %s)
                """, (name, category, purchase_price, sale_price))
                print("Data stored successfully, now appending in stored_purchased_items List")
                stored_purchased_items.append((cursor_mysql.lastrowid, name, category, quantity, sale_price, total_price, purchase_price))

            print("Successfully added the Purchased Items into spare-parts to your connected SQLite database")
        except Exception as e:
            print(f"Error adding Purchased Items into spare-parts to your connected SQLite database: {e}")
        
        # Close MySQL Connection
        conn_mysql.commit()
        conn_mysql.close()

    # Returning un-duplicated stored purchased items in MySQL database
    print("Returning stored purchased-items data from MySQL:", stored_purchased_items)
    return stored_purchased_items



def update_part(part_id, name, category, purchase_price, sale_price):
    """Update a part to SQLite and MySQL databases"""

    try:
        # Update into SQLite
        print("Updating Spare-Part to your connected SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        cursor_sqlite.execute("UPDATE spare_parts SET name=?, category=?, purchase_price=?, sale_price=? WHERE id=?", (name, category, purchase_price, sale_price, part_id))
        conn_sqlite.commit()
        conn_sqlite.close()
        print("Spare-Part updated to your connected SQLite database successfully")
    except Exception as e:
        print(f"Error updating spare-part to your connected SQLite database: {e}")

    try:
        # Update into MySQL
        print("Updating Spare-Part to your connected MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db")  
        cursor_mysql.execute("UPDATE spare_parts SET name=%s, category=%s, purchase_price=%s, sale_price=%s WHERE id=%s", (name, category, purchase_price, sale_price, part_id))
        conn_mysql.commit()
        conn_mysql.close()
        print("Spare-Part updated to your connected MySQL database successfully")
    except Exception as e:
        print(f"Error updating spare-part to your connected MySQL database: {e}")




def delete_part(part_id):
    """Delete a part from SQLite and MySQL databases"""

    try:
        # Delete from SQLite
        print("Deleting Spare-Part to your connected SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        cursor_sqlite.execute("DELETE FROM spare_parts WHERE id=?", (part_id,))
        conn_sqlite.commit()
        conn_sqlite.close()
        print("Spare-Part deleted to your connected SQLite database successfully")
    except Exception as e:
        print(f"Error deleting spare-part to your connected SQLite database: {e}")


    try:
        # Delete from MySQL
        print("Deleting Spare-Part to your connected MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db")  
        cursor_mysql.execute("DELETE FROM spare_parts WHERE id=%s", (part_id,))
        conn_mysql.commit()
        conn_mysql.close()
        print("Spare-Part deleted to your connected MySQL database successfully")
    except Exception as e:
        print(f"Error deleting spare-part to your connected MySQL database: {e}")




