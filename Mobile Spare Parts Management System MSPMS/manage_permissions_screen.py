




# Manage Permissions Frontend Screen




import tkinter as tk
from tkinter import messagebox, ttk
from permissions import fetch_permissions, add_permission, update_permission, delete_permission
from utils import validate_input


class ManagePermissionsScreen:
    def __init__(self, root, user):
        self.root = root
        self.root.title("MSPMS - Manage Permissions")
        self.root.geometry("700x500")
        self.root.minsize(700, 500)
        self.root.maxsize(700, 500)
        self.root.config(bg="skyblue")
        self.user = user
        self.clear_frame()
        self.create_widgets()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_widgets(self):

        # Dashboard Title
        title = tk.Label(self.root, text="Manage Permissions", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue")
        title.pack(pady=20)

        search_frame = tk.Frame(self.root, bg="skyblue")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search:", bg="skyblue", fg="black", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Helvetica", 14), bg="white", fg="black", insertbackground="black")
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_permission_screen, bg="#007bff", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Clear Search", command=self.load_permissions, bg="#6c757d", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)

        # TreeView Table

        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white", font=("Helvetica", 12))
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background="blue", foreground="black")
        style.map('Treeview', background=[('selected', '#007bff')])

        table_frame = tk.Frame(self.root, bg="skyblue")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=40)

        self.permission_list = ttk.Treeview(table_frame, columns=("ID", "Name", "Description"), show='headings')
        self.permission_list.heading("ID", text="ID")
        self.permission_list.heading("Name", text="Name")
        self.permission_list.heading("Description", text="Description")


        for col in self.permission_list["columns"]:
            self.permission_list.column(col, width=120, minwidth=100, stretch=tk.NO)

        self.permission_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.permission_list.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.permission_list.xview)
        self.permission_list.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)

        self.permission_list.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        button_frame = tk.Frame(self.root, bg="skyblue")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Back", command=self.back_to_dashboard_button, bg="#2ECC71", fg="black", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Add Permission", command=self.add_permission_screen, bg="#007bff", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Update Permission", command=self.update_permission_screen, bg="#ffc107", fg="black", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Delete Permission", command=self.delete_permission_screen, bg="#dc3545", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)

        self.load_permissions()


    def load_permissions(self):
        for i in self.permission_list.get_children():
            self.permission_list.delete(i)
        permissions = fetch_permissions()  # Call the backend method
        for permission in permissions:
            self.permission_list.insert('', 'end', values=permission)

    def back_to_dashboard_button(self):
        self.clear_frame()
        from manage_authorization_screen import ManageAuthorizationScreen
        ManageAuthorizationScreen(self.root, self.user)


    def add_permission_screen(self):
        add_permission_window = tk.Toplevel(self.root)
        add_permission_window.geometry("390x300")
        add_permission_window.maxsize(390, 300)
        add_permission_window.minsize(390, 300)
        add_permission_window.title("Add Permission")
        add_permission_window.config(bg="skyblue")

        # Title - Centered
        title = tk.Label(add_permission_window, text="Add Permission", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue")
        title.pack(pady=20)  

        # Frame for Form Fields
        form_frame = tk.Frame(add_permission_window, bg="skyblue")
        form_frame.pack(pady=10) 

        # Form Fields inside form_frame
        labels = ["Name", "Description"]
        entries = []

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg="skyblue", fg="black", font=("Helvetica", 12)).grid(row=i, column=0, pady=10, padx=10, sticky='e')
            entry = tk.Entry(form_frame, font=("Helvetica", 12))
            entry.grid(row=i, column=1, pady=10, padx=10)
            entries.append(entry)
        # Frame for Buttons at the Bottom
        button_frame = tk.Frame(add_permission_window, bg="skyblue")
        button_frame.pack(pady=20)
        # Buttons - Center Aligned in button_frame
        tk.Button(button_frame, text="Cancel", bg="#dc3545", fg="white", font=("Helvetica", 12),
                command=add_permission_window.destroy).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Add", bg="#007bff", fg="white", font=("Helvetica", 12),
                command=lambda: self.add_permission(entries, add_permission_window)).grid(row=0, column=1, padx=10)

    def add_permission(self, entries, window):
        permission_data = [entry.get() for entry in entries]
        print("Permission Data to be inserted ", permission_data)
        if not validate_input(*permission_data):
            messagebox.showerror("Error", "All fields are required")
            return
        add_permission(*permission_data)
        messagebox.showinfo("Success", "Permission added successfully")
        window.destroy()
        self.load_permissions()

    def update_permission_screen(self):
        selected_item = self.permission_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a permission to update")
            return

        # Fetch old data for the selected permission
        permission_data = self.permission_list.item(selected_item)['values']
        permission_id = self.permission_list.item(selected_item)['values'][0]

        update_permission_window = tk.Toplevel(self.root)
        update_permission_window.geometry("390x300")
        update_permission_window.minsize(390, 300)
        update_permission_window.maxsize(390, 300)
        update_permission_window.title("Update Permission")
        update_permission_window.config(bg="skyblue")

        # Title - Centered
        title = tk.Label(update_permission_window, text="Update Permission", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue")
        title.pack(pady=20)

        # Frame for Form Fields
        form_frame = tk.Frame(update_permission_window, bg="skyblue")
        form_frame.pack(pady=10)

        # Form Fields inside form_frame
        labels = ["Name", "Description"]
        entries = []

        # Display old data in the entry fields
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg="skyblue", fg="black", font=("Helvetica", 12)).grid(row=i, column=0, pady=10, padx=10, sticky='e')
            
            entry = tk.Entry(form_frame, font=("Helvetica", 12))
            entry.insert(0, permission_data[i+1])  # Insert old data (Name at index 1, Description at index 2)
            entry.grid(row=i, column=1, pady=10, padx=10)
            entries.append(entry)

        # Frame for Buttons at the Bottom
        button_frame = tk.Frame(update_permission_window, bg="skyblue")
        button_frame.pack(pady=20)

        # Buttons - Center Aligned in button_frame
        tk.Button(button_frame, text="Cancel", bg="#dc3545", fg="white", font=("Helvetica", 12),
                command=update_permission_window.destroy).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Update", bg="#ffc107", fg="black", font=("Helvetica", 12),
                command=lambda: self.update_permission(entries, permission_id, update_permission_window)).grid(row=0, column=1, padx=10)


    def update_permission(self, entries, permission_id, window):
        # Get new data from the entry fields
        permission_data = [entry.get() for entry in entries]
        # Validation
        if not validate_input(*permission_data):
            messagebox.showerror("Error", "All fields are required")
            return
        # Call the backend update function
        update_permission(permission_id, *permission_data)
        messagebox.showinfo("Success", "Permission updated successfully")
        # Close the update window and refresh the table list
        window.destroy()
        self.load_permissions()

    def delete_permission_screen(self):
        selected_item = self.permission_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a permission to delete")
            return
        name = self.permission_list.item(selected_item)['values'][1]
        self.delete_permission(name)

    def delete_permission(self,name):
        delete_permission(name)
        messagebox.showinfo("Success", "Permission deleted successfully")
        self.load_permissions()

    def search_permission_screen(self):
        search_term = self.search_entry.get().strip().lower()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter anyone of Id or Name as search term")
            return
        matched_permissions = []
        permissions = fetch_permissions() # Call the backend method and receive the returned data 
        for permission in permissions:
            permission_id = str(permission[0]).lower()
            permission_name = permission[1].lower()
            if search_term in permission_id or search_term in permission_name:
                matched_permissions.append(permission)
        self.display_matched_permissions(matched_permissions)

    def display_matched_permissions(self, matched_permissions):
        self.permission_list.delete(*self.permission_list.get_children())
        for permission in matched_permissions:
            self.permission_list.insert('', 'end', values=permission)




if __name__ == "__main__":
    root = tk.Tk()
    # user =   # user-data wis already passing from login screen to admin dashboard
    app = ManagePermissionsScreen(root, user)
    root.mainloop()








