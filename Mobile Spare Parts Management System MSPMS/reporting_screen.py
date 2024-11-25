


# Frontend Screen - ReportingScreen.py



import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
from PIL import Image, ImageTk
from  tkcalendar import DateEntry
from datetime import datetime, date, timedelta
import webbrowser
from reports import fetch_all_reports, get_oldest_date_from_databases, fetch_report_data, create_pdf_report, get_report_file_from_local, get_report_file_from_mysql, delete_report


class ReportingScreen:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Manage Reports - MSPMS")
        self.root.geometry("840x510")
        self.root.minsize(840,510)
        self.root.maxsize(840,510)
        self.root.configure(bg="skyblue")
        self.clear_frame()
        self.create_widgets()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_widgets(self):
        
        # Title
        title_label = tk.Label(self.root, text="Manage Reports", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue")
        title_label.grid(row=0, column=0, padx=10, pady=(20,5), sticky="n")
        
        # Main Frame
        self.main_frame = tk.Frame(self.root, bg="skyblue")
        self.main_frame.grid(row=1, column=0, padx=(10,10), pady=(5,20), sticky="nsew")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        ### Generate Report Section
        self.generate_report_frame = tk.LabelFrame(self.main_frame, text="Generate Report", width=150, bg="skyblue", font=("Helvetica", 14), height=10)
        self.generate_report_frame.grid(row=0, column=0, padx=(20,10), pady=(20,15), sticky="nsew")

        # Dropdown Interval Period
        tk.Label(self.generate_report_frame, text="Select Interval:", bg="skyblue", font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=10, pady=(20,10))
        self.interval_combobox = ttk.Combobox(self.generate_report_frame, values=["Today","Last Day", "Last Week", "Last Month", "Last 3 Months", "Last 6 Months", "Last 9 Months", "Last Year", "All Time", "Custom"], font=("Helvetica", 12), state='readonly')
        self.interval_combobox.grid(row=0, column=1, padx=10, pady=(20,10))
        self.interval_combobox.bind("<<ComboboxSelected>>", self.on_interval_select)
        
        # OR Label
        or_label = tk.Label(self.generate_report_frame, text="OR", font=("Helvetica", 12,), fg="red", bg="skyblue").grid(row=1, column=0, columnspan=2, padx=(40,40), pady=(15,15), sticky="nsew")

        # Custom Interval Period
        self.start_date_label = tk.Label(self.generate_report_frame, text="Start Date:", bg="skyblue", font=("Helvetica", 11, "bold"))
        self.start_date_label.grid(row=2, column=0, padx=10, pady=(10,10), sticky="w")
        self.start_date_entry = DateEntry(self.generate_report_frame, font=("Helvetica", 12), width=20, state='disabled', date_pattern='dd/mm/yyyy')
        self.start_date_entry.grid(row=2, column=1, padx=10, pady=(10,10),)

        self.end_date_label = tk.Label(self.generate_report_frame, text="End Date:", bg="skyblue", font=("Helvetica", 11, "bold"))
        self.end_date_label.grid(row=3, column=0, padx=10, pady=(6,10), sticky="w")
        self.end_date_entry = DateEntry(self.generate_report_frame, font=("Helvetica", 12), width=20, state='disabled', date_pattern='dd/mm/yyyy')
        self.end_date_entry.grid(row=3, column=1, padx=10, pady=(6,10))

        # Generate Report Button
        self.generate_button = tk.Button(self.generate_report_frame, text="Generate Report", font=("Helvetica", 12), fg="white", bg="green", command=self.generate_report, width=10,)
        self.generate_button.grid(row=4, column=0, columnspan=2, padx=(80,80), pady=(20,30), sticky="nsew")

        ### Existing Reports Section
        self.existing_reports_frame = tk.LabelFrame(self.main_frame, text="Existing Reports", width=50, bg="skyblue", font=("Helvetica", 14), height=10)
        self.existing_reports_frame.grid(row=0, column=1, padx=(10,20), pady=(20,15), sticky="nsew")
        # Frame
        listbox_frame = tk.Frame(self.existing_reports_frame, width=50)
        listbox_frame.grid(row=0, column=0, padx=10, pady=(20,20))
        # Scrollbar
        self.vertical_scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        self.vertical_scrollbar.grid(row=0, column=1, sticky='ns')
        self.horizontal_scrollbar = tk.Scrollbar(listbox_frame, orient=tk.HORIZONTAL)
        self.horizontal_scrollbar.grid(row=1, column=0, sticky='ew')
        # Listbox
        self.reports_listbox = tk.Listbox(listbox_frame, font=("Helvetica", 10), height=8, width=50, yscrollcommand=self.vertical_scrollbar.set, xscrollcommand=self.horizontal_scrollbar.set)
        self.reports_listbox.grid(row=0, column=0)
        # Configure scrollbar to control Listbox
        self.vertical_scrollbar.config(command=self.reports_listbox.yview)
        self.horizontal_scrollbar.config(command=self.reports_listbox.xview)
        # ListBox Content 
        self.reports_listbox.bind("<<ListboxSelect>>", self.on_report_select)
        # ListBox Content Selection Tracker
        self.selected_report_name = None
        self.main_frame.bind("<FocusOut>", self.reset_report_selection)

        # Creating a new frame for buttons of existing reports section
        self.buttons_frame = tk.Frame(self.existing_reports_frame, bg="skyblue")
        self.buttons_frame.grid(row=1, column=0, columnspan=2, pady=(15,15))
        # Buttons
        self.view_button = tk.Button(self.buttons_frame, text="View", font=("Helvetica", 12), fg="white", bg="#007bff", command=self.view_report, state='disabled', width=10,)
        self.view_button.pack(side=tk.LEFT, padx=5)
        self.download_button = tk.Button(self.buttons_frame, text="Download", font=("Helvetica", 12), fg="black", bg="#ffc107", command=self.download_report, state='disabled', width=10,)
        self.download_button.pack(side=tk.LEFT, padx=5)
        # Show the Delete button to all Users except user role 'salesman'
        if(self.user['role_id'] != 2): 
            self.delete_button = tk.Button(self.buttons_frame, text="Delete", font=("Helvetica", 12), fg="white", bg="red", command=self.delete_report, state='disabled', width=10,)
            self.delete_button.pack(side=tk.LEFT, padx=5)
        else:
            self.delete_button = None  # Set to None for 'Salesman' to avoid errors

        # Back Button Frame Section
        self.back_button_frame = tk.Frame(self.root, bg="skyblue")
        self.back_button_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(5,5))
        # Buttons Images
        # Path to Project Root/Base directory
        if getattr(sys, 'frozen', False):
            # PyInstaller executable base path
            BASE_DIR = os.path.dirname(sys.executable)
        else:
            # Script base path
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # Creating final path
        back_btn_path = os.path.join(BASE_DIR, "assets", "back_arrow.png")
        icon_back_arrow_image = Image.open(back_btn_path)
        icon_back_arrow_image = icon_back_arrow_image.resize((25,25), Image.LANCZOS) 
        icon_back_arrow_photo = ImageTk.PhotoImage(icon_back_arrow_image) 
        # Keep a reference to the image
        self.icon_back_arrow_photo = icon_back_arrow_photo  
        # Button
        self.back_button = tk.Button(self.back_button_frame, image=icon_back_arrow_photo, text="Back", width=80, height=30, compound="left", anchor="w", padx=10, font=("Helvetica", 12), fg="black", bg="#ECF0F1", command=self.back_to_dashboard_button,).grid(row=0, column=1, columnspan=2, padx=(5,30), sticky="nsew")

        # Load reports
        self.fetch_all_reports()


    def back_to_dashboard_button(self):
        self.clear_frame()
        from admin_dashboard_screen import AdminDashboardScreen
        from salesman_dashboard_screen import SalesmanDashboardScreen
        if(self.user['role_id'] == 1):
            AdminDashboardScreen(self.root, self.user)
        else:
            SalesmanDashboardScreen(self.root, self.user)        


    def on_interval_select(self, event):
        interval = self.interval_combobox.get()
        if interval == "Custom":
            self.start_date_entry.config(state='normal')
            self.end_date_entry.config(state='normal')
            # Bind the start_date_entry selection event to update the end_date_entry in real time
            self.start_date_entry.bind("<<DateEntrySelected>>", self.update_end_date_options)

        else:
            self.start_date_entry.config(state='disabled')
            self.end_date_entry.config(state='disabled')

    def update_end_date_options(self, event):
        selected_start_date = self.start_date_entry.get_date()
        today = datetime.now().date()

        if selected_start_date == today:
            # Disable end_date_entry completely
            self.end_date_entry.config(state='disabled')
        else:
            # Allow only dates between selected_start_date + 1 day and today
            self.end_date_entry.config(state='normal', mindate=selected_start_date + timedelta(days=1), maxdate=today)


    def generate_report(self):
        interval = self.interval_combobox.get()
        if interval == "Custom":
            start_date = self.start_date_entry.get_date()
            print("Custom start date selected (Database Format) = ", start_date) # format yyyy-mm-dd is db friendly
            end_date = self.end_date_entry.get_date()
            print("Custom end date selected (Database Format) = ", end_date) # format yyyy-mm-dd is db friendly
        else:
            current_datetime = datetime.now()
            end_date = current_datetime.date() # format yyyy-mm-dd is db-friendly
            print("Interval end date selected (Database Format) = ", end_date)
            if interval == "Today":
                start_date = end_date - timedelta(days=0) # format yyyy-mm-dd is db-friendly
                print("Interval start date selected (Database Format) = ", start_date)
            elif interval == "Last Day":
                start_date = end_date - timedelta(days=1) # format yyyy-mm-dd is db-friendly
                print("Interval start date selected (Database Format) = ", start_date)
            elif interval == "Last Week":
                start_date = end_date - timedelta(weeks=1) # format yyyy-mm-dd is db-friendly
                print("Interval start date selected (Database Format) = ", start_date)
            elif interval == "Last Month":
                start_date = end_date - timedelta(days=30) # format yyyy-mm-dd is db-friendly
                print("Interval start date selected (Database Format) = ", start_date)
            elif interval == "Last 3 Months":
                start_date = end_date - timedelta(days=90) # format yyyy-mm-dd is db-friendly
                print("Interval start date selected (Database Format) = ", start_date)
            elif interval == "Last 6 Months":
                start_date = end_date - timedelta(days=180) # format yyyy-mm-dd is db-friendly
                print("Interval start date selected (Database Format) = ", start_date)
            elif interval == "Last 9 Months":
                start_date = end_date - timedelta(days=270) # format yyyy-mm-dd is db-friendly
                print("Interval start date selected (Database Format) = ", start_date)
            elif interval == "Last Year":
                start_date = end_date - timedelta(days=365) # format yyyy-mm-dd is db-friendly
                print("Interval start date selected (Database Format) = ", start_date)
            elif interval == "All Time":
                # Fetch the oldest date from both SQLite and MySQL databases
                start_date = get_oldest_date_from_databases() # format yyyy-mm-dd is db-friendly
                print("Interval start date selected (Database Format) = ", start_date)
                if start_date == None:
                    print("Since no transactions existed, so we can't fetch report-data and generate report.")
                    # Show error message
                    tk.messagebox.showerror("Error", f"Since no transactions existed, so we can't fetch report-data and generate report.")
                    # Re-display the main screen
                    self.create_widgets()  # Ensure this method is called to refresh the UI
                    return

        # Convert Final Selected dates from db-friendly format (yyyy-mm-dd) to user-friendly format (dd-mm-yyyy)
        start_date_user_format = None 
        end_date_user_format = None
        if isinstance(start_date, str):
            # First, convert string to datetime object
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            start_date_user_format = start_date_obj.strftime('%d-%m-%Y')
            print(f"Start Date (User Friendly) = {start_date_user_format}")
        else:
            print("Start date is None or not in expected format.")        
        if isinstance(end_date, datetime):
            end_date_user_format = end_date.strftime('%d-%m-%Y')
        elif isinstance(end_date, date):  # If end_date is a date object
            end_date_user_format = datetime(end_date.year, end_date.month, end_date.day).strftime('%d-%m-%Y')
        print("Final Selected Intervals (User Format): Start =", start_date_user_format, " End = ", end_date_user_format)

        # Fetch report data based on the selected date range interval
        print("Now Fetching Report Data for selected interval")
        report_data = fetch_report_data(start_date, end_date)
        print("All received Returned Report Data of Transactions attribute only = ", report_data["transactions"])
        transactions_dates = [transaction['date'] for transaction in report_data["transactions"]]
        print("All received Returned Report Data of Transactions attribute with column Date only = ", transactions_dates)

        # Path to your HTML template file
        html_template_path = 'report_template.html'

        # Create PDF report using the fetched data and HTML template
        print("Now Creating PDF Report using fetched data")
        pdf_file_path = create_pdf_report(report_data, start_date, end_date, html_template_path)

        # Show success message
        messagebox.showinfo("Success", f"Report generated and saved locally in folder 'local_report_files' and also in MySQL Database if it was connected successfully")

        # Fetch all reports
        self.fetch_all_reports()

        # Refreshing and again creating screen
        self.create_widgets()

    def fetch_all_reports(self):
        self.reports_listbox.delete(0, tk.END)  # Clear the listbox first
        reports = fetch_all_reports()
        for report_tuple in reports:
            if report_tuple:  # Check if report is not empty
                report_name = report_tuple[0]  # Extract the report name from the tuple
                self.reports_listbox.insert(tk.END, report_name)  # Insert the report_name string into the listbox

    def on_report_select(self, event):
        selected_report = self.reports_listbox.curselection()
        if selected_report:
            self.selected_report_name = self.reports_listbox.get(selected_report)
            self.view_button.config(state='normal')
            self.download_button.config(state='normal')
            # Check if delete_button exists or not before configuring it
            if self.delete_button:
                self.delete_button.config(state='normal')
        else:
            self.view_button.config(state='disabled')
            self.download_button.config(state='disabled')
            # Check if delete_button exists or not before disabling it
            if self.delete_button:
                self.delete_button.config(state='disabled')

    def reset_report_selection(self, event):
        if self.selected_report_name:
            self.selected_report_name = None
            self.view_button.config(state='disabled')
            self.download_button.config(state='disabled')
            self.delete_button.config(state='disabled')
            # Check if delete_button exists before disabling it
            if self.delete_button:
                self.delete_button.config(state='disabled')
            self.reports_listbox.selection_clear(0, tk.END)


    def view_report(self):
        selected_report = self.reports_listbox.curselection()
        if selected_report:
            print("Now Viewing the Selected Report")
            selected_report_name = self.reports_listbox.get(selected_report)
            # Must verify selected_report_name is string type or not
            print("Selected Report Type = ", {type(selected_report_name)} )
            # Calling backend method 
            report_file_path = get_report_file_from_local(selected_report_name)  
            print("The returned path of report file is = ", report_file_path)

            # If File not exist locally
            if not os.path.exists(report_file_path):
                tk.messagebox.showerror("Error", "The report file does not exist locally. But now we will open report file from MySQL if it's connected now")
                # Fetch the binary data from MySQL if local file doesn't exist
                report_data = get_report_file_from_mysql(selected_report_name)  # Call Backend Method
                print("Returned Binary Report File Data = ", report_data)
                if report_data:
                    # Save the binary data as a local file
                    with open(report_file_path, 'wb') as file:
                        file.write(report_data)
                    # Open the newly saved file in the default PDF viewer
                    webbrowser.open(report_file_path)
                else:
                    tk.messagebox.showerror("Error","Failed to retrieve the report file_data from MySQL.")
                return      
            if report_file_path is None:
                tk.messagebox.showerror("Error", "Failed to retrieve the report file_path from both databases or it is null ")
                return        
            # If file exist locally, Open that file using its path in a default PDF viewer
            webbrowser.open(report_file_path)
            messagebox.showinfo("Success", f"Successfully Opened the selected Report file")
            print("Successfully Opened the selected Report file")
        else:
            tk.messagebox.showerror("Error", "Select the Report to View.")
            print("Error - Select the Report to View.")
            return



    def download_report(self):
        selected_report = self.reports_listbox.curselection()
        if selected_report:
            print("Now Downloading the Selected Report")
            selected_report_name = self.reports_listbox.get(selected_report)
            # Must verify selected_report_name is string type or not
            print("Selected Report Type = ", {type(selected_report_name)} )
            # Calling backend method
            report_file_path = get_report_file_from_local(selected_report_name) 
            print("The returned path of report file is = ", report_file_path)

            # Step 1: Check if the report file exists locally
            if report_file_path and os.path.exists(report_file_path):
                # If the file exists locally, read its content
                with open(report_file_path, "rb") as file:
                    # Reading all data of file present at path "report_file__path", then save this data to "report_data"
                    report_data = file.read() 
            # Step 2: If the file doesn't exist locally, fetch it's binary data from MySQL
            else:
                tk.messagebox.showerror("Error", "Failed to create downloadable file from local file. But now we will create downloadable file from MySQL if it's connected now")                
                # Fetch report binary data from MySQL
                report_data= get_report_file_from_mysql(selected_report_name)  # Calling backend method
                if report_data is None:
                    tk.messagebox.showerror("Error", "Failed to retrieve the report content from MySQL.")
                    return
            # Step 3: Prompt user to save the report file, either report_data coming from local or MySQL Database
            project_root = os.path.dirname(os.path.abspath(__file__))
            default_report_files_path = os.path.abspath(os.path.join(project_root, 'local_report_files')) 
            # Save File DialogBox 
            save_path = filedialog.asksaveasfilename(initialdir=default_report_files_path, initialfile=selected_report_name, defaultextension=".pdf", filetypes=[
                ("PDF file", "*.pdf")
            ])
            # Creating a file from fetched 'report_data' and save it selected desired 'save_path' from dialogBox
            if save_path:
                with open(save_path, "wb") as file:
                    file.write(report_data)
                messagebox.showinfo("Success", "Successfully downloaded the selected Report file")
                print("Successfully downloaded the selected Report file")
        else:
            tk.messagebox.showerror("Error", "Select the Report to Download.")
            print("Error - Select the Report to Download.")
            return



    
    def delete_report(self):
        selected_report = self.reports_listbox.curselection()
        if selected_report:
            print("Now Deleting the Selected Report")
            selected_report_name = self.reports_listbox.get(selected_report)
            print("Selected Report Type = ", {type(selected_report_name)} )  
            # Calling backend method           
            report_deleted = delete_report(selected_report_name)
            # Refreshing the screen and display the latest all reports
            self.fetch_all_reports()  
        else:
            tk.messagebox.showerror("Error", "Select the Report to Delete.")
            print("Error - Select the Report to Delete.")
            return




# Tkinter application setup
if __name__ == "__main__":
    root = tk.Tk()
    # user =   # user-data was already passing from admin dashboard to reporting screen
    app = ReportingScreen(root, user)
    root.mainloop()




