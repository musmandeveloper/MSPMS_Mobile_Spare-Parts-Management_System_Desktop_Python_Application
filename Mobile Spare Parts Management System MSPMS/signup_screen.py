



# Signup Screen


import tkinter as tk
from tkinter import messagebox
import os
import sys
from PIL import Image, ImageTk  # To handle the eye icon image
import re  # For password validation
from auth import signup


class SignUpScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("MSPMS - Sign Up")
        self.root.geometry("600x450")
        self.root.minsize(600, 450)
        self.root.maxsize(600, 450)
        self.root.config(bg="skyblue")
        self.show_password = False  # Initial state for password visibility
        self.clear_frame()
        self.signup_screen()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def signup_screen(self):

        # Title
        title_label = tk.Label(self.root, text="Sign Up", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue")
        title_label.pack(pady=10)

        # Note
        note_label = tk.Label(self.root, text="Note: Only Admin (Store Owner) can Sign-Up, he will create Salesmen Accounts.", font=("Helvetica", 12, "italic"), fg="red", bg="skyblue")
        note_label.pack(pady=5)

        # Form Frame
        form_frame = tk.Frame(self.root, bg="skyblue")
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Full Name", font=("Helvetica", 14), bg="skyblue").grid(row=0, column=0, pady=10, padx=10)
        self.full_name = tk.Entry(form_frame, font=("Helvetica", 14), width=25)
        self.full_name.grid(row=0, column=2, pady=10, padx=10)

        tk.Label(form_frame, text="Username", font=("Helvetica", 14), bg="skyblue").grid(row=1, column=0, pady=10, padx=10)
        self.username = tk.Entry(form_frame, font=("Helvetica", 14), width=25)
        self.username.grid(row=1, column=2, pady=10, padx=10)

        tk.Label(form_frame, text="Password", font=("Helvetica", 14), bg="skyblue").grid(row=2, column=0, pady=10, padx=10)
        # Password Frame for Password field with eye icon
        password_frame = tk.Frame(form_frame, bg="white")  # Frame to hold both the Entry and the eye icon
        password_frame.grid(row=2, column=2, pady=10, padx=10)
        # Password Field 
        self.password = tk.Entry(password_frame, font=("Helvetica", 14), show="*", width=23, bd=0)  # Slightly reduced width to accommodate the icon
        self.password.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
        # Path to Project Root/Base directory
        if getattr(sys, 'frozen', False):
            # PyInstaller executable base path
            BASE_DIR = os.path.dirname(sys.executable)
        else:
            # Script base path
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # Creating Final assets/resources path
        eye_show_icon_path = os.path.join(BASE_DIR, "assets", "eye_show.png")
        eye_hide_icon_path = os.path.join(BASE_DIR, "assets", "eye_hide.png")
        # Toggle &  Load the eye icon images
        self.eye_image_show = Image.open(eye_show_icon_path )  # Path to the "show" eye icon image
        self.eye_image_show = self.eye_image_show.resize((15, 10), Image.LANCZOS)
        self.eye_icon_show = ImageTk.PhotoImage(self.eye_image_show)
        self.eye_image_hide = Image.open(eye_hide_icon_path )  # Path to the "hide" eye icon image
        self.eye_image_hide = self.eye_image_hide.resize((15, 15), Image.LANCZOS)
        self.eye_icon_hide = ImageTk.PhotoImage(self.eye_image_hide)
 
        # Eye icon button
        self.eye_button = tk.Button(password_frame, image=self.eye_icon_hide, command=self.toggle_password, bg="white", bd=0)
        self.eye_button.pack(side=tk.RIGHT, padx=5)

        # Button Frame for Sign Up, Reset, Exit buttons
        button_frame = tk.Frame(self.root, bg="skyblue")
        button_frame.pack(pady=10)

        # Exit Button
        exit_button = tk.Button(button_frame, text="Exit", font=("Helvetica", 14), fg="white", bg="red", command=self.exit_application, width=10)
        exit_button.grid(row=0, column=0, padx=10)

        # Sign Up Button
        signup_button = tk.Button(button_frame, text="Sign Up", font=("Helvetica", 14), fg="white", bg="#1004FD", command=self.signup_user, width=20)
        signup_button.grid(row=0, column=1, padx=10)

        # Reset Button
        reset_button = tk.Button(button_frame, text="Reset", font=("Helvetica", 14), fg="white", bg="grey", command=self.reset_fields, width=10)
        reset_button.grid(row=0, column=2, padx=10)

        # OR Label
        or_label = tk.Label(self.root, text="OR", font=("Helvetica", 12), fg="red", bg="skyblue")
        or_label.pack(pady=5)

        # Sign In Button
        signin_button = tk.Button(self.root, text="Sign In", font=("Helvetica", 14), fg="black", bg="#FCED03", command=self.login_screen, width=30)
        signin_button.pack(pady=5)


    def toggle_password(self):
        """Toggle the password visibility."""
        if self.show_password:
            self.password.config(show="*")
            self.eye_button.config(image=self.eye_icon_hide)
            self.show_password = False
        else:
            self.password.config(show="")
            self.eye_button.config(image=self.eye_icon_show)
            self.show_password = True

    def signup_user(self):
        full_name = self.full_name.get()
        username = self.username.get()
        password = self.password.get()
        
        # Validation checks
        if not full_name:
            messagebox.showerror("Error", "Full Name cannot be empty")
            return
                
        if not username:
            messagebox.showerror("Error", "Username cannot be empty")
            return
        
        if not password:
            messagebox.showerror("Error", "Password cannot be empty")
            return
        
        if not password[0].isalpha():
            messagebox.showerror("Error", "Password must start with a letter (alphabet)")
            return

        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long")
            return

        if not re.search(r"[A-Z]", password):
            messagebox.showerror("Error", "Password must include at least one capital letter")
            return
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            messagebox.showerror("Error", "Password must include at least one special character/symbol ")
            return
        
        if not re.search(r"\d", password):
            messagebox.showerror("Error", "Password must include at least one numeric digit")
            return

        # Authenticating
        user_created = signup(username, password, full_name) 
        if user_created:
            messagebox.showinfo("Success", "User Successfully Signed-Up")
        else:
            messagebox.showerror("Error", "Error user Not Signed-Up")

    def reset_fields(self):
        """Clear the full name, username, and password fields."""
        self.full_name.delete(0, tk.END)
        self.username.delete(0, tk.END)
        self.password.delete(0, tk.END)

    def exit_application(self):
        """Properly exit the application."""
        self.root.quit()

    def login_screen(self):
        self.clear_frame()
        from login_screen import LoginScreen
        LoginScreen(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    SignUpScreen(root)
    root.mainloop()




