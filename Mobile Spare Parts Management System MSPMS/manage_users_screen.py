



# Manage Users Screen



import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date
from  tkcalendar import DateEntry
import sqlite3
import mysql.connector
from users import fetch_users, add_user, update_user, delete_user
from roles import fetch_roles
from utils import validate_input


class ManageUsersScreen:
    def __init__(self, root, user):
        self.root = root
        self.root.title("MSPMS - Manage Users")
        self.root.geometry("900x500")
        self.root.minsize(900, 500)
        self.root.maxsize(900, 500)
        self.root.config(bg="skyblue")
        self.user = user
        self.clear_frame()
        self.create_widgets()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_widgets(self):

        # Dashboard Title
        title = tk.Label(self.root, text="Manage Users", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue")
        title.pack(pady=20)

        # Search Frame
        search_frame = tk.Frame(self.root, bg="skyblue")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search:", bg="skyblue", fg="black", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Helvetica", 14), bg="white", fg="black", insertbackground="black")
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_user_screen, bg="#007bff", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Clear Search", command=self.load_users, bg="#6c757d", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)

        # TreeView Table

        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white", font=("Helvetica", 12))
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background="blue", foreground="black")
        style.map('Treeview', background=[('selected', '#007bff')])

        table_frame = tk.Frame(self.root, bg="skyblue")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=40)

        self.user_list = ttk.Treeview(table_frame, columns=("ID", "Username", "Password", "Role", "Full Name", "CNIC", "Gender", "DOB", "Address"), show='headings')
        self.user_list.heading("ID", text="ID")
        self.user_list.heading("Username", text="Username")
        self.user_list.heading("Password", text="Password")
        self.user_list.heading("Role", text="Role")
        self.user_list.heading("Full Name", text="Full Name")
        self.user_list.heading("CNIC", text="CNIC")
        self.user_list.heading("Gender", text="Gender")
        self.user_list.heading("DOB", text="DOB")
        self.user_list.heading("Address", text="Address")

        for col in self.user_list["columns"]:
            self.user_list.column(col, width=120, minwidth=100, stretch=tk.NO)

        self.user_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.user_list.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.user_list.xview)
        self.user_list.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)

        self.user_list.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Button Frame
        button_frame = tk.Frame(self.root, bg="skyblue")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Back", command=self.back_to_dashboard_button, bg="#2ECC71", fg="black", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Add User", command=self.add_user_screen, bg="#007bff", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Update User", command=self.update_user_screen, bg="#ffc107", fg="black", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Delete User", command=self.delete_user_screen, bg="#dc3545", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)

        self.load_users()

    def back_to_dashboard_button(self):
        self.clear_frame()
        from admin_dashboard_screen import AdminDashboardScreen
        AdminDashboardScreen(self.root, self.user)

    def load_users(self):
        for i in self.user_list.get_children():
            self.user_list.delete(i)
        users = fetch_users()  # Call the backend method and receive the returned data 
        for user in users:
            self.user_list.insert('', 'end', values=user)

    def add_user_screen(self):
        add_user_window = tk.Toplevel(self.root)
        add_user_window.geometry("400x550")
        add_user_window.minsize(400, 550)
        add_user_window.maxsize(400, 550)        
        add_user_window.title("Add User")
        add_user_window.config(bg="skyblue")

        # Title - Centered
        title = tk.Label(add_user_window, text="Add User", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue")
        title.pack(pady=20)  

        # Frame for Form Fields
        form_frame = tk.Frame(add_user_window, bg="skyblue")
        form_frame.pack(pady=10) 

        # Form Fields inside form_frame
        labels = ["Username", "Password", "Role", "Full Name", "CNIC", "Gender", "DOB", "Address"]
        entries = []

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg="skyblue", fg="black", font=("Helvetica", 12)).grid(row=i, column=0, pady=10, padx=10, sticky='e')
    
            # Fields for Labels except Role, Gender, DOB
            if label not in ["Role", "Gender", "DOB"]:
                entry = tk.Entry(form_frame, font=("Helvetica", 12))
                entry.grid(row=i, column=1, pady=10, padx=10)
                entries.append(entry)
            
            # Role Dropdown
            if label == "Role":
                roles = fetch_roles()  # Fetch roles from the database
                role_names = [role[1] for role in roles]  # Assuming role is in the form (role_id, role_name)
                self.role_combobox = ttk.Combobox(form_frame, values=role_names, font=("Helvetica", 12), width=18, state="readonly")
                self.role_combobox.grid(row=i, column=1, pady=10, padx=10)
                entries.append(self.role_combobox)
            
            # Gender Dropdown
            if label == "Gender":
                gender_combobox = ttk.Combobox(form_frame, values=["Male", "Female", "Other"], font=("Helvetica", 12), width=18, state="readonly")
                gender_combobox.grid(row=i, column=1, pady=10, padx=10)
                entries.append(gender_combobox)

            # DOB DateEntry (Calendar)
            if label == "DOB":
                dob_entry = DateEntry(form_frame, font=("Helvetica", 12), width=18, year=2000, mindate=date(1900, 1, 1), maxdate=date.today() , date_pattern="dd-mm-yyyy")
                dob_entry.delete(0, "end")  # This clears the field, leaving it empty
                dob_entry.grid(row=i, column=1, pady=10, padx=10)
                entries.append(dob_entry)

        # Frame for Buttons at the Bottom
        button_frame = tk.Frame(add_user_window, bg="skyblue")
        button_frame.pack(pady=20)
        # Buttons - Center Aligned in button_frame
        tk.Button(button_frame, text="Cancel", bg="#dc3545", fg="white", font=("Helvetica", 12),
                command=add_user_window.destroy).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Add", bg="#007bff", fg="white", font=("Helvetica", 12),
                command=lambda: self.add_user(entries, add_user_window)).grid(row=0, column=1, padx=10)


    def add_user(self, entries, window):
        user_data = [entry.get() for entry in entries]
        print("User Data going be saved = ", user_data)
        if not validate_input(*user_data):
            messagebox.showerror("Error", "All fields are required")
            return
        add_user(*user_data)
        messagebox.showinfo("Success", "User added successfully")
        window.destroy()
        self.load_users()


    def update_user_screen(self):
        selected_item = self.user_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a user to update")
            return

        # Fetch old data for the selected user
        user_data = self.user_list.item(selected_item)['values']
        user_id = user_data[0]

        update_user_window = tk.Toplevel(self.root)
        update_user_window.geometry("400x550")
        update_user_window.minsize(400, 550)
        update_user_window.maxsize(400, 550)
        update_user_window.title("Update User")
        update_user_window.config(bg="skyblue")

        # Title - Centered
        title = tk.Label(update_user_window, text="Update User", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue",)
        title.pack(pady=20)

        # Frame for Form Fields
        form_frame = tk.Frame(update_user_window, bg="skyblue")
        form_frame.pack(pady=10)

        # Form Labels
        labels = ["Username", "Password", "Role", "Full Name", "CNIC", "Gender", "DOB", "Address"]
        entries = []

        # Role Options and Gender Options
        

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg="skyblue", fg="black", font=("Helvetica", 12)).grid(row=i, column=0, pady=10, padx=10, sticky='e')

            if label == "Role":
                # Role Dropdown
                roles = fetch_roles()  # Fetch roles from the database
                role_names = [role[1] for role in roles]  # Assuming role is in the form (role_id, role_name)
                role_combobox = ttk.Combobox(form_frame, font=("Helvetica", 12), width=18, values=role_names)
                role_combobox.set(user_data[3])  # Set Default to the existing role value
                role_combobox.grid(row=i, column=1, pady=10, padx=10)
                entries.append(role_combobox)

            elif label == "Gender":
                # Gender Dropdown
                genders = ["Male", "Female", "Other"] # Possible Gender Values
                gender_combobox = ttk.Combobox(form_frame, font=("Helvetica", 12), width=18, values=genders)
                gender_combobox.set(user_data[6])  # Set Default to the existing gender value
                gender_combobox.grid(row=i, column=1, pady=10, padx=10)
                entries.append(gender_combobox)

            elif label == "DOB":
                # Date of Birth Calendar (Using DateEntry)
                dob_entry = DateEntry(form_frame, font=("Helvetica", 12), width=18, year=int(user_data[7].split('-')[0]),
                                    date_pattern="dd-mm-yyyy", mindate=date(1900, 1, 1), maxdate=date.today())
                dob_entry.set_date(user_data[7])  # Set the date as the existing DOB
                dob_entry.grid(row=i, column=1, pady=10, padx=10)
                entries.append(dob_entry)

            else:
                # Normal Entry Fields
                entry = tk.Entry(form_frame, font=("Helvetica", 12))
                entry.insert(0, user_data[i + 1])  # Insert old data
                entry.grid(row=i, column=1, pady=10, padx=10)
                entries.append(entry)

        # Frame for Buttons at the Bottom
        button_frame = tk.Frame(update_user_window, bg="skyblue")
        button_frame.pack(pady=20)

        # Buttons - Center Aligned in button_frame
        tk.Button(button_frame, text="Cancel", bg="#dc3545", fg="white", font=("Helvetica", 12),
                command=update_user_window.destroy).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Update", bg="#ffc107", fg="black", font=("Helvetica", 12),
                command=lambda: self.update_user(entries, user_id, update_user_window)).grid(row=0, column=1, padx=10)


    def update_user(self, entries, user_id, window):
        # Get new data from the entry fields
        user_data = [entry.get() if isinstance(entry, tk.Entry) else entry.get() for entry in entries]
        # Validation
        if not validate_input(*user_data):
            messagebox.showerror("Error", "All fields are required")
            return
        # Call the backend update function
        update_user(user_id, *user_data)
        messagebox.showinfo("Success", "User updated successfully")
        # Close the update window and refresh the table list
        window.destroy()
        self.load_users()


    def delete_user_screen(self):
        selected_item = self.user_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a user to delete")
            return
        username = self.user_list.item(selected_item)['values'][1]
        self.delete_user(username)

    def delete_user(self, username):
        delete_user(username)
        messagebox.showinfo("Success", "User deleted successfully")
        self.load_users()

    def search_user_screen(self):
        search_term = self.search_entry.get().strip().lower()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter anyone of Id, Username, Full-Name, CNIC, DOB as search term")
            return
        matched_users = []
        users = fetch_users() # Call the backend method and receive the returned data 
        for user in users:
            user_id = str(user[0]).lower(),
            user_username = user[1].lower(), 
            user_full_name = user[4].lower(), 
            user_cnic = user[5].lower(), 
            user_dob = str(user[7]).lower()
            if search_term in user_id or search_term in user_username or search_term in user_full_name or search_term in user_cnic or search_term in user_dob:
                matched_users.append(user)
        self.display_matched_users(matched_users)

    def display_matched_users(self, matched_users):
        self.user_list.delete(*self.user_list.get_children())
        for user in matched_users:
            self.user_list.insert('', 'end', values=user)



if __name__ == "__main__":
    root = tk.Tk()
    # user =   # user-data wis already passing from login screen to admin dashboard
    app = ManageUsersScreen(root, user)
    #app = ManageUsersScreen(root, user=None)
    root.mainloop()







