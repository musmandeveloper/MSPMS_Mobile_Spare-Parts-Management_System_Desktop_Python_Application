


# Transactions controller, Backend Function


# Import packages and libraries
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import get_sqlite_connection, get_mysql_connection
from inventory import add_purchased_items_from_update_for_sqlite
from inventory import add_purchased_items_from_update_for_mysql


def fetch_transactions():
    """Fetch transactions from SQLite and MySQL databases"""
    
    transactions = []
    # Dictionary to track (date,time) pairs with index keys, to avoid duplicate transactions 
    # even their IDs in both database are different, until date time is same then it means both 
    # are same transaction, So we find duplicates based on Date Time of each transaction
    seen_transactions = {} 

    try:
        # SQLite Connection
        print("Now fetching transactions from your connected SQLite Database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # Fetch Transactions
        cursor_sqlite.execute(
        """
            SELECT t.id, t.date, t.time, t.type, u.username AS username, t.grand_total_price, t.paid_price, t.balance_price
            FROM transactions t
            JOIN users u ON t.user_id = u.id
        """)
        sqlite_transactions = cursor_sqlite.fetchall()
        if not sqlite_transactions:
            print("No transactions table data found in SQLite database.")
        else:    
            print("Transactions Table fetched data: ", sqlite_transactions)
            # Fetch Transactions Items
            for idx, transaction in enumerate(sqlite_transactions):
                print("Transaction tuple inside unpacking loop:", transaction)
                if len(transaction) != 8:
                    print(f"Skipping transaction due to incorrect data: {transaction}")
                    continue
                transaction_id, date, time, type, user_id, grand_total_price, paid_price, balance_price = transaction
                if transaction_id in seen_transactions:
                    print(f"Skipping duplicate transaction with ID {transaction_id}  Bcz it's already fetched from MySQL")
                    continue  # Skip if already added
                # Store date and time of this sqlite fetched transaction in the seen_transactions dictionary
                seen_transactions[idx] = (date,time) # Note date time will be in DB Formats
                print("Now we will fetch data from transaction_items table")
                cursor_sqlite.execute(
                """
                    SELECT spare_part_id, spare_part_name, quantity, purchase_price, sale_price, total_price 
                    FROM transaction_items 
                    WHERE transaction_id = ?
                """, (transaction_id,))
                items = cursor_sqlite.fetchall()
                print(f"Items Fetched Data against transaction id {transaction_id}:", items)
                item_names, item_quantities, item_purchase_prices, item_sale_prices, item_total_prices = [], [], [], [], []
                for item in items:
                    item_names.append(item[1])
                    item_quantities.append(item[2])
                    item_purchase_prices.append(item[3])
                    item_sale_prices.append(item[4])
                    item_total_prices.append(item[5])
                # Converting date from database-friendly format 'yyyy-mm-dd' to user-friendly format 'dd-mm-yyyy' just before appending
                date_user_format = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
                transactions.append({
                    'date': date_user_format,
                    'time': time,
                    'id': transaction_id,
                    'user_id': user_id,
                    'type': type,
                    'item_names': item_names,
                    'item_quantities': item_quantities,
                    'item_purchase_prices': item_purchase_prices,
                    'item_sale_prices': item_sale_prices,
                    'item_total_prices': item_total_prices,
                    'grand_total_price': grand_total_price,
                    'paid_price': paid_price, 
                    'balance_price': balance_price
                })
            print("Successfully fetched all transactions from your connected SQLite database")
        conn_sqlite.close()
    except Exception as e:
        print(f"Error fetching transactions from your connected SQLite database: {e}")

    try:
        # MySQL Connection
        print("Now fetching transactions from your connected MySQL Database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        cursor_mysql.execute("USE mspms_mysql_db")
        cursor_mysql.execute(
        """
            SELECT t.id, t.date, t.time, t.type, u.username AS username, t.grand_total_price, t.paid_price, t.balance_price  
            FROM transactions t
            JOIN users u ON t.user_id = u.id
        """)
        mysql_transactions = cursor_mysql.fetchall()
        if not mysql_transactions:
            print("No transactions table data found in MySQL database.")
        else:
            print("Transactions Table fetched data: ", mysql_transactions)
            # Fetch Transactions Items
            for transaction in mysql_transactions:
                print("Transaction tuple inside unpacking loop:", transaction)
                if len(transaction) != 8:
                    print(f"Skipping transaction due to incorrect data: {transaction}")
                    continue
                transaction_id, date, time, type, user_id, grand_total_price, paid_price, balance_price = transaction
                # Normalize date and time values
                date = date.strftime('%Y-%m-%d')  # Convert MySQL datetime.date to string
                time = str(time)  # Convert MySQL timedelta to string
                # It exactly match all fields value, then consider it is already in seen_transactions
                #if transaction_id in seen_transactions:
                    #print(f"Skipping duplicate transaction with ID {transaction_id} in MySQL Bcz it's already fetched from SQLite")
                    #continue  # Skip if already added
                # Check if this (date, time) pair already exists in seen_transactions
                if any((date,time) == dt for dt in seen_transactions.values()):
                    print(f"Skipping duplicate transaction with Date: {date} and Time: {time} fetched from MySQL as it's already fetched from SQLite")
                    continue  # Skip next all code and go back to above loop if date,time are matched
                print("Now we will fetch data from transaction_items table")
                cursor_mysql.execute(
                """
                    SELECT spare_part_id, spare_part_name, quantity, purchase_price, sale_price, total_price 
                    FROM transaction_items 
                    WHERE transaction_id = %s
                """, (transaction_id,))
                items = cursor_mysql.fetchall()
                print(f"Items Fetched Data against transaction id {transaction_id}:", items)
                item_names, item_quantities, item_purchase_prices, item_sale_prices, item_total_prices = [], [], [], [], []
                for item in items:
                    item_names.append(item[1])
                    item_quantities.append(item[2])
                    item_purchase_prices.append(item[3])
                    item_sale_prices.append(item[4])
                    item_total_prices.append(item[5])
                # Converting date from database-friendly format 'yyyy-mm-dd' to user-friendly format 'dd-mm-yyyy' just before appending
                date_user_format = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')                
                transactions.append({
                    'date': date_user_format,
                    'time': time,
                    'id': transaction_id,
                    'user_id': user_id,
                    'type': type,
                    'item_names': item_names,
                    'item_quantities': item_quantities,
                    'item_purchase_prices': item_purchase_prices,
                    'item_sale_prices': item_sale_prices,
                    'item_total_prices': item_total_prices,
                    'grand_total_price': grand_total_price,
                    'paid_price': paid_price, 
                    'balance_price': balance_price
                })
            print("Successfully fetched all transactions from your connected MySQL database")
        conn_mysql.close()
    except Exception as e:
        print(f"Error fetching transactions from your connected MySQL database: {e}")

    # Returning Overall Final data without duplicates from both databases
    print("Returning Fetched Transactions data (without duplicate transactions) = ", transactions)
    return transactions


def record_transaction_sqlite(items, user_id, transaction_type, grand_total_price, paid_price, balance_price):
    """Record a transaction in SQLite database with proper logic for sale and purchase"""
    
    current_datetime = datetime.now()
    current_date = current_datetime.date().strftime('%Y-%m-%d')
    current_time = current_datetime.time().strftime('%H:%M:%S')

    try:
        # SQLite Connection
        print("Now recording transaction into your connected SQLite Database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()

        # Record Transaction
        print("Adding data into transactions table")
        cursor_sqlite.execute(
        """
            INSERT INTO transactions (date, time, user_id, type, grand_total_price, paid_price, balance_price) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (current_date, current_time, user_id, transaction_type, grand_total_price, paid_price, balance_price))
        transaction_id = cursor_sqlite.lastrowid
        print("Successfully data added into transactions table")
        # Record Transaction Items
        print("Items to be inserted:", items)
        for item in items:
            if len(item) == 7:
                part_id, name, category, quantity, sale_price, total_price, purchase_price = item
                # Handle "Sale" transaction_type by checking and adding item in spare_parts
                if transaction_type == "Sale":
                    # First, check if the part exists in the spare_parts table
                    cursor_sqlite.execute(
                        """
                        SELECT id FROM spare_parts 
                        WHERE name = ? AND category = ?
                        """, (name, category)
                    )
                    result = cursor_sqlite.fetchone()
                    if result:
                        # If the part exists, get the existing item_id
                        spare_part_id = result[0]
                        print(f"Existing spare part found with ID {spare_part_id}")
                    else:
                        # If not, insert the new part and get its ID
                        cursor_sqlite.execute(
                            """
                            INSERT INTO spare_parts (name, category, purchase_price, sale_price) 
                            VALUES (?, ?, ?, ?)
                            """, (name, category, purchase_price, sale_price)
                        )
                        spare_part_id = cursor_sqlite.lastrowid
                        print(f"New spare part received with ID={part_id} is now stored in SQLite with ID={spare_part_id}")
                    # Now use this spare_part_id for the transaction_items table
                    cursor_sqlite.execute(
                        """
                        INSERT INTO transaction_items (transaction_id, spare_part_id, spare_part_name, spare_part_category, quantity, purchase_price, sale_price, total_price) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (transaction_id, spare_part_id, name, category, quantity, purchase_price, sale_price, total_price)
                    )
                    print(f"Successfully added item with ID {spare_part_id} into transaction_items table")
                else:
                    # For "Purchase" transaction type, keep the original logic
                    cursor_sqlite.execute(
                        """
                        INSERT INTO transaction_items (transaction_id, spare_part_id, spare_part_name, spare_part_category, quantity, purchase_price, sale_price, total_price) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (transaction_id, part_id, name, category, quantity, purchase_price, sale_price, total_price)
                    )
                    print("Successfully data added into transaction_items table")
            else:
                print("Skipping item due to incorrect format:", item)
        # Commit the transaction
        conn_sqlite.commit()
        conn_sqlite.close()
        print(f"{transaction_type.capitalize()} recorded successfully in SQLite database")
    except Exception as e:
        print(f"Error recording {transaction_type} in SQLite database: {e}")



def record_transaction_mysql(items, user_id, transaction_type, grand_total_price, paid_price, balance_price):
    """Record a transaction in MySQL databases"""

    current_datetime = datetime.now()
    current_date = current_datetime.date().strftime('%Y-%m-%d')
    current_time = current_datetime.time().strftime('%H:%M:%S')

    try:
        # MySQL Connection
        print("Now recording/adding transaction into your connected MySQL Database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Use MySQL database
        cursor_mysql.execute("USE mspms_mysql_db")
        # Record Transaction
        print("Adding data into transactions table")
        cursor_mysql.execute(
            """
            INSERT INTO transactions (date, time, user_id, type, grand_total_price, paid_price, balance_price) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (current_date, current_time, user_id, transaction_type, grand_total_price, paid_price, balance_price)
        )
        transaction_id = cursor_mysql.lastrowid
        print("Successfully data added into transactions table")
        # Record Transaction Items
        print("Items to be inserted:", items)
        for item in items:
            if len(item) == 7:
                part_id, name, category, quantity, sale_price, total_price, purchase_price = item
                # Handle "Sale" transaction_type by checking and adding item in spare_parts
                if transaction_type == "Sale":
                    # First, check if the part exists in the spare_parts table
                    cursor_mysql.execute(
                        """
                        SELECT id FROM spare_parts 
                        WHERE name = %s AND category = %s
                        """, (name, category)
                    )
                    result = cursor_mysql.fetchone()
                    if result:
                        # If the part exists, get the existing item_id
                        spare_part_id = result[0]
                        print(f"Existing spare part found with ID {spare_part_id}")
                    else:
                        # If not, insert the new part and get its ID
                        cursor_mysql.execute(
                            """
                            INSERT INTO spare_parts (name, category, purchase_price, sale_price) 
                            VALUES (%s, %s, %s, %s)
                            """, (name, category, purchase_price, sale_price)
                        )
                        spare_part_id = cursor_mysql.lastrowid
                        print(f"New spare part received with ID={part_id} is now stored in MySQL with ID={spare_part_id}")
                    # Now use this spare_part_id for the transaction_items table
                    cursor_mysql.execute(
                        """
                        INSERT INTO transaction_items (transaction_id, spare_part_id, spare_part_name, spare_part_category, quantity, purchase_price, sale_price, total_price) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (transaction_id, spare_part_id, name, category, quantity, purchase_price, sale_price, total_price)
                    )
                    print(f"Successfully added item with ID {spare_part_id} into transaction_items table")
                else:
                    # For "Purchase" transaction type, keep the original logic
                    cursor_mysql.execute(
                        """
                        INSERT INTO transaction_items (transaction_id, spare_part_id, spare_part_name, spare_part_category, quantity, purchase_price, sale_price, total_price) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (transaction_id, part_id, name, category, quantity, purchase_price, sale_price, total_price)
                    )
                    print("Successfully data added into transaction_items table")
            else:
                print("Skipping item due to incorrect format:", item)

        conn_mysql.commit()
        conn_mysql.close()
        print(f"{transaction_type.capitalize()} recorded successfully in MySQL database")

    except Exception as e:
        print(f"Error recording {transaction_type} in MySQL database: {e}")



def fetch_transaction_old_data(transaction_id):
    """Fetch specific transaction details from SQLite and MySQL databases based on transaction_id."""
    
    transaction_data = {}
    seen_transaction_ids = set()  # To track added transaction IDs

    try:
        # SQLite Connection
        print(f"Fetching transactions table data for selected ID {transaction_id} from SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # Fetch specific Transaction from SQLite
        cursor_sqlite.execute(
        """
            SELECT t.id, t.date, t.time, t.type, u.id AS user_id, u.username AS username, t.grand_total_price, t.paid_price, t.balance_price
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            WHERE t.id = ?
        """, (transaction_id,))
        sqlite_transaction = cursor_sqlite.fetchone()
        if not sqlite_transaction:
            print(f"No transaction found with ID {transaction_id} in SQLite database.")
        else:
            print(f"Transaction data fetched from SQLite: {sqlite_transaction}")
            # Fetch Transaction Items from SQLite
            cursor_sqlite.execute(
            """
                SELECT spare_part_id, spare_part_name, spare_part_category, quantity, purchase_price, sale_price, total_price 
                FROM transaction_items 
                WHERE transaction_id = ?
            """, (transaction_id,))
            items = cursor_sqlite.fetchall()
            print(f"Items fetched for transaction ID {transaction_id} from SQLite: {items}")
            item_ids, item_statuses, item_names, item_categories, item_quantities, item_purchase_prices, item_sale_prices, item_total_prices = [], [], [], [], [], [], [], []
            for item in items:
                item_ids.append(item[0])
                item_statuses.append('Old')                
                item_names.append(item[1])
                item_categories.append(item[2])
                item_quantities.append(item[3])
                item_purchase_prices.append(item[4])
                item_sale_prices.append(item[5])
                item_total_prices.append(item[6])
            # Converting date from database format 'yyyy-mm-dd' to user-friendly format 'dd-mm-yyyy'
            date_user_format = datetime.strptime(sqlite_transaction[1], '%Y-%m-%d').strftime('%d-%m-%Y')
            transaction_data = {
                'id': sqlite_transaction[0],
                'date': date_user_format,
                'time': sqlite_transaction[2],
                'type': sqlite_transaction[3],
                'user_id': sqlite_transaction[4],
                'username': sqlite_transaction[5],
                'item_ids': item_ids,
                'item_statuses': item_statuses,                
                'item_names': item_names,
                'item_categories': item_categories,
                'item_quantities': item_quantities,
                'item_purchase_prices': item_purchase_prices,
                'item_sale_prices': item_sale_prices,
                'item_total_prices': item_total_prices,
                'grand_total_price': sqlite_transaction[6],
                'paid_price': sqlite_transaction[7], 
                'balance_price': sqlite_transaction[8]
            }
            seen_transaction_ids.add(transaction_id)
        conn_sqlite.close()
    except Exception as e:
        print(f"Error fetching transaction from SQLite database: {e}")

    try:
        # MySQL Connection
        print(f"Fetching transactions table data for selected ID {transaction_id} from MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Fetch specific Transaction from MySQL
        cursor_mysql.execute("USE mspms_mysql_db")
        cursor_mysql.execute(
        """
            SELECT t.id, t.date, t.time, t.type, u.id AS user_id, u.username AS username, t.grand_total_price, t.paid_price, t.balance_price  
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            WHERE t.id = %s
        """, (transaction_id,))
        mysql_transaction = cursor_mysql.fetchone()
        if not mysql_transaction:
            print(f"No transaction found with ID {transaction_id} in MySQL database.")
        else:
            print(f"Transaction data fetched from MySQL: {mysql_transaction}")
            # Fetch Transaction Items from MySQL
            cursor_mysql.execute(
            """
                SELECT spare_part_id, spare_part_name, spare_part_category, quantity, purchase_price, sale_price, total_price 
                FROM transaction_items 
                WHERE transaction_id = %s
            """, (transaction_id,))
            items = cursor_mysql.fetchall()
            print(f"Items fetched for transaction ID {transaction_id} from MySQL: {items}")
            item_ids, item_statuses, item_names, item_categories, item_quantities, item_purchase_prices, item_sale_prices, item_total_prices = [], [], [], [], [], [], [], []
            for item in items:
                item_ids.append(item[0])
                item_statuses.append('Old')
                item_names.append(item[1])
                item_categories.append(item[2])
                item_quantities.append(item[3])
                item_purchase_prices.append(item[4])
                item_sale_prices.append(item[5])
                item_total_prices.append(item[6])
            # Converting date from database format 'yyyy-mm-dd' to user-friendly format 'dd-mm-yyyy'
            date_user_format = datetime.strptime(mysql_transaction[1], '%Y-%m-%d').strftime('%d-%m-%Y')
            transaction_data = {
                'id': mysql_transaction[0],                
                'date': date_user_format,
                'time': mysql_transaction[2],
                'type': mysql_transaction[3],                
                'user_id': mysql_transaction[4],
                'username': mysql_transaction[5],
                'item_ids': item_ids,
                'item_statuses': item_statuses,
                'item_names': item_names,
                'item_categories': item_categories,
                'item_quantities': item_quantities,
                'item_purchase_prices': item_purchase_prices,
                'item_sale_prices': item_sale_prices,
                'item_total_prices': item_total_prices,
                'grand_total_price': mysql_transaction[6],
                'paid_price': mysql_transaction[7], 
                'balance_price': mysql_transaction[8]
            }
            seen_transaction_ids.add(transaction_id)
        conn_mysql.close()
    except Exception as e:
        print(f"Error fetching transaction from MySQL database: {e}")

    print(f"Returning fetched transaction data for ID {transaction_id} = {transaction_data}")
    return transaction_data



def update_transaction(transaction_id, date, time, transaction_type, user_id, items, grand_total_price, paid_price, balance_price):
    """Update a transaction in SQLite and MySQL databases"""
    
    # Step 0: Convert date from user-friendly (dd-mm-yyy) to database format (yyyy-mm-dd)
    date_db_format = datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
    print("Converted received date from User-Format to DB-Format = ", date_db_format)

    try:
        print("Updating transaction data in transactions and transaction_items Tables (SQLite)")
        # SQLite Connection
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # Step 1: Get the transaction_id based on date and time
        cursor_sqlite.execute(
        """
            SELECT id FROM transactions 
            WHERE date = ? AND time = ?
        """, (date_db_format, time))
        matched_transaction_id_in_sqlite = cursor_sqlite.fetchone()
        # Getting single value from fetched-data tuple of one value
        if not matched_transaction_id_in_sqlite:
            print(f"This transaction {transaction_id} with this Date={date_db_format} and Time={time} was not already in transactions table in SQLite so we also can't Update it in MySQLite")
            # Don't use 'return' here because we still want to check next try-except block of mysql instead of existing whole function
        else:
            matched_transaction_id_in_sqlite = matched_transaction_id_in_sqlite[0]  # Extract the id from the tuple
            print(f"Transaction with received ID={transaction_id} is matched in SQLite with Transaction ID={matched_transaction_id_in_sqlite}")  
            # Step 1: Update the main transaction
            print("Now Updating transaction data in transactions Table")
            cursor_sqlite.execute(
            """
                UPDATE transactions 
                SET date = ?, time = ?, user_id = ?, type = ?, grand_total_price = ?, paid_price = ?, balance_price = ?
                WHERE id = ?
            """, (date_db_format, time, user_id, transaction_type, grand_total_price, paid_price, balance_price, matched_transaction_id_in_sqlite))
            print(f"Successfully updated transaction ID={transaction_id} data in transactions Table")
            # Step 2: Group items based on status ("Old" or "New")
            print("Grouping items into Old and New groups")
            old_items = [item for item in items if item[1] == 'Old']  # Grouping old items
            print("Old Items group = ", old_items)
            new_items = [item for item in items if item[1] == 'New']  # Grouping new items
            print("New Items group = ", new_items)
            # Step 3: Update old items in transaction_items
            # Step 3.1: Update old items in transaction_items
            print("Now Updating Old items either sale or purchase, in transaction_items Table")
            for item in old_items:
                part_id, old_status, name, category, quantity, purchase_price, sale_price, total_price = item
                print(f"Old Item {part_id} data received: ID={part_id} Status={old_status} Name={name} Category={category} Quantity={quantity} P.P={purchase_price} S.P={sale_price} T.P={total_price}")
                # Update existing transaction items
                cursor_sqlite.execute(
                """
                    UPDATE transaction_items 
                    SET quantity = ?, purchase_price = ?, sale_price = ?, total_price = ? 
                    WHERE transaction_id = ? AND spare_part_id = ?
                """, (quantity, purchase_price, sale_price, total_price, matched_transaction_id_in_sqlite, part_id))        
            print(f"Successfully updated all Old Items of transaction Id={transaction_id} in transaction_items")
            # Step 3.2: Delete all old items that are now not part of this transaction ID anymore
            # Create a list of part_ids from old_items that are still part of this Transaction ID
            old_item_ids_still_part = [item[0] for item in old_items]
            # Delete all old items in transaction_items are not in received old_item_ids and also whose date and time in transactions table is same as we now received date time 
            print("Deleting old items not part of the updated transaction in SQLite ...")
            cursor_sqlite.execute(
            """
                DELETE FROM transaction_items 
                WHERE transaction_id = ? AND spare_part_id NOT IN ({})
            """.format(",".join("?" * len(old_item_ids_still_part))),
            (matched_transaction_id_in_sqlite, *old_item_ids_still_part))
            conn_sqlite.commit()
            print(f"Successfully deleted all old items transaction_items that now not in the transaction ID={transaction_id} anymore")
            # Step 4: Handle new items of purchase and sale transaction type
            print("Now Grouping New Items data into Sale and Purchase groups")
            new_sale_items = [item for item in new_items if transaction_type == 'Sale']  # New sale items
            print("New Sale Items group = ", new_sale_items)
            new_purchase_items = [item for item in new_items if transaction_type == 'Purchase']  # New purchase items
            print("New Purchase Items group = ", new_purchase_items)
            # Step 4.1: Insert new sale items into transaction_items
            if new_sale_items:
                print("Now Inserting New sale items data in transaction_items Table")
                for new_sale_item in new_sale_items:
                    part_id, new_status, name, category, quantity, purchase_price, sale_price, total_price = new_sale_item
                    # First Check if the item already exists in spare_parts or not
                    cursor_sqlite.execute(
                        """
                        SELECT id FROM spare_parts
                        WHERE name = ? AND category = ?
                        """, (name, category)
                    )
                    result = cursor_sqlite.fetchone()
                    if result:
                        # If item exists, get its that spare_part_id that is already in sqlite
                        spare_part_id_sqlite = result[0]
                        print(f"This spare part with received Id={part_id} was already in spare_parts table with ID {spare_part_id_sqlite} in SQLite")
                    else:
                        # If item does not exist, insert it into spare_parts and get that newly assigned part ID
                        cursor_sqlite.execute(
                            """
                            INSERT INTO spare_parts (name, category, purchase_price, sale_price)
                            VALUES (?, ?, ?, ?)
                            """, (name, category, purchase_price, sale_price)
                        )
                        spare_part_id_sqlite = cursor_sqlite.lastrowid
                        print(f"This spare part with received Id={part_id} was not in spare_parts table, So we added it and its new assigned ID is {spare_part_id_sqlite} in SQLite")
                    # Insert into transaction_items using its old ID or newly assigned IDspare_part_id_sqlite
                    cursor_sqlite.execute(
                        """
                        INSERT INTO transaction_items (transaction_id, spare_part_id, spare_part_name, spare_part_category, quantity, purchase_price, sale_price, total_price) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (matched_transaction_id_in_sqlite, spare_part_id_sqlite, name, category, quantity, purchase_price, sale_price, total_price)
                    )
                # Commit and close MySQL connection
                conn_sqlite.commit()
                conn_sqlite.close()
                print(f"Successfully updated Transaction ID = {transaction_id} in SQLite database")
                messagebox.showinfo("Success", f"Successfully updated Transaction ID = {transaction_id} in SQLite database")             
            # Step 4.2: Insert new purchase items into both spare_parts and transaction_items Tables
            if new_purchase_items:
                print("Now Inserting New purchase items data in both spare_parts and transaction_items Tables")
                # Remove 'null' and 'New' columns from each new purchase item
                cleaned_new_purchase_items = [item[2:] for item in new_purchase_items]
                # Commit and close connection before calling add_purchased_items
                conn_sqlite.commit()
                conn_sqlite.close()
                print("Closed SQLite connection before calling add_purchased_items")
                stored_new_purchased_items = add_purchased_items_from_update_for_sqlite(cleaned_new_purchase_items)
                print("Returned data after saving purchased items in inventory", stored_new_purchased_items)
                # Re-open SQLite connection to insert into transaction_items
                print("Re-open SQLite connection after calling add_purchased_items, to store received data in transaction_items Table")
                conn_sqlite = get_sqlite_connection()
                cursor_sqlite = conn_sqlite.cursor()
                # After Storing in spare_parts Table, Now store them in transaction_items Table
                for stored_new_purchased_item in stored_new_purchased_items:
                    part_id, name, category, quantity, sale_price, total_price, purchase_price = stored_new_purchased_item
                    # Insert into transaction_items
                    cursor_sqlite.execute(
                    """
                        INSERT INTO transaction_items (transaction_id, spare_part_id, spare_part_name, spare_part_category, quantity, purchase_price, sale_price, total_price)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (matched_transaction_id_in_sqlite, part_id, name, category, quantity, purchase_price, sale_price, total_price))
                print(f"Successfully inserted all New Purchase Items of Transaction ID={transaction_id} into transaction_items Table")
                # close sqlite connection
                conn_sqlite.commit()
                conn_sqlite.close()
                print(f"Successfully updated Transaction ID = {transaction_id} in SQLite database")
                messagebox.showinfo("Success", f"Successfully updated Transaction ID = {transaction_id} in SQLite database")
    except Exception as e:
        print(f"Error updating Transaction ID = {transaction_id} in SQLite database: {e}")


    try:
        print("Updating transaction data in transactions and transaction_items Tables (MySQL)")
        # MySQL Connection
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Below specify the name of your connected MySQL database
        cursor_mysql.execute("USE mspms_mysql_db") 
        # Step 1: Get the transaction_id based on date and time
        cursor_mysql.execute(
        """
            SELECT id FROM transactions 
            WHERE date = %s AND time = %s
        """, (date_db_format, time))
        matched_transaction_id_in_mysql = cursor_mysql.fetchone()
        # Getting single value from fetched-data tuple of one value
        if not matched_transaction_id_in_mysql:
            print(f"This transaction {transaction_id} with this Date={date_db_format} and Time={time} was not already in transactions table in MySQL so we also can't Update it in MySQL")
            return # Exit from whole function if that transaction is not existed in both database which we want to update
        else:
            matched_transaction_id_in_mysql = matched_transaction_id_in_mysql[0]  # Extract the id from the tuple
            print(f"Transaction with received ID={transaction_id} is matched in MySQL with Transaction ID={matched_transaction_id_in_mysql}")
            # Step 1: Update the main transaction 
            print("Now Updating transaction data in transactions Table")
            cursor_mysql.execute(
            """
                UPDATE transactions 
                SET date = %s, time = %s, user_id = %s, type = %s, grand_total_price = %s, paid_price = %s, balance_price = %s
                WHERE id = %s
            """, (date_db_format, time, user_id, transaction_type, grand_total_price, paid_price, balance_price, matched_transaction_id_in_mysql))
            print(f"Successfully updated transaction ID={transaction_id} data in transactions Table")
            # Step 2: Group items based on status ("Old" or "New")
            print("Now Grouping items into Old and New groups")
            old_items = [item for item in items if item[1] == 'Old']  # Grouping old items
            print("Old Items group = ", old_items)
            new_items = [item for item in items if item[1] == 'New']  # Grouping new items
            print("New Items group = ", new_items)
            # Step 3: Update old items in transaction_items
            # Step 3.1: Update old items in transaction_items
            print("Now Updating Old items either Sale or Purchase in transaction_items Table")
            for item in old_items:
                part_id, old_status, name, category, quantity, purchase_price, sale_price, total_price = item
                # Update existing transaction items
                cursor_mysql.execute(
                """
                    UPDATE transaction_items 
                    SET quantity = %s, purchase_price = %s, sale_price = %s, total_price = %s 
                    WHERE transaction_id = %s AND spare_part_id = %s
                """, (quantity, purchase_price, sale_price, total_price, matched_transaction_id_in_mysql, part_id))
            print(f"Successfully updated all Old Items of transaction ID={transaction_id} in transaction_items")
            # Step 3.2: Delete all old items that are now not part of this transaction ID anymore
            # Create a list of part_ids from old_items that are still part of this Transaction ID
            old_item_ids_still_part = [item[0] for item in old_items]
            # Delete all old items in transaction_items are not in received old_item_ids and also whose date and time in transactions table is same as we now received date time 
            print("Deleting old items not part of the updated transaction in MySQL...")
            delete_query_mysql = """
                DELETE FROM transaction_items 
                WHERE transaction_id = %s AND spare_part_id NOT IN ({})
            """.format(",".join(["%s"] * len(old_item_ids_still_part)))
            # Execute the query with the correct parameters
            cursor_mysql.execute(delete_query_mysql, (matched_transaction_id_in_mysql, *old_item_ids_still_part))
            conn_mysql.commit()
            print(f"Successfully deleted all old items transaction_items that now not in the transaction ID={transaction_id} anymore")        
            # Step 4: Handle new items of purchase and sale transaction type 
            print("Now Grouping New Items data into Sale and Purchase groups")
            new_sale_items = [item for item in new_items if transaction_type == 'Sale']  # New sale items
            print("New Sale Items group = ", new_sale_items)
            new_purchase_items = [item for item in new_items if transaction_type == 'Purchase']  # New purchase items
            print("New Purchase Items group = ", new_purchase_items)
            # Step 4.1: Insert new sale items into transaction_items 
            if new_sale_items:
                print("Now Inserting New sale items data in transaction_items Table")
                for new_sale_item in new_sale_items:
                    part_id, new_status, name, category, quantity, purchase_price, sale_price, total_price = new_sale_item
                    # First Check if the item already exists in spare_parts or not
                    cursor_mysql.execute(
                        """
                        SELECT id FROM spare_parts
                        WHERE name = %s AND category = %s
                        """, (name, category)
                    )
                    result = cursor_mysql.fetchone()
                    if result:
                        # If item exists, get its that spare_part_id that is already in sqlite
                        spare_part_id_mysql = result[0]
                        print(f"This spare part with received Id={part_id} was already in spare_parts table with ID {spare_part_id_mysql} in MySQL")
                    else:
                        # If item does not exist, insert it into spare_parts and get that newly assigned part ID
                        cursor_mysql.execute(
                            """
                            INSERT INTO spare_parts (name, category, purchase_price, sale_price)
                            VALUES (%s, %s, %s, %s)
                            """, (name, category, purchase_price, sale_price)
                        )
                        spare_part_id_mysql = cursor_mysql.lastrowid
                        print(f"This spare part with received Id={part_id} was not in spare_parts table, So we added it and its new assigned ID is {spare_part_id_mysql} in MySQL")
                    # Insert into transaction_items using its old ID or newly assigned IDspare_part_id_sqlite
                    cursor_mysql.execute(
                        """
                        INSERT INTO transaction_items (transaction_id, spare_part_id, spare_part_name, spare_part_category, quantity, purchase_price, sale_price, total_price) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (matched_transaction_id_in_mysql, spare_part_id_mysql, name, category, quantity, purchase_price, sale_price, total_price)
                    )
                print(f"Successfully inserted all New Sale Items of Transaction ID={transaction_id} into transaction_items Table")
                # Commit and close MySQL connection
                conn_mysql.commit()
                conn_mysql.close()
                print(f"Successfully updated Transaction ID={transaction_id} in MySQL database")
                messagebox.showinfo("Success", f"Successfully updated Transaction ID = {transaction_id} in MySQL database")
            # Step 4.2: Insert new purchase items into both spare_parts and transaction_items Tables
            if new_purchase_items:
                print("Now Inserting New purchase items data in both spare_parts and transaction_items Tables")
                cleaned_new_purchase_items = [item[2:] for item in new_purchase_items]  # Remove 'null' and 'New' columns
                # Commit and close MySQL connection before calling add_purchased_items
                conn_mysql.commit()
                conn_mysql.close()
                print("Closed MySQL connection before calling add_purchased_items")
                stored_new_purchased_items = add_purchased_items_from_update_for_mysql(cleaned_new_purchase_items)
                print("Returned data after saving purchased items in inventory (MySQL)", stored_new_purchased_items)
                # Re-open MySQL connection to insert into transaction_items
                print("Re-open MySQL connection after calling add_purchased_items, to store received data in transaction_items Table")
                conn_mysql = get_mysql_connection()
                cursor_mysql = conn_mysql.cursor()
                # Below specify the name of your connected MySQL database
                cursor_mysql.execute("USE mspms_mysql_db") 
                # After storing in spare_parts Table, Now store them in transaction_items Table (MySQL)
                for stored_new_purchased_item in stored_new_purchased_items:
                    part_id, name, category, quantity, sale_price, total_price, purchase_price = stored_new_purchased_item
                    # Insert into transaction_items (MySQL)
                    cursor_mysql.execute(
                    """
                        INSERT INTO transaction_items (transaction_id, spare_part_id, spare_part_name, spare_part_category, quantity, purchase_price, sale_price, total_price)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (matched_transaction_id_in_mysql, part_id, name, category, quantity, purchase_price, sale_price, total_price))
                print(f"Successfully inserted all New Purchase Items of Transaction ID={transaction_id} into transaction_items Table")
                # Commit and close MySQL connection
                conn_mysql.commit()
                conn_mysql.close()
                print(f"Successfully updated Transaction ID={transaction_id} in MySQL database")
                messagebox.showinfo("Success", f"Successfully updated Transaction ID = {transaction_id} in MySQL database")
    except Exception as e:
        print(f"Error updating Transaction ID={transaction_id} in MySQL database: {e}")



def delete_transaction(transaction_id):
    """Delete a transaction from SQLite and MySQL databases"""
    
    try:
        # SQLite Connection
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # Delete Transaction Items and Update Spare Parts Stock
        cursor_sqlite.execute(
        """
            SELECT spare_part_id, quantity, type 
            FROM transaction_items 
            JOIN transactions ON transaction_items.transaction_id = transactions.id 
            WHERE transaction_id = ?
        """, (transaction_id,))
        # Must add trailing comma in parameters in SELECT Query even if there is only one parameters like (transaction_id,)
        # In multiple parameters case then between them there must be a comma like  (parameter1, parameter2)
        # Otherwise error will come unsupported parameters type, bcz we SQL Query expect tuple a parameters
        items = cursor_sqlite.fetchall()
        for part_id, quantity, transaction_type in items:
            if transaction_type == 'Sale':
                cursor_sqlite.execute("UPDATE spare_parts SET stock = stock + ? WHERE id = ?", (quantity, part_id))
            elif transaction_type == 'Purchase':
                cursor_sqlite.execute("UPDATE spare_parts SET stock = stock - ? WHERE id = ?", (quantity, part_id))
        cursor_sqlite.execute("DELETE FROM transaction_items WHERE transaction_id = ?", (transaction_id,))
        cursor_sqlite.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn_sqlite.commit()
        conn_sqlite.close()
        print(f"Transaction deleted successfully from SQLite database")
    except Exception as e:
        print(f"Error deleting transaction from SQLite database: {e}")


    try:
        # MySQL Connection
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        # Delete Transaction Items and Update Spare Parts Stock
        cursor_mysql.execute("USE mspms_mysql_db")
        cursor_mysql.execute(
        """
            SELECT spare_part_id, quantity, type 
            FROM transaction_items 
            JOIN transactions ON transaction_items.transaction_id = transactions.id 
            WHERE transaction_id = %s
        """, (transaction_id,))
        # Must add trailing comma in parameters in SELECT Query even if there is only one parameters like (transaction_id,)
        # In multiple parameters case then between them there must be a comma like  (parameter1, parameter2)
        # Otherwise error will come unsupported parameters type, bcz we SQL Query expect tuple a parameters
        items = cursor_mysql.fetchall()
        for part_id, quantity, transaction_type in items:
            if transaction_type == 'Sale':
                cursor_mysql.execute("UPDATE spare_parts SET stock = stock + %s WHERE id = %s", (quantity, part_id))
            elif transaction_type == 'Purchase':
                cursor_mysql.execute("UPDATE spare_parts SET stock = stock - %s WHERE id = %s", (quantity, part_id))
        cursor_mysql.execute("DELETE FROM transaction_items WHERE transaction_id = %s", (transaction_id,))
        cursor_mysql.execute("DELETE FROM transactions WHERE id = %s", (transaction_id,))
        conn_mysql.commit()
        conn_mysql.close()
        print(f"Successfully deleted Transaction ID = {transaction_id} from MySQL database")
    except Exception as e:
        print(f"Error deleting Transaction ID = {transaction_id} from MySQL database: {e}")




