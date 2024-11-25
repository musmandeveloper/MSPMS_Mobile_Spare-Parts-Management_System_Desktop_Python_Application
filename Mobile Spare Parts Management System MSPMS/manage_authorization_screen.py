



# Manage Authorization Frontend Screen



import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from manage_roles_screen import ManageRolesScreen
from manage_permissions_screen import ManagePermissionsScreen
from assign_authorization_screen import AssignAuthorizationScreen
from utils import validate_input


class ManageAuthorizationScreen:
    def __init__(self, root, user):
        self.root = root
        self.root.title("MSPMS - Manage Authorization Screen")
        self.root.geometry("920x510")
        self.root.minsize(920,510)
        self.root.maxsize(920,510)
        self.root.config(bg="skyblue")
        self.user = user
        self.clear_frame()
        self.create_widgets()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_widgets(self):


        # Application Logo and Name
        app_logo_frame = tk.Frame(self.root, bg="skyblue")
        app_logo_frame.grid(row=0, column=5, columnspan=4, pady=(30,40), padx=30, sticky="nsew")

        # Load application logo (replace 'app_logo.png' with your actual image path)
        self.app_logo_image = Image.open("assets/app_logo_1.png")
        self.app_logo_image = self.app_logo_image.resize((60, 60), Image.LANCZOS)
        self.app_logo_photo = ImageTk.PhotoImage(self.app_logo_image)
        app_logo_label = tk.Label(app_logo_frame, image=self.app_logo_photo, bg="skyblue")
        app_logo_label.pack(side="left", padx=10)

        app_name_label = tk.Label(app_logo_frame, text="Mobile Spare Parts Management System - MSPMS", font=("Helvetica", 24, "bold"), fg="#5A55E6", bg="skyblue")
        app_name_label.pack(side="left", padx=10)

        # User Profile Icon, Welcome Message, and Logout Button
        profile_frame = tk.Frame(self.root, bg="skyblue")
        profile_frame.grid(row=1, column=5, columnspan=4, pady=10, padx=30, sticky="ew")

        # Load user profile icon (replace 'user_icon.png' with your actual image path)
        self.profile_image = Image.open("assets/user_icon.png")
        self.profile_image = self.profile_image.resize((50, 50), Image.LANCZOS)
        self.profile_photo = ImageTk.PhotoImage(self.profile_image)
        profile_label = tk.Label(profile_frame, image=self.profile_photo, bg="skyblue")
        profile_label.grid(row=1, column=5, padx=(10,280), sticky="w")

        welcome_label = tk.Label(profile_frame, text=f"Welcome {self.user['full_name']}", font=("Helvetica", 12), fg="black", bg="skyblue")
        welcome_label.grid(row=1, column=6, sticky="nsew")

        logout_button = tk.Button(profile_frame, text="Logout", font=("Helvetica", 14), fg="white", bg="#dc3545", command=self.logout, width=10, height=1)
        logout_button.grid(row=1, column=7, padx=(180,10), sticky="e")

        profile_frame.grid_columnconfigure(0, weight=1)
        profile_frame.grid_columnconfigure(1, weight=1)
        profile_frame.grid_columnconfigure(2, weight=1)

        # Dashboard Label
        tk.Label(self.root, text="Manage Authorization", font=("Helvetica", 20, "bold"), fg="black", bg="skyblue").grid(row=2, column=5, columnspan=4, padx=30, pady=20, sticky="nsew")

        # Buttons Frame
        buttons_frame = tk.Frame(self.root, bg="skyblue")
        buttons_frame.grid(row=3, column=5, columnspan=3, pady=(30,20), padx=(50,40), sticky="nsew")

        # Buttons Images
        # 1
        icon_back_arrow_image = Image.open("assets/back_arrow.png")
        icon_back_arrow_image = icon_back_arrow_image.resize((35,35), Image.LANCZOS) 
        icon_back_arrow_photo = ImageTk.PhotoImage(icon_back_arrow_image)        
        # 2
        icon_manage_role_image = Image.open("assets/manage_role.png")
        icon_manage_role_image = icon_manage_role_image.resize((35,35), Image.LANCZOS) 
        icon_manage_role_photo = ImageTk.PhotoImage(icon_manage_role_image)
        # 3
        icon_manage_permission_image = Image.open("assets/manage_permission.png")
        icon_manage_permission_image = icon_manage_permission_image.resize((35,35), Image.LANCZOS)  
        icon_manage_permission_photo = ImageTk.PhotoImage(icon_manage_permission_image)
        # 4
        icon_assign_authorization_image = Image.open("assets/assign_authorization.png")
        icon_assign_authorization_image = icon_assign_authorization_image.resize((35,35), Image.LANCZOS) 
        icon_assign_authorization_photo = ImageTk.PhotoImage(icon_assign_authorization_image)

        # Keep a reference to the image
        self.icon_back_arrow_photo = icon_back_arrow_photo        
        self.icon_manage_role_photo = icon_manage_role_photo
        self.icon_manage_permission_photo  = icon_manage_permission_photo
        self.icon_assign_authorization_photo = icon_assign_authorization_photo

        # Buttons
        tk.Button(buttons_frame, image=icon_back_arrow_photo, text="Back", width=210, height=40, compound="left", anchor="w", padx=5, font=("Helvetica", 14), fg="#2C3E50", bg="#ECF0F1", command=self.back_to_dashboard_button, ).grid(row=0, column=0, pady=(20,10), padx=(20,10))
        tk.Button(buttons_frame, image=icon_manage_role_photo, text="Manage Role", width=210, height=40, compound="left", anchor="w", padx=5, font=("Helvetica", 14), fg="#2C3E50", bg="#ECF0F1", command=self.manage_roles_screen, ).grid(row=0, column=1, pady=(20,10), padx=(10,10))
        tk.Button(buttons_frame, image=icon_manage_permission_photo, text="Manage Permission", width=210, height=40, compound="left", anchor="w", padx=5, font=("Helvetica", 14), fg="#2C3E50", bg="#ECF0F1", command=self.manage_permissions_screen, ).grid(row=0, column=2, pady=(20,10), padx=(10,20))
        tk.Button(buttons_frame, image=icon_assign_authorization_photo, text="Assign Authorization", width=210, height=40, compound="left", anchor="w", padx=5, font=("Helvetica", 14), fg="#2C3E50", bg="#ECF0F1", command=self.assign_authorization_screen, ).grid(row=1, column=1, pady=(20,10), padx=(10,10))
 

    def back_to_dashboard_button(self):
        self.clear_frame()
        from admin_dashboard_screen import AdminDashboardScreen
        AdminDashboardScreen(self.root, self.user)

    def manage_roles_screen(self):
        self.clear_frame()
        ManageRolesScreen(self.root, self.user)

    def manage_permissions_screen(self):
        self.clear_frame()
        ManagePermissionsScreen(self.root, self.user)

    def assign_authorization_screen(self):
        self.clear_frame()
        AssignAuthorizationScreen(self.root, self.user)

    def logout(self):
        messagebox.showinfo("Logout", "You have successfully logged out.")
        self.clear_frame()
        from login_screen import LoginScreen
        LoginScreen(self.root)




if __name__ == "__main__":
    root = tk.Tk()
    # user =   # user-data wis already passing from login screen to admin dashboard
    app = ManageAuthorizationScreen(root, user)
    root.mainloop()



