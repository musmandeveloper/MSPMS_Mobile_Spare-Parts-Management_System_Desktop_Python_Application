



# Salesman Dashboard Screen



import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys
from PIL import Image, ImageTk
from manage_authorization_screen import ManageAuthorizationScreen
from manage_users_screen import ManageUsersScreen
from manage_spare_parts_screen import ManageSparePartsScreen
from record_transaction_screen import RecordTransactionScreen
from view_transactions_screen import ViewTransactionsScreen
from reporting_screen import ReportingScreen


class SalesmanDashboardScreen:
    def __init__(self, root, user):
        self.root = root
        self.root.title("MSPMS - Salesman Dashboard Screen")
        self.root.geometry("920x520")
        self.root.minsize(920, 520)
        self.root.maxsize(920, 520)
        self.root.config(bg="skyblue")
        self.user = user
        self.clear_frame()
        self.create_widgets()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_widgets(self):


        # Path to Project Root/Base directory
        if getattr(sys, 'frozen', False):
            # PyInstaller executable base path
            BASE_DIR = os.path.dirname(sys.executable)
        else:
            # Script base path
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # Creating final path
        logo_path = os.path.join(BASE_DIR, "assets", "app_logo_1.png")

        # Application Logo and Name
        app_logo_frame = tk.Frame(self.root, bg="skyblue")
        app_logo_frame.grid(row=0, column=5, columnspan=4, pady=40, padx=30, sticky="nsew")

        # Load application logo (replace 'app_logo.png' with your actual image path)
        self.app_logo_image = Image.open(logo_path)
        self.app_logo_image = self.app_logo_image.resize((60, 60), Image.LANCZOS)
        self.app_logo_photo = ImageTk.PhotoImage(self.app_logo_image)
        app_logo_label = tk.Label(app_logo_frame, image=self.app_logo_photo, bg="skyblue")
        app_logo_label.pack(side="left", padx=10)
        # Blue #5A55E6, Green #74e03a, Orange #F2571D
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
        profile_label.grid(row=1, column=5, padx=(10,270), sticky="w")

        welcome_label = tk.Label(profile_frame, text=f"Welcome {self.user['full_name']}", font=("Helvetica", 12), fg="black", bg="skyblue")
        welcome_label.grid(row=1, column=6, sticky="nsew")

        logout_button = tk.Button(profile_frame, text="Logout", font=("Helvetica", 14), fg="white", bg="#dc3545", command=self.logout, width=10, height=1)
        logout_button.grid(row=1, column=7, padx=(180,10), sticky="e")

        profile_frame.grid_columnconfigure(0, weight=1)
        profile_frame.grid_columnconfigure(1, weight=1)
        profile_frame.grid_columnconfigure(2, weight=1)

        # Dashboard Label
        tk.Label(self.root, text="Salesman Dashboard", font=("Helvetica", 20, "bold"), fg="black", bg="skyblue").grid(row=2, column=5, columnspan=4, padx=30, pady=20, sticky="nsew")

        # Buttons Frame
        buttons_frame = tk.Frame(self.root, bg="skyblue")
        buttons_frame.grid(row=3, column=5, columnspan=4, pady=30, padx=30, sticky="nsew")

        # Buttons Images
        manage_inventory_path = os.path.join(BASE_DIR, "assets", "manage_inventory.png")
        record_transaction_path = os.path.join(BASE_DIR, "assets", "record_transaction.png")
        view_transaction_path = os.path.join(BASE_DIR, "assets", "view_transaction.png")
        manage_report_path = os.path.join(BASE_DIR, "assets", "manage_report.png")
        # 1
        icon_manage_inventory_image = Image.open(manage_inventory_path)
        icon_manage_inventory_image = icon_manage_inventory_image.resize((35,35), Image.LANCZOS) 
        icon_manage_inventory_photo = ImageTk.PhotoImage(icon_manage_inventory_image)
        # 2
        icon_record_transaction_image = Image.open(record_transaction_path)
        icon_record_transaction_image = icon_record_transaction_image.resize((35,35), Image.LANCZOS)
        icon_record_transaction_photo = ImageTk.PhotoImage(icon_record_transaction_image)
        # 3
        icon_view_transaction_image = Image.open(view_transaction_path)
        icon_view_transaction_image = icon_view_transaction_image.resize((35,35), Image.LANCZOS) 
        icon_view_transaction_photo = ImageTk.PhotoImage(icon_view_transaction_image)
        # 4
        icon_manage_report_image = Image.open(manage_report_path)
        icon_manage_report_image = icon_manage_report_image.resize((35,35), Image.LANCZOS) 
        icon_manage_report_photo = ImageTk.PhotoImage(icon_manage_report_image) 

        # Keep a reference to the image
        self.icon_manage_inventory_photo = icon_manage_inventory_photo
        self.icon_record_transaction_photo = icon_record_transaction_photo
        self.icon_view_transaction_photo  = icon_view_transaction_photo 
        self.icon_manage_report_photo = icon_manage_report_photo

        # Buttons
        tk.Button(buttons_frame, image=icon_manage_inventory_photo, text="Manage Spare Parts", width=223, height=40, compound="left", anchor="w", padx=5, font=("Helvetica", 14), fg="#2C3E50", bg="#ECF0F1", command=self.manage_spare_parts_screen, ).grid(row=0, column=0, pady=(20,10), padx=(20,10))
        tk.Button(buttons_frame, image=icon_record_transaction_photo, text="Record Transaction", width=223, height=40, compound="left", anchor="w", padx=5, font=("Helvetica", 14), fg="#2C3E50", bg="#ECF0F1", command=self.record_transaction_screen, ).grid(row=0, column=1, pady=(20,10), padx=(10,10))
        tk.Button(buttons_frame, image=icon_view_transaction_photo, text="View Transactions", width=223, height=40, compound="left", anchor="w", padx=5, font=("Helvetica", 14), fg="#2C3E50", bg="#ECF0F1", command=self.view_transactions_screen, ).grid(row=0, column=2, pady=(20,10), padx=(10,20))
        tk.Button(buttons_frame, image=icon_manage_report_photo, text="Manage Reports", width=223, height=40, compound="left", anchor="w", padx=5, font=("Helvetica", 14), fg="#2C3E50", bg="#ECF0F1", command=self.manage_reports_screen, ).grid(row=1, column=1, pady=(20,10), padx=(10,10))


    def manage_spare_parts_screen(self):
        self.clear_frame()
        ManageSparePartsScreen(self.root, self.user)

    def record_transaction_screen(self):
        self.clear_frame()
        RecordTransactionScreen(self.root, self.user)

    def view_transactions_screen(self):
        self.clear_frame()
        ViewTransactionsScreen(self.root, self.user)

    def manage_reports_screen(self):
        self.clear_frame()
        ReportingScreen(self.root, self.user)

    def logout(self):
        messagebox.showinfo("Logout", "You have successfully logged out.")
        self.clear_frame()
        from login_screen import LoginScreen
        LoginScreen(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    # user =   # user-data was already passing from login screen to admin dashboard
    app = SalesmanDashboardScreen(root, user)
    root.mainloop()




