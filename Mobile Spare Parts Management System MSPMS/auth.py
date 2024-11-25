



# Users Authentication controller




from database import get_sqlite_connection, get_mysql_connection



def login(username, password):
    user_data = None

    # First try to connect SQLite offline local database, then online MySQL database
    print(f"Now Authenticating using the connected offline local SQLite Database")
    conn_sqlite = get_sqlite_connection()
    if conn_sqlite:
        try:
            cursor_sqlite = conn_sqlite.cursor()
            cursor_sqlite.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user_sqlite = cursor_sqlite.fetchone()
            conn_sqlite.close()

            if user_sqlite:
                user_data = {
                    'id': user_sqlite[0],
                    'username': user_sqlite[1],
                    'password': user_sqlite[2],
                    'role_id': user_sqlite[3],
                    'full_name': user_sqlite[4],
                }
                return user_data

        except Exception as sqlite_error:
            print(f"Error querying SQLite: {sqlite_error}")
            conn_sqlite.close()

    # Then try connect to MySQL if internet and Database Server is available
    print(f"Now Authenticating using the connected online MySQL Database if internet & database server available")
    conn_mysql = get_mysql_connection()
    if conn_mysql:
        try:
            cursor_mysql = conn_mysql.cursor(dictionary=True)
            # Below specify the name of your connected MySQL database to use for authentication
            cursor_mysql.execute("USE mspms_mysql_db")  
            cursor_mysql.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user_mysql = cursor_mysql.fetchone()
            conn_mysql.close()

            if user_mysql:
                user_data = {
                    'id': user_mysql[0],
                    'username': user_mysql[1],
                    'password': user_mysql[2],
                    'role_id': user_mysql[3],
                    'full_name': user_mysql[4],
                }
                return user_data

        except Exception as mysql_error:
            print(f"Error querying MySQL: {mysql_error}")
            conn_mysql.close()







def signup(username, password, full_name):

    user_created = false
   
    role_id = 1 
    cnic = ''
    gender = ''
    dob = ''
    address = ''

    # First try to connect SQLite offline local database, then online MySQL database
    print(f"Now Sign-Up using the connected offline local SQLite Database")
    conn_sqlite = get_sqlite_connection()

    if conn_sqlite:
        try:
            cursor_sqlite = conn_sqlite.cursor()
            cursor_sqlite.execute("INSERT INTO users (username, password, role_id, full_name, cnic, gender, dob, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (username, password, role_id, full_name, cnic, gender, dob, address))
            conn_sqlite.commit()
            conn_sqlite.close()
            user_created = true
            print("Succesfully User Sign-Up into your connected SQLite database")
            return user_created
        except Exception as sqlite_error:
            print(f"Error during sign-up into SQLite: {sqlite_error}")
            conn_sqlite.close()

    # Now try connect to MySQL if internet and Database Server is available
    print(f"Now Sign-Up using the connected online MySQL Database if internet & database server available")
    conn_mysql = get_mysql_connection()

    if conn_mysql:
        try:
            cursor_mysql = conn_mysql.cursor(dictionary=True)
            # Below specify the name of your connected MySQL database to use for authentication
            cursor_mysql.execute("USE mspms_mysql_db")  
            cursor_mysql.execute("INSERT INTO users (username, password, role_id, full_name, cnic, gender, dob, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (username, password, role_id, full_name, cnic, gender, dob, address))
            conn_mysql.commit()
            conn_mysql.close()
            user_created = true
            print("Succesfully User Sign-Up into your connected MySQL database")
            return user_created
        except Exception as mysql_error:
            print(f"Error during sign-up into MySQL: {mysql_error}")
            conn_mysql.close()





