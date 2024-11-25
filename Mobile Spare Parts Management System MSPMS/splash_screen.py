



# Splash Frontend Screen




import tkinter as tk
from login_screen import LoginScreen
import os
import sys
from PIL import Image, ImageTk


class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("MSPMS - Splash Screen")
        self.root.geometry("850x420")
        self.root.minsize(850,420)
        self.root.maxsize(850,420)
        self.root.config(bg="skyblue")
        self.create_widgets()
        self.show_splash()

    def create_widgets(self):
        # Get the directory where the script is located
        #base_dir = os.path.dirname(__file__)
        # Above or Below
        if getattr(sys, 'frozen', False):
            BASE_DIR = os.path.dirname(sys.executable)
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # Construct the relative path to the image
        logo_path = os.path.join(BASE_DIR, "assets", "app_logo_1.png")
        self.app_logo_image = Image.open(logo_path)
        
        #self.app_logo_image = Image.open("assets/app_logo_1.png")
        self.app_logo_image = self.app_logo_image.resize((180, 250), Image.LANCZOS)
        self.app_logo_photo = ImageTk.PhotoImage(self.app_logo_image)
        app_logo_label = tk.Label(self.root, image=self.app_logo_photo, bg="skyblue")
        app_logo_label.pack(pady=40)

        # Application title
        # Blue #5A55E6,  Orange #F2571D
        app_title_label = tk.Label(self.root, text="Mobile Spare Parts Management System - MSPMS", font=("Helvetica", 24, "bold"), fg="#5A55E6", bg="skyblue")
        app_title_label.pack(pady=0, padx=10)

    def show_splash(self):
        self.root.after(5000, self.show_login)

    def show_login(self):
        self.clear_frame()
        LoginScreen(self.root)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()







