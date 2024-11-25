



# Manage Spare-Parts Screen



import tkinter as tk
from tkinter import messagebox, ttk
from inventory import fetch_parts, add_part, update_part, delete_part
from utils import validate_input
import sqlite3
import mysql.connector

class ManageSparePartsScreen:
    def __init__(self, root, user):
        self.root = root
        self.root.title("MSPMS - Manage Spare-Parts")
        self.root.geometry("820x500")
        self.root.minsize(820, 500)
        self.root.maxsize(820, 500)
        self.root.config(bg="skyblue")
        self.user = user
        self.clear_frame()
        self.create_widgets()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_widgets(self):

        # Dashboard Title
        tk.Label(self.root, text="Manage Spare-Parts", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue").pack(pady=20)

        # Search Frame
        search_frame = tk.Frame(self.root, bg="skyblue")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search:", bg="skyblue", fg="black", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Helvetica", 14), bg="white", fg="black", insertbackground="black")
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_part_screen, bg="#007bff", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Clear Search", command=self.load_parts, bg="#6c757d", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
         
        # Treeview Table
        
        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white", font=("Helvetica", 12))
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background="blue", foreground="black")
        style.map('Treeview', background=[('selected', '#007bff')])

        table_frame = tk.Frame(self.root, bg="skyblue")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=40)

        self.part_list = ttk.Treeview(table_frame, columns=("ID", "Name", "Category", "Purchase_Price", "Sale_Price"), show='headings')
        self.part_list.heading("ID", text="ID")
        self.part_list.heading("Name", text="Name")
        self.part_list.heading("Category", text="Category")
        self.part_list.heading("Purchase_Price", text="Purchase Price")
        self.part_list.heading("Sale_Price", text="Sale Price")

        for col in self.part_list["columns"]:
            self.part_list.column(col, width=120, minwidth=100, stretch=tk.NO)

        self.part_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.part_list.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.part_list.xview)
        self.part_list.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)
        self.part_list.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
         
        # Buttons Frame
        button_frame = tk.Frame(self.root, bg="skyblue")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Back", command=self.back_to_dashboard_button, bg="#2ECC71", fg="black", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Add Part", command=self.add_part_screen, bg="#007bff", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Update Part", command=self.update_part_screen, bg="#ffc107", fg="black", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Delete Part", command=self.delete_part_screen, bg="#dc3545", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)

        self.load_parts()
    
    def back_to_dashboard_button(self):
        self.clear_frame()
        from admin_dashboard_screen import AdminDashboardScreen
        from salesman_dashboard_screen import SalesmanDashboardScreen
        if(self.user['role_id'] == 1):
            AdminDashboardScreen(self.root, self.user)
        else:
            SalesmanDashboardScreen(self.root, self.user)

    def load_parts(self):
        for i in self.part_list.get_children():
            self.part_list.delete(i)
        parts = fetch_parts()  # Call the Backend Method and receive the returned data 
        for part in parts:
            self.part_list.insert('', 'end', values=part)

    def add_part_screen(self):
        add_part_window = tk.Toplevel(self.root)
        add_part_window.geometry("400x380")
        add_part_window.minsize(400,380)
        add_part_window.maxsize(400,380)
        add_part_window.title("Add Spare-Part")
        add_part_window.config(bg="skyblue")
        # Title - Centered
        title = tk.Label(add_part_window, text="Add Spare-Part", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue")
        title.pack(pady=20)  
        # Frame for Form Fields
        form_frame = tk.Frame(add_part_window, bg="skyblue")
        form_frame.pack(pady=10) 
        # Form Fields Labels
        labels = ["Name", "Category", "Purchase Price", "Sale Price"]
        entries = []
        # Form Fields entries
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg="skyblue", fg="black", font=("Helvetica", 12)).grid(row=i, column=0, pady=10, padx=10, sticky='e')
            entry = tk.Entry(form_frame, font=("Helvetica", 12))
            entry.grid(row=i, column=1, pady=10, padx=10)
            entries.append(entry)
        # Frame for Buttons at the Bottom
        button_frame = tk.Frame(add_part_window, bg="skyblue")
        button_frame.pack(pady=20)
        # Buttons - Center Aligned in button_frame
        tk.Button(button_frame, text="Cancel", bg="#dc3545", fg="white", font=("Helvetica", 12),
                command=add_part_window.destroy).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Add", bg="#007bff", fg="white", font=("Helvetica", 12),
                command=lambda: self.add_part(entries, add_part_window)).grid(row=0, column=1, padx=10)

    def add_part(self, entries, window):
        part_data = [entry.get() for entry in entries]
        if not validate_input(*part_data):
            messagebox.showerror("Error", "All fields are required")
            return
        add_part(*part_data)
        messagebox.showinfo("Success", "part added successfully")
        window.destroy()
        self.load_parts()

    ## Update Part Screen
    def update_part_screen(self):
        selected_item = self.part_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a part to update")
            return
        # Fetch old data for the selected part
        part_data = self.part_list.item(selected_item)['values']
        part_id = self.part_list.item(selected_item)['values'][0]

        update_part_window = tk.Toplevel(self.root)
        update_part_window.geometry("400x370")
        update_part_window.minsize(400,370)
        update_part_window.maxsize(400,370)
        update_part_window.title("Update Spare-Part")
        update_part_window.config(bg="skyblue")

        # Title - Centered
        title = tk.Label(update_part_window, text="Update Spare-Part", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue")
        title.pack(pady=20)
        # Frame for Form Fields
        form_frame = tk.Frame(update_part_window, bg="skyblue")
        form_frame.pack(pady=10)
        # Form Fields Labels
        labels = ["Name", "Category", "Purchase Price", "Sale Price"]
        entries = []
        # Display old data in the entry fields
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg="skyblue", fg="black", font=("Helvetica", 12)).grid(row=i, column=0, pady=10, padx=10, sticky='e')
            entry = tk.Entry(form_frame, font=("Helvetica", 12))
            entry.insert(0, part_data[i+1])  # Insert old data (Name=index1,Category=index2,Purchase_Price=index3,Sale_Price=index4
            entry.grid(row=i, column=1, pady=10, padx=10)
            entries.append(entry)
        # Frame for Buttons at the Bottom
        button_frame = tk.Frame(update_part_window, bg="skyblue")
        button_frame.pack(pady=20)  # Packs button frame below the form
        # Buttons - Center Aligned in button_frame
        tk.Button(button_frame, text="Cancel", bg="#dc3545", fg="white", font=("Helvetica", 12),
                command=update_part_window.destroy).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Update", bg="#ffc107", fg="black", font=("Helvetica", 12),
                command=lambda: self.update_part(entries, part_id, update_part_window)).grid(row=0, column=1, padx=10)

    def update_part(self, entries, part_id, window):
        # Get new data from the entry fields
        part_data = [entry.get() for entry in entries]
        print(f"Received new updated data of selected Item ID={part_id} is = {part_data}")
        # Validation
        if not validate_input(*part_data):
            messagebox.showerror("Error", "All fields are required")
            return
        # Call the backend update function
        update_part(part_id, *part_data)
        messagebox.showinfo("Success", "part updated successfully")
        # Close the update window and refresh the part list
        window.destroy()
        self.load_parts()


    ## Delete Part Screen
    def delete_part_screen(self):
        selected_item = self.part_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a part to delete")
            return
        part_id = self.part_list.item(selected_item)['values'][0]
        self.delete_part(part_id)

    def delete_part(self, part_id):
        delete_part(part_id)
        messagebox.showinfo("Success", "Spare-Part deleted successfully")
        self.load_parts()


    ## Function Search Items based on some features
    def search_part_screen(self):
        search_term = self.search_entry.get().strip().lower()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter anyone of Id, Name, Category, Stock as a search term")
            return
        matched_parts = []
        parts = fetch_parts() # Call the backend method and receive the returned data 
        for part in parts:
            part_id = str(part[0]).lower()
            part_name = part[1].lower()
            part_category = part[2].lower()
            if search_term in part_id or search_term in part_name or search_term in part_category:
                matched_parts.append(part)
        self.display_matched_parts(matched_parts)

    def display_matched_parts(self, matched_parts):
        self.part_list.delete(*self.part_list.get_children())
        for part in matched_parts:
            self.part_list.insert('', 'end', values=part)


if __name__ == "__main__":
    root = tk.Tk()
    # user =   # user-data wis already passing from login screen to admin dashboard
    app = ManageSparePartsScreen(root, user)
    #app = ManageSparePartsScreen(root, user=None)
    root.mainloop()


