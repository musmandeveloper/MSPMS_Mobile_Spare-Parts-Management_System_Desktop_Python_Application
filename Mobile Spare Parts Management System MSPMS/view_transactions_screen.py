



# View all transactions


import tkinter as tk
from tkinter import ttk, messagebox
from transactions import fetch_transactions, fetch_transaction_old_data, update_transaction, delete_transaction
from inventory import fetch_parts
from update_transaction_screen import UpdateTransactionScreen
from utils import validate_input

class ViewTransactionsScreen:
    def __init__(self, root, user):
        self.root = root
        self.root.title("MSPMS - View Transactions")
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
        title = tk.Label(self.root, text="View Transactions", font=("Helvetica", 24, "bold"),  fg="black", bg="skyblue")
        title.pack(pady=20)

        # Search Frame
        search_frame = tk.Frame(self.root, bg="skyblue")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search:", bg="skyblue", fg="black", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Helvetica", 12), bg="white", fg="black", insertbackground="black")
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_transaction_screen, bg="#007bff", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Clear Search", command=self.load_transactions, bg="#6c757d", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)

        # TreeView Table

        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white", font=("Helvetica", 12))
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background="blue", foreground="black")
        style.map('Treeview', background=[('selected', '#007bff')])

        table_frame = tk.Frame(self.root, bg="skyblue")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(20, 10))

        self.transaction_list = ttk.Treeview(table_frame, columns=("Date", "Time", "Transaction_Id", "Username", "Type", "Items_Names", "Items_Quantities", "Items_Purchase_Prices", "Items_Sale_Prices", "Items_Total_Prices", "Grand_Total_Price", "Paid_Price", "Balance_Price"), show='headings')
        self.transaction_list.heading("Date", text="Date")
        self.transaction_list.heading("Time", text="Time")
        self.transaction_list.heading("Transaction_Id", text="Transaction ID")
        self.transaction_list.heading("Username", text="Username")
        self.transaction_list.heading("Type", text="Type")
        self.transaction_list.heading("Items_Names", text="Items Names")
        self.transaction_list.heading("Items_Quantities", text="Items_Quantities")
        self.transaction_list.heading("Items_Purchase_Prices", text="Items Purchase Prices")
        self.transaction_list.heading("Items_Sale_Prices", text="Items Sale Prices")
        self.transaction_list.heading("Items_Total_Prices", text="Items Total Prices")
        self.transaction_list.heading("Grand_Total_Price", text="Grand Total Price")
        self.transaction_list.heading("Paid_Price", text="Paid Price")
        self.transaction_list.heading("Balance_Price", text="Balance Price")

        for col in self.transaction_list["columns"]:
            self.transaction_list.column(col, width=120, minwidth=100, stretch=tk.NO)

        self.transaction_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.transaction_list.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.transaction_list.xview)
        self.transaction_list.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)
        self.transaction_list.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # ListBox Content 
        self.transaction_list.bind("<<TreeviewSelect>>", self.on_transaction_select)

        # Buttons Frame
        buttons_frame = tk.Frame(self.root, bg="skyblue")
        buttons_frame.pack(pady=20)
        # Buttons
        tk.Button(buttons_frame, text="Back", command=self.back_to_dashboard_button, bg="#2ECC71", fg="black", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        self.update_button = tk.Button(buttons_frame, text="Update Transaction", command=self.update_transaction_screen, bg="#ffc107", fg="black", font=("Helvetica", 12), state='disabled', width=15)
        self.update_button.pack(side=tk.LEFT, padx=10)
        # Show the Delete button to all Users except user role 'salesman'
        if(self.user['role_id'] != 2): 
            self.delete_button = tk.Button(buttons_frame, text="Delete Transaction", command=self.delete_transaction_screen, bg="#dc3545", fg="white", font=("Helvetica", 12), state='disabled', width=15)
            self.delete_button.pack(side=tk.LEFT, padx=10)
        else:
            self.delete_button = None  # Set to None for 'Salesman' to avoid errors

        # Load all data into table
        self.load_transactions()


    def back_to_dashboard_button(self):
        self.clear_frame()
        from admin_dashboard_screen import AdminDashboardScreen
        from salesman_dashboard_screen import SalesmanDashboardScreen
        if(self.user['role_id'] == 1):
            AdminDashboardScreen(self.root, self.user)
        else:
            SalesmanDashboardScreen(self.root, self.user)        


    def load_transactions(self):
        for i in self.transaction_list.get_children():
            self.transaction_list.delete(i)
        transactions = fetch_transactions()  # Call the backend method and receive the returned data
        # Inserting fetched data into tables cells / list
        for transaction in  transactions:
            transaction_values = (
                transaction['date'],
                transaction['time'],
                transaction['id'],
                transaction['user_id'],
                transaction['type'],
                ', '.join(transaction['item_names']),
                ', '.join(map(str, transaction['item_quantities'])),
                ', '.join(map(str, transaction['item_purchase_prices'])),
                ', '.join(map(str, transaction['item_sale_prices'])),
                ', '.join(map(str, transaction['item_total_prices'])),
                transaction['grand_total_price'],
                transaction['paid_price'],
                transaction['balance_price']
            )
            self.transaction_list.insert('', 'end', values=transaction_values)



    def on_transaction_select(self, event):
        selected_transaction = self.transaction_list.selection()
        if selected_transaction:
            self.update_button.config(state='normal')
            if self.user['role_id'] != 2:
                self.delete_button.config(state='normal')
            else:
                self.delete_button.config(state='disabled')
        else:
            self.update_button.config(state='disabled')
            self.delete_button.config(state='disabled')


    def update_transaction_screen(self):
        selected_item = self.transaction_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a transaction to update")
            return
        transaction_id = self.transaction_list.item(selected_item)['values'][2]
        transaction_old_data = fetch_transaction_old_data(transaction_id)
        print(f"Received transaction old data for ID {transaction_id} = {transaction_old_data}")
        self.clear_frame()
        UpdateTransactionScreen(self.root, self.user, transaction_old_data)    


    def delete_transaction_screen(self):
        selected_item = self.transaction_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a transaction to delete")
            return
        transaction_id = self.transaction_list.item(selected_item)['values'][2]
        print("Selected Deleting Transaction's ID = ", transaction_id)
        self.delete_transaction(transaction_id)


    def delete_transaction(self, transaction_id):
        delete_transaction(transaction_id) # Call Backend Function
        messagebox.showinfo("Success", "Successfully deleted selected transaction")
        self.load_transactions()



    def search_transaction_screen(self):
        search_term = self.search_entry.get().strip().lower()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter anyone of Date Time, Transaction Id, User Id, Transaction Type as search term")
            return
        matched_transactions = []
        transactions = fetch_transactions() # Call the backend method and receive the returned data 
        for transaction in transactions:
            date = str(transaction['date']).lower(),
            time = str(transaction['time']).lower(),
            id = str(transaction['id']).lower(), 
            user_id = str(transaction['user_id']).lower(), 
            type = transaction['type'].lower(), 
            if search_term in date or search_term in time or search_term in id or search_term in user_id or search_term in type:
                matched_transactions.append(transaction)
        self.display_matched_transactions(matched_transactions)


    def display_matched_transactions(self, matched_transactions):
        self.transaction_list.delete(*self.transaction_list.get_children())
        for transaction in matched_transactions:
            transaction = (
                transaction['date'],
                transaction['time'],
                transaction['id'],
                transaction['user_id'],
                transaction['type'],
                ', '.join(transaction['item_names']),
                ', '.join(map(str, transaction['item_quantities'])),
                ', '.join(map(str, transaction['item_purchase_prices'])),
                ', '.join(map(str, transaction['item_sale_prices'])),
                transaction['grand_total_price']
            )
            self.transaction_list.insert('', 'end', values=transaction)





if __name__ == "__main__":
    root = tk.Tk()
    app = ViewTransactionsScreen(root, user=None)
    root.mainloop()





'''
    def update_transaction_screen(self):
        selected_item = self.transaction_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a transaction to update")
            return

        update_transaction_window = tk.Toplevel(self.root)
        update_transaction_window.geometry("780x750")
        update_transaction_window.minsize(780, 750)
        update_transaction_window.maxsize(780, 750)
        update_transaction_window.title("Update Transaction")
        update_transaction_window.config(bg="skyblue")

        # Title - Centered
        title = tk.Label(update_transaction_window, text="Update Transaction", font=("Helvetica", 24, "bold"), bg="skyblue", fg="white")
        title.pack(pady=20)

        # Frame for Form Fields
        form_frame = tk.Frame(update_transaction_window, bg="skyblue")
        form_frame.pack(pady=10)

        # List of Fields to Display
        labels = ["Username", "Type", "Items", "Grand Total Price", "Paid Price", "Balance Price"]
        entries = []
    
        # Fetch old data for the selected transaction
        transaction_id = self.transaction_list.item(selected_item)['values'][2]
        self.transaction_id = transaction_id  # Store as class attribute
        transaction_data = fetch_transaction_old_data(transaction_id)  # Backend Method

        # Fetched Old data from database
        ts_username = transaction_data['user_id']
        ts_type = transaction_data['type']
        item_names = transaction_data['item_names']
        item_quantities = transaction_data['item_quantities']
        item_purchase_prices = transaction_data['item_purchase_prices']
        item_sale_prices = transaction_data['item_sale_prices']
        item_total_prices = transaction_data['item_total_prices']
        ts_grand_total_price = transaction_data['grand_total_price']
        ts_paid_price = transaction_data['paid_price']
        ts_balance_price = transaction_data['balance_price']            

        # Username
        tk.Label(form_frame, text="Username", bg="skyblue", fg="black", font=("Helvetica", 12)).grid(row=0, column=0, pady=10, padx=10, sticky='e')
        username_entry = tk.Entry(form_frame, font=("Helvetica", 12))
        username_entry.insert(0, ts_username)  # Display old username
        username_entry.grid(row=0, column=1, pady=10, padx=10)

        # Type - Sale or Purchase Dropdown
        tk.Label(form_frame, text="Type", bg="skyblue", fg="black", font=("Helvetica", 12)).grid(row=1, column=0, pady=10, padx=10, sticky='e')
        type_combobox = ttk.Combobox(form_frame, font=("Helvetica", 12), width=18, values=["Sale", "Purchase"])
        type_combobox.set(ts_type)  # Set the old type
        type_combobox.grid(row=1, column=1, pady=10, padx=10)

        # Frame for Buttons at the Bottom
        button_frame = tk.Frame(update_transaction_window, bg="skyblue")
        button_frame.pack(pady=20)
     
        # Buttons - Center Aligned in button_frame
        tk.Button(button_frame, text="Cancel", bg="#dc3545", fg="white", font=("Helvetica", 12),
                command=update_transaction_window.destroy).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Update", bg="#ffc107", fg="black", font=("Helvetica", 12),
                command=self.update_transaction(update_transaction_window)).grid(row=0, column=1, padx=10)


    # Update frontend function
    def update_transaction(self, window):
        messagebox.showinfo("Success", "Updating Transaction feature is under-development now")
        window.destroy()
        self.load_transactions()


'''