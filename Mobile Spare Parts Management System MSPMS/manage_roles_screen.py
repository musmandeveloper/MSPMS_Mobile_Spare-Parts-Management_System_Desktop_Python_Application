




import tkinter as tk
from tkinter import messagebox, ttk
from roles import fetch_roles, add_role, update_role, delete_role
from utils import validate_input


class ManageRolesScreen:
    def __init__(self, root, user):
        self.root = root
        self.root.title("MSPMS - Manage Roles")
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
        title = tk.Label(self.root, text="Manage Roles", font=("Helvetica", 24, "bold"),  fg="black", bg="skyblue")
        title.pack(pady=20)

        # Search Frame
        search_frame = tk.Frame(self.root, bg="skyblue")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search:", bg="skyblue", fg="black", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Helvetica", 14), bg="white", fg="black", insertbackground="black")
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_role_screen, bg="#007bff", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Clear Search", command=self.load_roles, bg="#6c757d", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)

        # TreeView Table
        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white", font=("Helvetica", 12))
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background="blue", foreground="black")
        style.map('Treeview', background=[('selected', '#007bff')])

        table_frame = tk.Frame(self.root, bg="skyblue")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=40)

        self.role_list = ttk.Treeview(table_frame, columns=("ID", "Name", "Description"), show='headings')
        self.role_list.heading("ID", text="ID")
        self.role_list.heading("Name", text="Name")
        self.role_list.heading("Description", text="Description")

        for col in self.role_list["columns"]:
            self.role_list.column(col, width=120, minwidth=100, stretch=tk.NO)

        self.role_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.role_list.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.role_list.xview)
        self.role_list.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)

        self.role_list.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Button Frame
        button_frame = tk.Frame(self.root, bg="skyblue")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Back", command=self.back_to_dashboard_button, bg="#2ECC71", fg="black", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Add Role", command=self.add_role_screen, bg="#007bff", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Update Role", command=self.update_role_screen, bg="#ffc107", fg="black", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Delete Role", command=self.delete_role_screen, bg="#dc3545", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)

        self.load_roles()

    def load_roles(self):
        for i in self.role_list.get_children():
            self.role_list.delete(i)
        roles = fetch_roles()  # Fetch roles from backend
        for role in roles:
            self.role_list.insert('', 'end', values=role)

    def back_to_dashboard_button(self):
        self.clear_frame()
        from manage_authorization_screen import ManageAuthorizationScreen
        ManageAuthorizationScreen(self.root, self.user)
        

    def add_role_screen(self):
        add_role_window = tk.Toplevel(self.root)
        add_role_window.geometry("390x300")
        add_role_window.minsize(390, 300)
        add_role_window.maxsize(390, 300) 
        add_role_window.title("Add Role")
        add_role_window.config(bg="skyblue")

        # Title - Centered
        title = tk.Label(add_role_window, text="Add Role", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue",)
        title.pack(pady=20)  
        # Frame for Form Fields
        form_frame = tk.Frame(add_role_window, bg="skyblue")
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
        button_frame = tk.Frame(add_role_window, bg="skyblue")
        button_frame.pack(pady=20)
        # Buttons - Center Aligned in button_frame
        tk.Button(button_frame, text="Cancel", bg="#dc3545", fg="white", font=("Helvetica", 12),
                command=add_role_window.destroy).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Add", bg="#007bff", fg="white", font=("Helvetica", 12),
                command=lambda: self.add_role(entries, add_role_window)).grid(row=0, column=1, padx=10)


    def add_role(self, entries, window):
        role_data = [entry.get() for entry in entries]
        print("Role Data to be inserted ", role_data)
        if not validate_input(*role_data):
            messagebox.showerror("Error", "All fields are required")
            return
        add_role(*role_data)
        messagebox.showinfo("Success", "Role added successfully")
        window.destroy()
        self.load_roles()

    def update_role_screen(self):
        selected_item = self.role_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a role to update")
            return
        # Fetch old data for the selected role
        role_data = self.role_list.item(selected_item)['values']
        role_id = self.role_list.item(selected_item)['values'][0]

        update_role_window = tk.Toplevel(self.root)
        update_role_window.geometry("390x300")
        update_role_window.minsize(390, 300)
        update_role_window.maxsize(390, 300) 
        update_role_window.title("Update Role")
        update_role_window.config(bg="skyblue")

        # Title - Centered
        title = tk.Label(update_role_window, text="Update Role", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue")
        title.pack(pady=20)

        # Frame for Form Fields
        form_frame = tk.Frame(update_role_window, bg="skyblue")
        form_frame.pack(pady=10)

        # Form Fields inside form_frame
        labels = ["Name", "Description"]
        entries = []

        # Display old data in the entry fields
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg="skyblue", fg="black", font=("Helvetica", 12)).grid(row=i, column=0, pady=10, padx=10, sticky='e')
            
            entry = tk.Entry(form_frame, font=("Helvetica", 12))
            entry.insert(0, role_data[i+1])  # Insert old data (Name at index 1, Description at index 2)
            entry.grid(row=i, column=1, pady=10, padx=10)
            entries.append(entry)

        # Frame for Buttons at the Bottom
        button_frame = tk.Frame(update_role_window, bg="skyblue")
        button_frame.pack(pady=20)  # Packs button frame below the form

        # Buttons - Center Aligned in button_frame
        tk.Button(button_frame, text="Cancel", bg="#dc3545", fg="white", font=("Helvetica", 12),
                command=update_role_window.destroy).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Update", bg="#ffc107", fg="black", font=("Helvetica", 12),
                command=lambda: self.update_role(entries, role_id, update_role_window)).grid(row=0, column=1, padx=10)


    def update_role(self, entries, role_id, window):
        # Get new data from the entry fields
        role_data = [entry.get() for entry in entries]
        # Validation
        if not validate_input(*role_data):
            messagebox.showerror("Error", "All fields are required")
            return
        # Call the backend update function
        update_role(role_id, *role_data)
        messagebox.showinfo("Success", "Role updated successfully")
        # Close the update window and refresh the role list
        window.destroy()
        self.load_roles()

    def delete_role_screen(self):
        selected_item = self.role_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a role to delete")
            return
        role_name= self.role_list.item(selected_item)['values'][1]
        self.delete_role(role_name)

    def delete_role(self, role_name):
        delete_role(role_name)
        messagebox.showinfo("Success", "Role deleted successfully")
        self.load_roles()

    def search_role_screen(self):
        search_term = self.search_entry.get().strip().lower()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
        matched_roles = []
        roles = fetch_roles()  # Fetch roles from backend
        for role in roles:
            role_id = str(role[0]).lower()
            role_name = role[1].lower()
            if search_term in role_id or search_term in role_name:
                matched_roles.append(role)
        self.display_matched_roles(matched_roles)

    def display_matched_roles(self, matched_roles):
        self.role_list.delete(*self.role_list.get_children())
        for role in matched_roles:
            self.role_list.insert('', 'end', values=role)




if __name__ == "__main__":
    root = tk.Tk()
    # user =   # user-data wis already passing from login screen to admin dashboard
    app = ManageRolesScreen(root, user)
    #app = ManageRolesScreen(root, user=None)
    root.mainloop()




