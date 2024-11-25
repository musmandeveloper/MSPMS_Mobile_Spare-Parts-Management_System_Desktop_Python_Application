




# Assign Authorization Frontend Screen



import tkinter as tk
from tkinter import messagebox, ttk
from authorization import fetch_authorizations, add_authorization, fetch_assigned_permissions, update_authorization, delete_authorization
from roles import fetch_roles
from permissions import fetch_permissions
from utils import validate_input


class AssignAuthorizationScreen:
    def __init__(self, root, user):
        self.root = root
        self.root.title("MSPMS - Assign Authorization Screen")
        self.root.geometry("700x530")
        self.root.minsize(700,530)
        self.root.maxsize(700,530)
        self.root.config(bg="skyblue")
        self.user = user
        self.clear_frame()
        self.create_widgets()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_widgets(self):

        # Dashboard Title
        title = tk.Label(self.root, text="Assign Authorization", font=("Helvetica", 24, "bold"),  fg="black", bg="skyblue")
        title.pack(pady=20)

        search_frame = tk.Frame(self.root, bg="skyblue")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search:", bg="skyblue", fg="black", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Helvetica", 14), bg="white", fg="black", insertbackground="black")
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_authorization_screen, bg="#007bff", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Clear Search", command=self.load_authorizations, bg="#6c757d", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)

        # TreeView Table

        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white", font=("Helvetica", 12))
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background="blue", foreground="black")
        style.map('Treeview', background=[('selected', '#007bff')])

        table_frame = tk.Frame(self.root, bg="skyblue")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=30)

        self.authorization_list = ttk.Treeview(table_frame, columns=("Id", "Role_Name", "Permission_Name"), show='headings')
        self.authorization_list.heading("Id", text="Id")
        self.authorization_list.heading("Role_Name", text="Role Name")
        self.authorization_list.heading("Permission_Name", text="Permission Name")

        for col in self.authorization_list["columns"]:
            self.authorization_list.column(col, width=120, minwidth=100, stretch=tk.NO)

        self.authorization_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.authorization_list.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.authorization_list.xview)
        self.authorization_list.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)

        self.authorization_list.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Button Frame
        button_frame = tk.Frame(self.root, bg="skyblue")
        button_frame.pack(pady=(20,30))

        tk.Button(button_frame, text="Back", command=self.back_to_dashboard_button, bg="#2ECC71", fg="black", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Add Authorization", command=self.add_authorization_screen, bg="#007bff", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Update Authorization", command=self.update_authorization_screen, bg="#ffc107", fg="black", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Delete Authorization", command=self.delete_authorization_screen, bg="#dc3545", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)

        self.load_authorizations()


    def back_to_dashboard_button(self):
        self.clear_frame()
        from manage_authorization_screen import ManageAuthorizationScreen
        ManageAuthorizationScreen(self.root, self.user)

    def load_authorizations(self):
        for i in self.authorization_list.get_children():
            self.authorization_list.delete(i)
        authorizations = fetch_authorizations()  # Call the backend method and receive the returned data 
        print("Received Fetched Authorizations:", authorizations)
        for authorization in authorizations:
            self.authorization_list.insert('', 'end', values=authorization)

    def back_button(self):
        self.clear_frame()
        self.create_widgets()

    def add_authorization_screen(self):
        # Create a Toplevel window for the pop-up
        add_auth_window = tk.Toplevel(self.root)
        add_auth_window.geometry("430x370")
        add_auth_window.minsize(430, 370)
        add_auth_window.maxsize(430, 370)
        add_auth_window.title("Add Authorization")
        add_auth_window.config(bg="skyblue")

        # Title - Centered
        title = tk.Label(add_auth_window, text="Add Authorization", font=("Helvetica", 20, "bold"), fg="black", bg="skyblue")
        title.pack(pady=20)

        # Fetch roles and permissions from the backend
        roles = fetch_roles()  # call the backend method and receive the returned data
        permissions = fetch_permissions()  # call the backend method and receive the returned data
        # Debugging: Print fetched roles and permissions
        print("Fetched Roles:", roles)
        print("Fetched Permissions:", permissions)

        # Form Frame for Role and Permissions fields
        form_frame = tk.Frame(add_auth_window, bg="skyblue")
        form_frame.pack(pady=10, padx=10, fill="both")

        # Role Combobox
        tk.Label(form_frame, text="Role:", bg="skyblue", fg="black", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky='e', pady=10, padx=(10, 8))
        role_names = [role[1] for role in roles]
        self.role_combobox = ttk.Combobox(form_frame, values=role_names, font=("Helvetica", 12), width=26)
        self.role_combobox.grid(row=0, column=1, pady=10, padx=(8, 10))

        # Permissions Label
        tk.Label(form_frame, text="Permissions:", bg="skyblue", fg="black", font=("Helvetica", 12, "bold")).grid(row=1, column=0, sticky='ne', pady=10, padx=10)

        # Scrollable Frame for Permissions Checkboxes
        scroll_container = tk.Frame(form_frame, bg="skyblue", bd=2, relief="flat")
        scroll_container.grid(row=1, column=1, columnspan=2, pady=10, padx=(8, 10), sticky='nsew')
        # Canvas
        canvas = tk.Canvas(scroll_container, bg="white", width=240, height=100)
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)        
        h_scrollbar = ttk.Scrollbar(scroll_container, orient="horizontal", command=canvas.xview)
        # Scrollable frame inside canvas
        scrollable_frame = tk.Frame(canvas, bg="white")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        # Canvas configuration for horizontal and vertical scrolling
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        # Grid the canvas and scrollbars inside the scroll_container
        canvas.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        # Scroll container configuration
        scroll_container.grid_rowconfigure(0, weight=1)
        scroll_container.grid_columnconfigure(0, weight=1)

        # Add permission checkboxes in one column (one checkbox per row)
        self.permission_vars = {}
        for i, permission in enumerate(permissions):
            var = tk.IntVar()
            chk = tk.Checkbutton(scrollable_frame, text=permission[1], variable=var, bg="white", fg="blue", font=("Helvetica", 12), selectcolor="white")
            chk.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            self.permission_vars[permission[1]] = var

        # Buttons Frame at the bottom
        button_frame = tk.Frame(add_auth_window, bg="skyblue")
        button_frame.pack(pady=20)
        # Buttons - Center Aligned
        tk.Button(button_frame, text="Cancel", bg="#dc3545", fg="white", font=("Helvetica", 12),
                command=add_auth_window.destroy, width=15).grid(row=0, column=0, padx=(10, 15))
        tk.Button(button_frame, text="Add", bg="#007bff", fg="white", font=("Helvetica", 12),
                command=lambda: self.add_authorization(), width=15).grid(row=0, column=1, padx=(15, 10))


    def add_authorization(self):
        selected_role_name = self.role_combobox.get()
        # Debugging: Print selected role name
        print("Selected Role-Name:", selected_role_name)
        selected_permissions_name = [perm_name for perm_name, var in self.permission_vars.items() if var.get() == 1]
        print(f"Selected Permissions-Name for selected role:{selected_role_name} are = ", selected_permissions_name)
        if not selected_permissions_name:
            messagebox.showerror("Error", "At least one permission must be selected")
            return
        add_authorization(selected_role_name, selected_permissions_name)
        self.back_button()


    def update_authorization_screen(self):
        selected_item = self.authorization_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select an authorization to update")
            return
        auth_id = self.authorization_list.item(selected_item)['values'][0]
        old_role_name = self.authorization_list.item(selected_item)['values'][1]

        # Create a Toplevel window for the pop-up
        update_auth_window = tk.Toplevel(self.root)
        update_auth_window.geometry("430x370")
        update_auth_window.minsize(430, 370)
        update_auth_window.maxsize(430, 370)
        update_auth_window.title("Update Authorization")
        update_auth_window.config(bg="skyblue")

        # Title - Centered
        title = tk.Label(update_auth_window, text="Update Authorization", font=("Helvetica", 20, "bold"), fg="black", bg="skyblue")
        title.pack(pady=20)

        # Fetch roles and permissions from the backend
        roles = fetch_roles()  # Replace with your actual backend method
        permissions = fetch_permissions()  # Replace with your actual backend method
        # Fetch old assigned permissions to selected role_name
        assigned_permissions = fetch_assigned_permissions(old_role_name)  

        # Form Frame for Role and Permissions fields
        form_frame = tk.Frame(update_auth_window, bg="skyblue")
        form_frame.pack(pady=10, padx=10, fill="both")

        # Role Label and Combobox using grid
        tk.Label(form_frame, text="Role:", bg="skyblue", fg="black", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky='e', pady=10, padx=(10, 8))
        self.role_label = tk.Label(form_frame, text=old_role_name, font=("Helvetica", 12), width=26, anchor="w", relief="sunken")
        self.role_label.grid(row=0, column=1, pady=10, padx=(8, 10))

        # Permissions Label using grid
        tk.Label(form_frame, text="Permissions:", bg="skyblue", fg="black", font=("Helvetica", 12, "bold")).grid(row=1, column=0, sticky='ne', pady=10, padx=10)
        # Scrollable Frame for Permissions Checkboxes using grid
        scroll_container = tk.Frame(form_frame, bg="skyblue", bd=2, relief="flat")
        scroll_container.grid(row=1, column=1, columnspan=2, pady=10, padx=(8, 10), sticky='nsew')
        # Canvas
        canvas = tk.Canvas(scroll_container, bg="white", width=240, height=100)
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(scroll_container, orient="horizontal", command=canvas.xview)
        # Scrollable frame inside canvas
        scrollable_frame = tk.Frame(canvas, bg="white")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        # Canvas configuration for horizontal and vertical scrolling
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        # Grid the canvas and scrollbars inside the scroll_container
        canvas.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        # Scroll container configuration
        scroll_container.grid_rowconfigure(0, weight=1)
        scroll_container.grid_columnconfigure(0, weight=1)
        # Add permission checkboxes in one column (one checkbox per row)
        self.permission_vars = {}
        for i, permission in enumerate(permissions):
            var = tk.IntVar()
            chk = tk.Checkbutton(scrollable_frame, text=permission[1], variable=var, bg="white", fg="blue", font=("Helvetica", 12), selectcolor="white")
            chk.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            if permission[0] in assigned_permissions:
                var.set(1)
            self.permission_vars[permission[1]] = var

        # Buttons Frame at the bottom using pack
        button_frame = tk.Frame(update_auth_window, bg="skyblue")
        button_frame.pack(pady=20)
        # Buttons - Center Aligned using grid
        tk.Button(button_frame, text="Cancel", bg="#dc3545", fg="white", font=("Helvetica", 12),
                command=update_auth_window.destroy, width=15).grid(row=0, column=0, padx=(10, 15))
        tk.Button(button_frame, text="Update", bg="#ffc107", fg="white", font=("Helvetica", 12),
                command=lambda: self.update_authorization(auth_id, old_role_name), width=15).grid(row=0, column=1, padx=(15, 10))


    def update_authorization(self, auth_id, selected_role_name):
        new_selected_permissions = [perm_name for perm_name, var in self.permission_vars.items() if var.get() == 1]
        print("Newly Assigning Permissions for selected role: {selected_role_name} are = ", new_selected_permissions)
        if not new_selected_permissions:
            messagebox.showerror("Error", "At least one permission must be selected")
            return
        update_authorization(auth_id, selected_role_name, new_selected_permissions)  # Calling Backend Method
        self.back_button()
    

    def delete_authorization_screen(self):
        selected_item = self.authorization_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a authorization to delete")
            return
        role_name = self.authorization_list.item(selected_item)['values'][1]        
        self.delete_authorization(role_name)

    def delete_authorization(self, role_name):
        delete_authorization(role_name)
        self.load_authorizations()


    def search_authorization_screen(self):
        search_term = self.search_entry.get().strip().lower()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter anyone of Id, Role ID as search term")
            return
        matched_authorizations = []
        authorizations = fetch_authorizations() # Call the backend method and receive the returned data 
        for authorization in authorizations:
            authorization_id = str(authorization[0]).lower(),
            authorization_role_id = str(authorization[1]).lower(), 
            if search_term in authorization_id or search_term in authorization_role_id:
                matched_authorizations.append(authorization)
        self.display_matched_authorizations(matched_authorizations)

    def display_matched_authorizations(self, matched_authorizations):
        self.authorization_list.delete(*self.authorization_list.get_children())
        for authorization in matched_authorizations:
            self.authorization_list.insert('', 'end', values=authorization)




if __name__ == "__main__":
    root = tk.Tk()
    # user =   # user-data wis already passing from login screen to admin dashboard
    app = AssignAuthorizationScreen(root, user)
    root.mainloop()





