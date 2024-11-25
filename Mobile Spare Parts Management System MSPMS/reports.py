


# Backend Controller 


# import io
from datetime import datetime, timedelta, date
import os
import sys
import pdfkit
from jinja2 import Environment, FileSystemLoader
from database import get_sqlite_connection, get_mysql_connection
import tkinter as tk
from tkinter import  messagebox



def fetch_all_reports():
    """Fetch all reports from SQLite and MySQL databases"""
    reports = []

    try:
        # Fetch from SQLite
        print("Now Fetching All Reports from your connected SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        cursor_sqlite.execute("SELECT report_name FROM reports")
        reports = cursor_sqlite.fetchall()
        conn_sqlite.close()
        print("Successfully fetched all reports from your connected SQLite database")
        print("Fetched Data from SQLite = ", reports)
    except Exception as e:
        print(f"Error fetching all reports from SQLite: {e}")

    try:
        # Fetch from MySQL
        print("Now Fetching All Reports from your connected MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        cursor_mysql.execute("USE mspms_mysql_db")
        cursor_mysql.execute("SELECT report_name FROM reports")
        reports = cursor_mysql.fetchall()
        conn_mysql.close()
        print("Successfully fetched all reports from your connected MySQL database")
        print("Fetched Data from MySQL = ", reports)
    except Exception as e:
        print(f"Error fetching all reports from MySQL: {e}")

    return reports



def get_oldest_date_from_databases():
    oldest_date_sqlite = None
    oldest_date_mysql = None
    
    # Fetch the oldest date from SQLite database
    
    try:
        print("Fetching oldest date of oldest transaction from SQLite Database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # Assuming the dates are stored in 'yyyy-mm-dd' format in SQLite
        cursor_sqlite.execute("SELECT MIN(date) FROM transactions")
        result_sqlite = cursor_sqlite.fetchone()
        
        if result_sqlite[0]:
            oldest_date_sqlite = result_sqlite[0]  # Keep it in 'yyyy-mm-dd' db-friendly format
            print("Oldest Transaction Date in SQLite= ", oldest_date_sqlite)
        
        conn_sqlite.close()
    except Exception as e:
        print(f"Error fetching oldest date from SQLite: {e}")
    
    # Fetch the oldest date from MySQL database
    try:
        print("Fetching oldest date of oldest transaction from MySQL Database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        cursor_mysql.execute("USE mspms_mysql_db")
        # Assuming the dates are stored in 'yyyy-mm-dd' format in MySQL
        cursor_mysql.execute("SELECT MIN(date) FROM transactions")
        result_mysql = cursor_mysql.fetchone()
        
        if result_mysql[0]:
            oldest_date_mysql = result_mysql[0]  # Keep it in 'yyyy-mm-dd' db-friendly format
            print("Oldest Transaction Date in MySQL= ", oldest_date_mysql)
        
        conn_mysql.close()
    except Exception as e:
        print(f"Error fetching oldest date from MySQL: {e}")

    # Checking and converting both dates to `date` for comparison
    if oldest_date_sqlite:
        if isinstance(oldest_date_sqlite, str):
            oldest_date_sqlite_obj = datetime.strptime(oldest_date_sqlite, '%Y-%m-%d').date()
        elif isinstance(oldest_date_sqlite, datetime):
            oldest_date_sqlite_obj = oldest_date_sqlite.date()
        else:
            oldest_date_sqlite_obj = oldest_date_sqlite
    else:
        oldest_date_sqlite_obj = None
        
    if oldest_date_mysql:
        if isinstance(oldest_date_mysql, str):
            oldest_date_mysql_obj = datetime.strptime(oldest_date_mysql, '%Y-%m-%d').date()
        elif isinstance(oldest_date_mysql, datetime):
            oldest_date_mysql_obj = oldest_date_mysql.date()
        else:
            oldest_date_mysql_obj = oldest_date_mysql
    else:
        oldest_date_mysql_obj = None   
    
    # Comparing and Determining the oldest date between SQLite and MySQL
    if oldest_date_sqlite_obj and oldest_date_mysql_obj:
        final_oldest_date = min(oldest_date_sqlite_obj, oldest_date_mysql_obj).strftime('%Y-%m-%d')
    elif oldest_date_sqlite_obj:
        final_oldest_date = oldest_date_sqlite_obj.strftime('%Y-%m-%d')
    elif oldest_date_mysql_obj:
        final_oldest_date = oldest_date_mysql_obj.strftime('%Y-%m-%d')
    else:
        # Fallback to a default date if no dates are found
        final_oldest_date = None
        
    if final_oldest_date:
        print("Final Oldest Date Returned (Database Format) = ", final_oldest_date)
        return final_oldest_date
    else:
        print("No dates found in transactions table in both databases.")
        return None





def fetch_report_data(start_date, end_date):
    """Fetch report data from SQLite and MySQL databases within a date range"""

    data = {
        "transactions": [],
        "transaction_items": [],
        "profit_loss": (0, 0),
        "user_transactions": []
    }
    
    try:
        # Fetch from SQLite
        print("Now Fetching Report Data from your connected SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        # Fetch transactions
        cursor_sqlite.execute(
            """
            SELECT 
                t.id, 
                t.date,
                t.time, 
                t.type, 
                u.username, 
                t.grand_total_price,
                t.paid_price,
                t.balance_price 
            FROM transactions t 
            JOIN users u ON t.user_id = u.id 
            WHERE t.date BETWEEN ? AND ?
            """, 
            (start_date, end_date)
        )
        transactions = cursor_sqlite.fetchall()
        # Convert the date column to 'dd-mm-yyyy' user-friendly format before storing
        for transaction in transactions:
            transaction_id, date, time, trans_type, username, grand_total_price, paid_price, balance_price = transaction
            # Convert the date to 'dd-mm-yyyy' format
            date_user_format = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
            # Append the modified transaction data to the transactions list
            data["transactions"].append({
                'id': transaction_id,
                'date': date_user_format,
                'time': time,
                'type': trans_type,
                'username': username,
                'grand_total_price': grand_total_price,
                'paid_price':  paid_price,
                'balance_price': balance_price 
            })
        # Fetch inventory (we assume this means transaction items in this context)
        cursor_sqlite.execute(
            """
            SELECT 
                t.id AS transaction_id,            
                ti.spare_part_name, 
                ti.spare_part_category, 
                ti.quantity,
                ti.purchase_price, 
                ti.sale_price, 
                ti.total_price
            FROM transaction_items ti 
            JOIN transactions t ON ti.transaction_id = t.id 
            WHERE t.date BETWEEN ? AND ?
            GROUP BY ti.spare_part_name, t.id
            """, 
            (start_date, end_date)
        )
        #data["inventory"] = cursor_sqlite.fetchall()
        inventory = cursor_sqlite.fetchall()
        data["transaction_items"] = inventory     
        
        # Fetch profit and loss
        cursor_sqlite.execute(
            """
            SELECT 
                SUM(ti.sale_price - ti.purchase_price) AS profit, 
                SUM(ti.purchase_price - ti.sale_price) AS loss 
            FROM transaction_items ti 
            JOIN transactions t ON ti.transaction_id = t.id 
            WHERE t.date BETWEEN ? AND ?
            """, 
            (start_date, end_date)
        )
        #data["profit_loss"] = cursor_sqlite.fetchone()
        profit_loss = cursor_sqlite.fetchone()
        data["profit_loss"] = {
            "profit": profit_loss[0] if profit_loss[0] else 0,
            "loss": profit_loss[1] if profit_loss[1] else 0
        }        
        # Fetch user transactions
        cursor_sqlite.execute(
            """
            SELECT 
                u.username, 
                COUNT(t.id) AS transaction_count 
            FROM transactions t 
            JOIN users u ON t.user_id = u.id 
            WHERE t.date BETWEEN ? AND ?
            GROUP BY u.username
            """, 
            (start_date, end_date)
        )
        user_transactions = cursor_sqlite.fetchall()
        data["user_transactions"] = user_transactions
        conn_sqlite.close()
        print("Successfully fetched report data from your connected SQLite database")
    except Exception as e:
        print(f"Error fetching report data from SQLite: {e}")
    
    try:
        # Fetch from MySQL
        print("Now Fetching Report Data from your connected MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        cursor_mysql.execute("USE mspms_mysql_db")
        
        # Fetch transactions
        cursor_mysql.execute(
            """
            SELECT 
                t.id, 
                t.date,
                t.time, 
                t.type, 
                u.username, 
                t.grand_total_price,
                t.paid_price,
                t.balance_price                  
            FROM transactions t 
            JOIN users u ON t.user_id = u.id 
            WHERE t.date BETWEEN %s AND %s
            """, 
            (start_date, end_date)
        )
        transactions = cursor_mysql.fetchall()
        print("Fetched Transactions =", transactions)
        # Convert the date column to 'dd-mm-yyyy' user-friendly format before storing
        for transaction in transactions:
            transaction_id, date_value, time, trans_type, username, grand_total_price, paid_price, balance_price = transaction
            # Convert the date to 'dd-mm-yyyy' format
            # Check if the 'date_value' variable is an instance of 'date' or 'datetime' object
            if isinstance(date_value, (date, datetime)):
                date_user_format = date_value.strftime('%d-%m-%Y')
            else:
                # Handle the case where date might still be a string (in case of unexpected input)
                date_user_format = datetime.strptime(date_value, '%Y-%m-%d').strftime('%d-%m-%Y')
            #date_user_format = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
            # Append the modified transaction data to the transactions list
            data["transactions"].append({
                'id': transaction_id,
                'date': date_user_format,
                'time': time,
                'type': trans_type,
                'username': username,
                'grand_total_price': grand_total_price,
                'paid_price':  paid_price,
                'balance_price': balance_price                 
            })
        # Fetch inventory (we assume this means transaction items in this context)
        cursor_mysql.execute(
            """
            SELECT 
                t.id AS transaction_id,
                ti.spare_part_name, 
                ti.spare_part_category, 
                ti.quantity,
                ti.purchase_price, 
                ti.sale_price, 
                ti.total_price 
            FROM transaction_items ti 
            JOIN transactions t ON ti.transaction_id = t.id 
            WHERE t.date BETWEEN %s AND %s
            GROUP BY ti.spare_part_name, t.id
            """, 
            (start_date, end_date)
        )
        #data["inventory"] = cursor_mysql.fetchall()
        inventory = cursor_mysql.fetchall()
        data["transaction_items"] = inventory 
        # Fetch profit and loss
        cursor_mysql.execute(
            """
            SELECT 
                SUM(ti.sale_price - ti.purchase_price) AS profit, 
                SUM(ti.purchase_price - ti.sale_price) AS loss 
            FROM transaction_items ti 
            JOIN transactions t ON ti.transaction_id = t.id 
            WHERE t.date BETWEEN %s AND %s
            """, 
            (start_date, end_date)
        )
        #data["profit_loss"] = cursor_mysql.fetchone()
        profit_loss = cursor_mysql.fetchone()
        data["profit_loss"] = {
            "profit": profit_loss[0] if profit_loss[0] else 0,
            "loss": profit_loss[1] if profit_loss[1] else 0
        }  
        # Fetch user transactions
        cursor_mysql.execute(
            """
            SELECT 
                u.username, 
                COUNT(t.id) AS transaction_count 
            FROM transactions t 
            JOIN users u ON t.user_id = u.id 
            WHERE t.date BETWEEN %s AND %s
            GROUP BY u.username
            """, 
            (start_date, end_date)
        )
        #data["user_transactions"] = cursor_mysql.fetchall()
        user_transactions = cursor_mysql.fetchall()
        data["user_transactions"] = user_transactions    
        conn_mysql.close()
        print("Successfully fetched report data from your connected MySQL database")
    except Exception as e:
        print(f"Error fetching report data from MySQL: {e}")
    
    print("Returned Fetched Data of selected interval = ", data)
    return data
    


def create_pdf_report(report_data, start_date, end_date, html_template_path):
    """Create a PDF report from the provided data"""

    # Convert start_date and end_date from strings data-type to datetime objects 
    # Before changing from DB-Format to User-Format to use in file name
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    current_datetime = datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.time()
    
    # Setting Report Name using the selected dates and the current date/time
    report_name = f"Report_from_{start_date.strftime('%d-%m-%Y')}_to_{end_date.strftime('%d-%m-%Y')}_on_{current_date.strftime('%d-%m-%Y')}_at_{current_time.strftime('%H-%M-%S')}.pdf"    

    # Project root/base directory path
    #project_root = os.path.dirname(os.path.abspath(__file__))
    # Above OR below
    if getattr(sys, 'frozen', False):
        BASE_DIR = os.path.dirname(sys.executable)
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(os.path.dirname(html_template_path)))
    template = env.get_template(os.path.basename(html_template_path))
 
    # Calculate absolute path for the static image
    logo_path = os.path.abspath(os.path.join(BASE_DIR, 'assets', 'app_logo_1.png'))    

    # Render the HTML template with fetched report_data
    html_content = template.render(
        report_name=report_name,
        logo_path=logo_path,
        start_date=start_date.strftime('%d-%m-%Y'),
        end_date=end_date.strftime('%d-%m-%Y'),
        current_date=current_date.strftime('%d-%m-%Y'),
        current_time=current_time.strftime('%H-%M-%S'),        
        transactions=report_data.get('transactions', []),
        transaction_items=report_data.get('transaction_items', []),
        profit_loss=report_data.get('profit_loss', {}),
        user_transactions=report_data.get('user_transactions', []),
    )

    # Local Path where report files saved locally on computer
    report_local_path =  os.path.join(BASE_DIR, "local_report_files", report_name)

    # Define the relative path to wkhtmltopdf
    #project_root = os.path.dirname(os.path.abspath(__file__))
    wkhtmltopdf_path = os.path.join(BASE_DIR, 'dependencies', 'wkhtmltopdf', 'bin', 'wkhtmltopdf.exe')

    #wkhtmltopdf_path = 'wkhtmltopdf/bin/wkhtmltopdf.exe'

    # Ensure the file exists
    if not os.path.isfile(wkhtmltopdf_path):
        raise FileNotFoundError(f"'{wkhtmltopdf_path}' not found.")
    
    # Configuration for pdfkit
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    # enable-local-file-access Option
    options = {
        'enable-local-file-access': None
    }

    # Convert HTML to PDF using pdfkit and save to a file
    try:
        # Convert HTML to PDF and save to a file
        pdfkit.from_string(html_content, report_local_path, configuration=config, options=options)
        print(f"PDF successfully created and saved at {report_local_path}")
    except OSError as e:
        print(f"wkhtmltopdf reported an error: {str(e)}")
        raise
    
    # Saving reports on databases
    # In SQLite
    try:
        print("Now Saving Report to your connected SQLite database")
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        print("Value of Current Date = ", current_date)
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        cursor_sqlite.execute('''INSERT INTO reports (date, report_name, file_path) VALUES (?, ?, ?)''', (current_date, report_name, report_local_path))
        conn_sqlite.commit()
        conn_sqlite.close()
    except Exception as e:
        print(f"Error saving report to MySQL: {e}")        
    # In MySQL
    try:
        print("Now Saving Report to your connected MySQL database")
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        print("Value of Current Date = ", current_date)
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        cursor_mysql.execute("USE mspms_mysql_db")
        # Convert report data to binary data
        def convert_to_binary_data(file_path):
            with open(file_path, 'rb') as file:
                binary_data = file.read()
            return binary_data
        # Prepare the data
        binary_data = convert_to_binary_data(report_local_path)
        cursor_mysql.execute("INSERT INTO reports (date, report_name, file_data, file_path) VALUES (%s, %s, %s, %s)",
                             (current_date, report_name, binary_data, report_local_path))
        conn_mysql.commit()
        conn_mysql.close()
        print("Successfully saved report to your connected MySQL database")
    except Exception as e:
        print(f"Error saving report to MySQL: {e}")

    # Return
    return report_local_path






def get_report_file_from_local(report_name):
    """Get the Path of report file from SQLite and MySQL databases"""
    print(f"Report Name: {report_name} (Type: {type(report_name)})")  # Debugging statement

    try:
        # Get content from SQLite
        print("Now fetching Path of report file from your connected SQLite database")
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        cursor_sqlite.execute("SELECT file_path FROM reports WHERE report_name = ?", (report_name,))
        fetched_report_file = cursor_sqlite.fetchone()
        conn_sqlite.close()
        if fetched_report_file:
            print("Successfully fetched path of report file from your connected SQLite database")
            # Fetchone give result in tuple even it fetched only 1 person data
            # So get your data by using index in case you not want only 1 person data instead of all persons
            return fetched_report_file[0]  # Extract the string from the tuple, even it has 1 report_path            
    except Exception as e:
        print(f"Error fetching Path of report file from SQLite: {e}")

    try:
        # Get content from MySQL
        print("Now Fetching Path of report file from your connected MySQL database")
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        cursor_mysql.execute("USE mspms_mysql_db")
        cursor_mysql.execute("SELECT file_path FROM reports WHERE report_name = %s", (report_name,))
        fetched_report_file = cursor_mysql.fetchone()
        conn_mysql.close()
        if fetched_report_file:
            print("Successfully fetched Path of report file from your connected MySQL database")
            # Fetchone give result in tuple even it fetched only 1 person data
            # So get your data by using index in case you not want only 1 person data instead of all persons
            return fetched_report_file[0]  # Extract the string from the tuple, even it has 1 report_path
    except Exception as e:
        print(f"Error fetching Path of report file from MySQL: {e}")
   

    return None



def get_report_file_from_mysql(report_name):
    """Fetch the binary report data from MySQL database"""
    try:
        # Get content from SQLite
        print("Now fetching binary report file from your connected SQLite database")        
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        cursor_mysql.execute("USE mspms_mysql_db")
        cursor_mysql.execute("SELECT file_data FROM reports WHERE report_name = %s", (report_name,))
        report_data = cursor_mysql.fetchone()
        conn_mysql.close()
        if report_data:
            print("Successfully fetched binary report file from MySQL.")
            return report_data[0]  # Return the binary data
    except Exception as e:
        print(f"Error fetching binary report file from MySQL: {e}")
    
    return None



def delete_report(report_name):
    report_deleted = False

    # Delete from SQLite database
    try:
        conn_sqlite = get_sqlite_connection()
        cursor_sqlite = conn_sqlite.cursor()
        cursor_sqlite.execute("DELETE FROM reports WHERE report_name = ?", (report_name,))
        conn_sqlite.commit()
        if cursor_sqlite.rowcount > 0:
            report_deleted = True
            print(f"Report '{report_name}' deleted from SQLite database.")
            messagebox.showinfo("Success", "Successfully deleted the Selected Report file from SQLite database.")
        else:
            print(f"Report '{report_name}' not found in SQLite database. So it's Already deleted.")
            messagebox.showinfo("Success", "Selected Report not found in SQLite database. So It's Already deleted.")
        conn_sqlite.close()
    except Exception as e:
        print(f"Error deleting report from SQLite: {e}")
        tk.messagebox.showerror("Error", "Error deleting the selected report from SQLite: {e}")
    # Delete from MySQL database
    try:
        conn_mysql = get_mysql_connection()
        cursor_mysql = conn_mysql.cursor()
        cursor_mysql.execute("USE mspms_mysql_db")
        cursor_mysql.execute("DELETE FROM reports WHERE report_name = %s", (report_name,))
        conn_mysql.commit()
        if cursor_mysql.rowcount > 0:
            report_deleted = True
            print(f"Report '{report_name}' deleted from MySQL database.")
            messagebox.showinfo("Success", "Successfully deleted the Selected Report file from MySQL database.")
        else:
            print(f"Report '{report_name}' not found in MySQL database. So It's Already deleted.")
            messagebox.showinfo("Success", "Selected Report not found in MySQL database. So It's Already deleted.")
        conn_mysql.close()
    except Exception as e:
        print(f"Error deleting report from MySQL: {e}")
        tk.messagebox.showerror("Error", "Error deleting the selected report from MySQL: {e}")


    return report_deleted





