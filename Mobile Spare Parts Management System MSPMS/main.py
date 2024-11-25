

import os
import subprocess
import sys
import tkinter as tk
from splash_screen import SplashScreen
from initial_data import insert_initial_data 


# Get the base directory, whether running as a script or as a PyInstaller executable
def get_base_dir():
    if getattr(sys, 'frozen', False):
        # PyInstaller executable base path
        return os.path.dirname(sys.executable)
    else:
        # Script base path
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()


def setup_database():
    db_folder = os.path.join(BASE_DIR, 'local_database')
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)
    
    db_file = os.path.join(db_folder, 'mspms_sqlite_db.sqlite')
    if not os.path.exists(db_file):
        # Run your database setup code
        subprocess.run([sys.executable, os.path.join(BASE_DIR, 'database.py')], check=True)

  
def insert_initial_data():
    initial_data_marker = os.path.join(BASE_DIR, 'initial_data_inserted.txt')
    if not os.path.exists(initial_data_marker):
        subprocess.run([sys.executable, os.path.join(BASE_DIR, 'initial_data.py')], check=True)


def setup_report_folder():
    report_folder = os.path.join(BASE_DIR, 'local_report_files')
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)



def main():
    setup_database()
    insert_initial_data()
    setup_report_folder()
    root = tk.Tk()
    SplashScreen(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()



