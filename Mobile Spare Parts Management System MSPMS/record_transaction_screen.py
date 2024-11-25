


# Record Transaction Screen



import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys
from PIL import Image, ImageTk
from sale_transaction_screen import SaleTransactionScreen
from purchase_transaction_screen import PurchaseTransactionScreen
from utils import validate_input


class RecordTransactionScreen:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("MSPMS - Record Transaction Screen")
        self.root.geometry("920x430")
        self.root.minsize(920,430)
        self.root.maxsize(920,430)
        self.root.config(bg="skyblue")
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
        user_icon_path = os.path.join(BASE_DIR, "assets", "user_icon.png")

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
        self.profile_image = Image.open(user_icon_path)
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
        tk.Label(self.root, text="Record Transaction", font=("Helvetica", 20, "bold"), fg="black", bg="skyblue").grid(row=2, column=5, columnspan=4, padx=30, pady=20, sticky="nsew")

        # Buttons Frame
        buttons_frame = tk.Frame(self.root, bg="skyblue")
        buttons_frame.grid(row=3, column=5, columnspan=3, pady=(30,20), padx=(50,40), sticky="nsew")

        # Buttons Images
        back_btn_path = os.path.join(BASE_DIR, "assets", "back_arrow.png")
        purchase_transaction_path = os.path.join(BASE_DIR, "assets", "purchase_transaction.png")
        sale_transaction_path = os.path.join(BASE_DIR, "assets", "sale_transaction.png")        
        # 1
        icon_back_arrow_image = Image.open(back_btn_path)
        icon_back_arrow_image = icon_back_arrow_image.resize((35,35), Image.LANCZOS) 
        icon_back_arrow_photo = ImageTk.PhotoImage(icon_back_arrow_image)        
        # 2
        icon_purchase_transaction_image = Image.open(purchase_transaction_path)
        icon_purchase_transaction_image = icon_purchase_transaction_image.resize((35,35), Image.LANCZOS) 
        icon_purchase_transaction_photo = ImageTk.PhotoImage(icon_purchase_transaction_image)
        # 3
        icon_sale_transaction_image = Image.open(sale_transaction_path)
        icon_sale_transaction_image = icon_sale_transaction_image.resize((35,35), Image.LANCZOS)  
        icon_sale_transaction_photo = ImageTk.PhotoImage(icon_sale_transaction_image)

        # Keep a reference to the image
        self.icon_back_arrow_photo = icon_back_arrow_photo        
        self.icon_purchase_transaction_photo = icon_purchase_transaction_photo
        self.icon_sale_transaction_photo  = icon_sale_transaction_photo

        # Buttons        
        tk.Button(buttons_frame, image=icon_back_arrow_photo, text="Back", width=230, height=40, compound="left", anchor="w", padx=5, font=("Helvetica", 14), fg="#2C3E50", bg="#ECF0F1", command=self.back_to_dashboard_button, ).grid(row=1, column=0, pady=(20,10), padx=(20,10))
        tk.Button(buttons_frame, image=icon_purchase_transaction_photo, text="Purchase Transaction", width=230, height=40, compound="left", anchor="w", padx=5, font=("Helvetica", 14), fg="#2C3E50", bg="#ECF0F1", command=self.purchase_transaction_screen, ).grid(row=1, column=1, pady=(20,10), padx=(10,10))
        tk.Button(buttons_frame, image=icon_sale_transaction_photo, text="Sale Transaction", width=230, height=40, compound="left", anchor="w", padx=5, font=("Helvetica", 14), fg="#2C3E50", bg="#ECF0F1", command=self.sale_transaction_screen, ).grid(row=1, column=2, pady=(20,10), padx=(10,20))



    def back_to_dashboard_button(self):
        self.clear_frame()
        from admin_dashboard_screen import AdminDashboardScreen
        from salesman_dashboard_screen import SalesmanDashboardScreen
        if(self.user['role_id'] == 1):
            AdminDashboardScreen(self.root, self.user)
        else:
            SalesmanDashboardScreen(self.root, self.user)


    def purchase_transaction_screen(self):
        self.clear_frame()
        PurchaseTransactionScreen(self.root, self.user)


    def sale_transaction_screen(self):
        self.clear_frame()
        SaleTransactionScreen(self.root, self.user)


    def logout(self):
        messagebox.showinfo("Logout", "You have successfully logged out.")
        self.clear_frame()
        from login_screen import LoginScreen
        LoginScreen(self.root)




if __name__ == "__main__":
    root = tk.Tk()
    # user =   # user-data is already passing from dashboards
    app = RecordTransactionScreen(root, user)
    root.mainloop()




 

