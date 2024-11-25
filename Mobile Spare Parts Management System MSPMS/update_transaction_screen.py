

# Update Transaction Screen


# Import libraries and backend functions
import tkinter as tk
from tkinter import ttk, messagebox
from inventory import fetch_parts
from transactions import update_transaction

class UpdateTransactionScreen:
    def __init__(self, root, user, transaction_old_data):
        self.root = root
        self.user = user
        self.transaction_old_data = transaction_old_data
        self.root.title("MSPMS - Update Transaction")
        self.root.geometry("920x580")
        self.root.minsize(920,580)
        self.root.maxsize(920,580)
        self.root.config(bg="skyblue")

        ## 01 Unpacking transaction old data received
        print(f"Received Transaction Old Data in update screen is : {self.transaction_old_data}")
        # Transaction Info Variables
        self.old_transaction_id = self.transaction_old_data['id']        
        self.old_transaction_date = self.transaction_old_data['date']
        self.old_transaction_time = self.transaction_old_data['time']
        self.old_transaction_type = self.transaction_old_data['type']        
        self.old_transaction_user_id = self.transaction_old_data['user_id']        
        self.old_transaction_username = self.transaction_old_data['username']
        # Item Info Variables
        self.old_item_ids = self.transaction_old_data['item_ids']
        self.old_item_statuses = self.transaction_old_data['item_statuses']
        self.old_item_names = self.transaction_old_data['item_names']
        self.old_item_categories = self.transaction_old_data['item_categories']
        self.old_item_quantities = self.transaction_old_data['item_quantities']
        self.old_item_purchase_prices = self.transaction_old_data['item_purchase_prices']
        self.old_item_sale_prices = self.transaction_old_data['item_sale_prices']
        self.old_item_total_prices = self.transaction_old_data['item_total_prices']
        # Total Prices and Payment Info Variables
        self.old_grand_total_price = self.transaction_old_data['grand_total_price']
        self.old_paid_price = self.transaction_old_data['paid_price']
        self.old_balance_price = self.transaction_old_data['balance_price']

        ## 02 Creating Form Fields

        # Transaction Info
        self.create_transaction_info()
        # Items Table
        self.create_items_table()
        # Items Buttons
        self.create_items_buttons()
        # Total Price, Paid, Balance
        self.create_total_display()
        # Buttons
        self.create_bottom_buttons()

    def create_transaction_info(self):

        # Dashboard Title
        tk.Label(self.root, text="Update Transaction", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue").pack(pady=20)

        # Info fields Frame
        info_frame = tk.Frame(self.root, bg="skyblue")
        info_frame.pack(pady=5)

        tk.Label(info_frame, text="Date:", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        tk.Label(info_frame, text=self.old_transaction_date, font=("Helvetica", 12), width=20, anchor="w", relief="sunken").grid(row=0, column=1, padx=5, pady=5)

        tk.Label(info_frame, text="Time:", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=0, column=3, padx=(60,5), pady=5, sticky='w')
        tk.Label(info_frame, text=self.old_transaction_time, font=("Helvetica", 12), width=20, anchor="w", relief="sunken").grid(row=0, column=4, padx=5, pady=5)

        tk.Label(info_frame, text="Transaction ID:", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        tk.Label(info_frame, text=self.old_transaction_id, font=("Helvetica", 12), width=20, anchor="w", relief="sunken").grid(row=1, column=1, padx=5, pady=5)

        tk.Label(info_frame, text="Username:", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=1, column=3, padx=(60,5), pady=5, sticky='w')
        tk.Label(info_frame, text=self.old_transaction_username, font=("Helvetica", 12), width=20, anchor="w", relief="sunken").grid(row=1, column=4, padx=5, pady=5)
        
        tk.Label(info_frame, text="Type:", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.type_var = tk.StringVar(value=self.old_transaction_type)
        self.type_combobox = ttk.Combobox(info_frame, textvariable=self.type_var, values=["Purchase", "Sale"], font=("Helvetica", 12), width=18,)
        self.type_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.type_combobox.bind("<<ComboboxSelected>>", self.update_total_prices)       

    def create_items_table(self):
        # Table Style
        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white", font=("Helvetica", 12))
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background="blue", foreground="black")
        style.map('Treeview', background=[('selected', '#007bff')])
        # Table Frame
        self.items_frame = tk.Frame(self.root, bg="skyblue")
        self.items_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=30)
        # Table Column Headings
        self.table = ttk.Treeview(self.items_frame, height=3, columns=("ID", "Status", "Name", "Category", "Quantity", "Purchase Price", "Sale Price", "Total Price", "Action"), show='headings')
        self.table.heading("ID", text="ID")
        self.table.heading("Status", text="Status")        
        self.table.heading("Name", text="Name")
        self.table.heading("Category", text="Category")
        self.table.heading("Quantity", text="Quantity")
        self.table.heading("Purchase Price", text="Purchase Price")
        self.table.heading("Sale Price", text="Sale Price")
        self.table.heading("Total Price", text="Total Price")
        self.table.heading("Action", text="Action")
        # Table Columns width config
        for col in self.table["columns"]:
            self.table.column(col, width=100, minwidth=70, stretch=tk.NO)
        # Table display config
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Table Scrollbars
        v_scrollbar = ttk.Scrollbar(self.items_frame, orient="vertical", command=self.table.yview)
        h_scrollbar = ttk.Scrollbar(self.items_frame, orient="horizontal", command=self.table.xview)
        self.table.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)
        self.table.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        # Table Frame config
        self.items_frame.grid_rowconfigure(0, weight=1)
        self.items_frame.grid_columnconfigure(0, weight=1)
        # Add rows in table for each item, with old data
        for i in range(len(self.old_item_names)):
            self.table.insert('', 'end', values=(
                self.old_item_ids[i],
                self.old_item_statuses[i],
                self.old_item_names[i],
                self.old_item_categories[i],
                self.old_item_quantities[i],
                self.old_item_purchase_prices[i],
                self.old_item_sale_prices[i],
                self.old_item_total_prices[i],
                "Delete"  # Action column text value based button
            ))
        
        # Bind event for editing "Quantity" column
        self.table.bind("<Double-1>", self.on_double_click)

        # Bind event for "Delete" action
        self.table.bind("<ButtonRelease-1>", self.on_item_click)


    def on_double_click(self, event):
        item = self.table.selection()[0]  # Get selected row
        col = self.table.identify_column(event.x)  # Get the column clicked
        if col == "#5":  # If "Quantity" column is clicked
            self.edit_quantity(item)
    def edit_quantity(self, item):
        # Get the bounding box of the selected row and column for Quantity
        row_bbox = self.table.bbox(item, column=4)  # Column index for "Quantity"
        # Create an Entry widget
        entry = tk.Entry(self.items_frame)
        entry.place(x=row_bbox[0], y=row_bbox[1], width=row_bbox[2], height=row_bbox[3])
        # Re-fill the current quantity value
        current_quantity = self.table.item(item, 'values')[4]
        entry.insert(0, current_quantity)
        # Bind the return key (Enter) to update the table and remove the entry widget
        entry.bind("<Return>", lambda e: self.save_quantity(item, entry))
    def save_quantity(self, item, entry):
        # Get the new quantity entered by the user
        new_quantity = entry.get()
        # Update the quantity value in the table
        values = list(self.table.item(item, 'values'))
        values[4] = new_quantity  # Update "Quantity" field
        self.table.item(item, values=values)
        # Remove the Entry widget
        entry.destroy()
        # Call the update_total_prices function to recalculate the total price
        self.update_total_prices()  # No event argument required here
        

    def on_item_click(self, event):
        selected_item = self.table.selection()  # Get selected item
        cur_item = self.table.item(selected_item)  # Get the item data
        col = self.table.identify_column(event.x)  # Identify clicked column
        # Check if "Action" column (7th column) was clicked
        if col == '#9':  
            index = self.table.index(selected_item)  # Get the index of the selected item
            self.delete_item(index)  # Call delete function    
    def delete_item(self, index):
        selected_item = self.table.get_children()[index]  # Get the item by its index
        self.table.delete(selected_item)  # Delete the selected item row from the table
        # Call update_grand_total after inserting new item row in items table
        self.update_grand_total()

    def create_items_buttons(self):
        items_button_frame = tk.Frame(self.root, bg="skyblue")
        items_button_frame.pack(pady=(5,10))
        # Add New Item Button
        add_button = tk.Button(items_button_frame, text="Add New Item", command=self.add_new_item, font=("Helvetica", 12), bg="#007bff", fg="white", width=12)
        add_button.pack(side="left", padx=5)

    # Insert New Row after some processing
    def add_row(self, id, status, name, category, quantity, purchase_price, sale_price):
        total_price = quantity * sale_price if self.type_var.get() == "Sale" else quantity * purchase_price
        self.table.insert("", "end", values=(id, status, name, category, quantity, purchase_price, sale_price, total_price))

    def create_total_display(self):
        self.total_frame = tk.Frame(self.root, bg="skyblue")
        self.total_frame.pack(pady=(20,10))
        # Grand Total Price
        tk.Label(self.total_frame, text="Grand Total Price:", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.grand_total_price_value_label = tk.Label(self.total_frame, text=self.old_grand_total_price, font=("Helvetica", 12), width=15, anchor="w", relief="sunken")
        self.grand_total_price_value_label.grid(row=0, column=1, padx=5, pady=5)        
        # Paid Price
        tk.Label(self.total_frame, text="Paid Price:", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=0, column=3, padx=(15,5), pady=5, sticky='e')
        self.paid_price_entry = tk.Entry(self.total_frame, font=("Helvetica", 12), width=15)
        self.paid_price_entry.grid(row=0, column=4, padx=5, pady=5)
        self.paid_price_entry.insert(0, self.old_paid_price)
        self.paid_price_entry.bind("<KeyRelease>", self.update_paid_price)  # Bind KeyRelease event
        # Balance Price
        tk.Label(self.total_frame, text="Balanced Price:", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=0, column=5, padx=(15,5), pady=5, sticky='e')
        self.balance_price_value_label = tk.Label(self.total_frame, text=self.old_balance_price, font=("Helvetica", 12), width=15, anchor="w", relief="sunken")
        self.balance_price_value_label.grid(row=0, column=6, padx=5, pady=5) 

    def create_bottom_buttons(self):
        button_frame = tk.Frame(self.root, bg="skyblue")
        button_frame.pack(pady=(25,40))
        # Cancel Button
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel_transaction, font=("Helvetica", 14), bg="#dc3545", fg="white", width=15)
        cancel_button.pack(side="left", padx=(15,15))
        # Update Button
        update_button = tk.Button(button_frame, text="Update", command=self.update_transaction, font=("Helvetica", 14), bg="#ffc107", fg="black", width=15)
        update_button.pack(side="left", padx=(15,15))

    # Insert New Item
    def add_new_item(self):
        # Get current transaction type
        current_type = self.type_var.get()
        # Create a new Toplevel window (Pop-up form)
        popup = tk.Toplevel(self.root, bg="skyblue")
        popup.title("MSPMS - Add New Item")
        popup.geometry("450x430")
        popup.minsize(450,430)
        popup.maxsize(450,430)  

        # Form Fields Elements based on transaction type
        if current_type == "Purchase":
            # Pop-Up Screen Title
            title = tk.Label(popup, text="Add New Purchase Item", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue")
            title.grid(row=0, column=0, columnspan=2, padx=(45,45), pady=20, sticky="nsew")
            # Select Item Dropdown
            inventory_items = fetch_parts()  # call backend function to get inventory data
            # Select Item Dropdown 
            tk.Label(popup, text="Select Item", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=1, column=0, padx=(20,5), pady=5, sticky="w")
            item_var = tk.StringVar(popup)
            # Use correct index below by fetched data sequence : (id, name, category, purchase_price, sale_price)
            item_names = [f"{item[0]} - {item[1]} - {item[2]} - {item[3]} - {item[4]}" for item in inventory_items]
            self.item_dropdown = ttk.Combobox(popup, textvariable=item_var, values=item_names, font=("Helvetica", 10), width=32)
            self.item_dropdown.grid(row=1, column=1, padx=(5,20), pady=5)
            self.item_dropdown.bind("<<ComboboxSelected>>", self.on_part_selected)
            # "OR" text in center
            tk.Label(popup, text="OR", font=("Helvetica", 16, "bold"), fg="red", bg="skyblue").grid(row=2, column=0, columnspan=2, pady=10, padx=(80,80), sticky="nsew")
            # Name Entry Field
            tk.Label(popup, text="Name", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=3, column=0, padx=(20,5), pady=5,  sticky="w")
            self.name_entry = tk.Entry(popup, font=("Helvetica", 12), width=27)
            self.name_entry.grid(row=3, column=1, padx=(5,20), pady=5)
            # Category Entry Field
            tk.Label(popup, text="Category", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=4, column=0, padx=(20,5), pady=5, sticky="w")
            self.category_entry = tk.Entry(popup, font=("Helvetica", 12), width=27)
            self.category_entry.grid(row=4, column=1, padx=(5,20), pady=5)
            # Quantity Entry Field
            tk.Label(popup, text="Quantity", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=5, column=0, padx=(20,5), pady=5, sticky="w")
            self.quantity_entry = tk.Entry(popup, font=("Helvetica", 12), width=27)
            self.quantity_entry.grid(row=5, column=1, padx=(5,20), pady=5)
            # Purchase Price Entry Field
            tk.Label(popup, text="Purchase Price", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=6, column=0, padx=(20,5), pady=5, sticky="w")
            self.purchase_price_entry = tk.Entry(popup, font=("Helvetica", 12), width=27)
            self.purchase_price_entry.grid(row=6, column=1, padx=(5,20), pady=5)
            # Sale Price Entry Field
            tk.Label(popup, text="Sale Price", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=7, column=0, padx=(20,5), pady=5, sticky="w")
            self.sale_price_entry = tk.Entry(popup, font=("Helvetica", 12), width=27)
            self.sale_price_entry.grid(row=7, column=1, padx=(5,20), pady=5)
            # Add Item button for Purchase
            tk.Button(popup, text="Add Item", command=lambda: self.add_purchase_item(self.name_entry.get(), self.category_entry.get(), self.quantity_entry.get(), self.purchase_price_entry.get(), self.sale_price_entry.get(), popup), font=("Helvetica", 14), bg="#007bff", fg="white", width=3).grid(row=8, columnspan=2, padx=(50,50), pady=20, sticky="nsew")
        
        elif current_type == "Sale":
            # Pop-Up Screen Title
            title = tk.Label(popup, text="Add New Sale Item", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue")
            title.grid(row=0, column=0, columnspan=2, padx=(65,65), pady=20, sticky="nsew")            
            # Fetch currently available parts from the inventory
            inventory_items = fetch_parts()  # call backend function to get inventory data
            # Select Item Dropdown 
            tk.Label(popup, text="Select Item", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=1, column=0, padx=(20,10), pady=5, sticky="w")
            item_var = tk.StringVar(popup)
            # Use correct index below by fetched data sequence : (id, name, category, purchase_price, sale_price)
            item_names = [f"{item[0]} - {item[1]} - {item[2]} - {item[3]} - {item[4]}" for item in inventory_items]
            item_dropdown = ttk.Combobox(popup, textvariable=item_var, values=item_names, font=("Helvetica", 10), width=38)
            item_dropdown.grid(row=1, column=1, padx=(10,20), pady=5)
            # Quantity Entry Field
            tk.Label(popup, text="Quantity", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=2, column=0, padx=(20,10), pady=5)
            quantity_entry = tk.Entry(popup, font=("Helvetica", 12), width=32)
            quantity_entry.grid(row=2, column=1, padx=(10,20), pady=5)
            # Add Item button for Sale
            tk.Button(popup, text="Add Item", command=lambda: self.validate_sale_item(item_var.get(), quantity_entry.get(), inventory_items, popup), font=("Helvetica", 14), bg="#007bff", fg="white", width=3).grid(row=3, columnspan=2, padx=(50, 50), pady=50, sticky="nsew")

    def on_part_selected(self, event):
        selected_part = self.item_dropdown.get()
        print("Selected Item", selected_part)
        # Fetch item details from inventory based on selected_part
        self.name_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.purchase_price_entry.delete(0, tk.END)
        self.sale_price_entry.delete(0, tk.END)
 
        part_splited_data = selected_part.split(" - ")
        print("Selected part splited-data", part_splited_data)
        self.name_entry.insert(0, part_splited_data[1])
        self.category_entry.insert(0, part_splited_data[2])
        self.purchase_price_entry.insert(0, part_splited_data[3])
        self.sale_price_entry.insert(0, part_splited_data[4])
    
    def add_purchase_item(self, name, category, quantity, purchase_price, sale_price, popup):
        # Add the item data to the table in the main screen
        self.table.insert("", "end", values=("null", "New", name, category, quantity, purchase_price, sale_price, float(quantity) * float(purchase_price), "Delete"))
        # Call update_grand_total after inserting new item row in items table
        self.update_grand_total()
        popup.destroy()

    def validate_sale_item(self, selected_item, quantity, inventory_items, popup):
        selected_part = None  # Default to None
        # Print the selected item to debug
        print(f"Selected item received in validation from combobox: {selected_item}")
        # Parse selected_item to extract relevant fields (id, name, category)
        selected_id, selected_name, selected_category, selected_purchase_price, selected_sale_price, = selected_item.split(" - ")
        print(f"Parsed selected item -> Id: {selected_id}, Name: {selected_name}, Category: {selected_category}, Purchase-Price: {selected_purchase_price}, Sale-Price: {selected_sale_price} ")
        # Find the selected item data in inventory
        for item in inventory_items:
            item_name = item[1]
            item_category = item[2]
            # Print for debugging
            print(f"Matching selected item against inventory item -> Name: {item_name}, Category: {item_category}")
            if selected_name == item_name and selected_category == item_category:
                selected_part = item
                print(f"Successfully matched with above inventory item !!!")
                break
            print(f"Not matched with above inventory item !!!")
        # If Selected_part is still None
        if selected_part is None:
            messagebox.showerror("Error", "Selected item not matched with existed record in inventory.")
            return
        # Add the valid item data to the table in the main screen
        self.table.insert("", "end", values=(selected_id, "New", selected_name, selected_category, quantity, selected_purchase_price, selected_sale_price, float(quantity)*float(selected_sale_price), "Delete"))
        # Call update_grand_total after inserting new item row in items table
        self.update_grand_total()
        popup.destroy()

    def update_total_prices(self, event=None):
        # Update the total price for all rows in the table
        for row_id in self.table.get_children():
            row = self.table.item(row_id, 'values')
            quantity = float(row[4])
            purchase_price = float(row[5])
            sale_price = float(row[6])
            total_price = quantity * sale_price if self.type_var.get() == "Sale" else quantity * purchase_price
            self.table.item(row_id, values=row[:7] + (total_price, "Delete"))
        # Update the grand total
        self.update_grand_total()

    def update_grand_total(self):
        new_grand_total = sum(float(self.table.item(row, 'values')[7]) for row in self.table.get_children())
        # Update the Grand Total label's text to display new grand total
        self.grand_total_price_value_label.config(text=str(new_grand_total))
        # Also update Balanced Price based on current new grand total and paid price
        new_paid = float(self.paid_price_entry.get())
        new_balance = new_grand_total - new_paid
        # Update the Balance label's text to display new balance
        self.balance_price_value_label.config(text=str(new_balance))

    def update_paid_price(self, event):
        new_grand_total = sum(float(self.table.item(row, 'values')[7]) for row in self.table.get_children())
        # Update the Grand Total label's text to display new grand total
        self.grand_total_price_value_label.config(text=str(new_grand_total))
        # Get Update the Paid Entry Field's value to display new paid
        try:
            new_paid = float(self.paid_price_entry.get())
        except ValueError:
            new_paid = 0  # Default to 0 if the entry is empty or invalid   
        # Get and Update the Balance label's text to display new balance
        new_balance =  new_grand_total - new_paid
        self.balance_price_value_label.config(text=str(new_balance))

    def cancel_transaction(self):
        if messagebox.askokcancel("Cancel", "Are you sure you want to cancel the update ?"):
            from view_transactions_screen import ViewTransactionsScreen
            ViewTransactionsScreen(self.root, self.user)

    def update_transaction(self):
        new_final_grand_total = float(self.grand_total_price_value_label.cget("text"))
        new_final_paid = float(self.paid_price_entry.get())
        new_final_balance = new_final_grand_total - new_final_paid
        # Collect all current items data except the 'Action' column
        items_new_data = [self.table.item(row, 'values')[:8] for row in self.table.get_children()]
        print(f"New Final Items Table Data to be updated:", items_new_data)
        messagebox.showinfo("Success", "All Items Table data saved in an array successfully!")
        # Prepare and display the new final transaction data before sending to backend
        transaction_new_data = {
            "id": self.old_transaction_id,
            "date": self.old_transaction_date,
            "time": self.old_transaction_time,
            "type": self.type_var.get(),
            "user_id": self.old_transaction_user_id,
            "items": items_new_data,
            "grand_total": new_final_grand_total,
            "paid": new_final_paid,
            "balance": new_final_balance
        }
        print(f"New Final Transaction Data sending for updating:", transaction_new_data)
        # calling backend method to save data in database
        update_transaction(transaction_new_data['id'], transaction_new_data['date'], transaction_new_data['time'], transaction_new_data['type'], transaction_new_data['user_id'], transaction_new_data['items'], transaction_new_data['grand_total'], transaction_new_data['paid'], transaction_new_data['balance'])
        # Again displaying "View Transactions"Screen with new updated data
        from view_transactions_screen import ViewTransactionsScreen
        for widget in self.root.winfo_children():
            widget.destroy()
        ViewTransactionsScreen(self.root, self.user)



# Tkinter application setup
if __name__ == "__main__":
    root = tk.Tk()
    # user =   # user-data was already passing from admin dashboard to reporting screen
    app = UpdateTransactionScreen(root, user, transaction_old_data)
    root.mainloop()


