



# Record Purchase Transaction Screen




import tkinter as tk
from tkinter import messagebox, ttk
from inventory import fetch_parts, add_purchased_items_sqlite, add_purchased_items_mysql
from transactions import record_transaction_sqlite, record_transaction_mysql
from utils import validate_input


class PurchaseTransactionScreen:
    def __init__(self, root, user):
        self.root = root
        self.root.title("MSPMS - Purchase Transaction Screen")
        self.root.geometry("820x620")
        self.root.minsize(820,620)
        self.root.maxsize(820,620)
        self.root.config(bg="skyblue")
        self.user = user
        self.purchase_parts = []  # List to store purchased parts
        self.create_widgets()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_widgets(self):

        # Dashboard Title
        tk.Label(self.root, text="Record Purchase Transaction", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue").grid(row=0, column=0, columnspan=4, padx=15, pady=(20,5), sticky="nsew")

        # Form Frame
        form_frame = tk.Frame(self.root, bg="skyblue")
        form_frame.grid(row=3, column=0, columnspan=4, pady=(10,5), padx=20, sticky="nsew")

        # Dropdown to select spare part from inventory
        tk.Label(form_frame, text="Select Item:", font=("Helvetica", 12, "bold"), bg="skyblue").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        parts = fetch_parts()
        combobox_values = [f"{part[0]} : {part[1]} : {part[2]} : {part[3]} : {part[4]}" for part in parts]
        self.part_dropdown = ttk.Combobox(form_frame, font=("Helvetica", 10), width=30, values=combobox_values) 
        self.part_dropdown.grid(row=0, column=1, pady=7, padx=10)
        self.part_dropdown.bind("<<ComboboxSelected>>", self.on_part_selected)
        # "OR" text in center
        tk.Label(form_frame, text="OR (manually below fields)", font=("Helvetica", 14, "bold"), fg="red", bg="skyblue").grid(row=0, column=2, columnspan=2, pady=10, padx=10, sticky="w")
        # Entry for Name
        tk.Label(form_frame, text="Name:", font=("Helvetica", 12, "bold"), bg="skyblue").grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.name_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=25)
        self.name_entry.grid(row=1, column=1, pady=7, padx=10)
        # Entry for Category
        tk.Label(form_frame, text="Category:", font=("Helvetica", 12, "bold"), bg="skyblue").grid(row=1, column=2, pady=10, padx=10, sticky="w")
        self.category_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=25)
        self.category_entry.grid(row=1, column=3, pady=7, padx=10)
        # Entry for Quantity
        tk.Label(form_frame, text="Quantity:", font=("Helvetica", 12, "bold"), bg="skyblue").grid(row=2, column=0, pady=10, padx=10, sticky="w")
        self.quantity_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=25)
        self.quantity_entry.grid(row=2, column=1, pady=7, padx=10)
        # Entry for Purchase Price
        tk.Label(form_frame, text="Purchase Price:", font=("Helvetica", 12, "bold"), bg="skyblue").grid(row=2, column=2, pady=10, padx=10, sticky="w")
        self.purchase_price_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=25)
        self.purchase_price_entry.grid(row=2, column=3, pady=7, padx=10)
        # Entry for Sale Price
        tk.Label(form_frame, text="Sale Price:", font=("Helvetica", 12, "bold"), bg="skyblue").grid(row=3, column=0, pady=10, padx=10, sticky="w")
        self.sale_price_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=25)
        self.sale_price_entry.grid(row=3, column=1, pady=7, padx=10)
        # Add Part Button
        tk.Button(form_frame, text="Add Part", font=("Helvetica", 12), width=25, fg="white", bg="blue", command=self.add_purchase_part).grid(row=3, column=3, pady=7, padx=12)

        # TreeView Table
        # Table Style
        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white", font=("Helvetica", 12))
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background="blue", foreground="black")
        style.map('Treeview', background=[('selected', '#007bff')])
        #Table Frame
        self.table_frame = tk.Frame(self.root, bg="skyblue")
        self.table_frame.grid(row=4, column=0, columnspan=4, pady=(5,5), padx=(30,30), sticky="nsew")
        # Table Column Headings
        self.selected_part_list = ttk.Treeview(self.table_frame, columns=("Name", "Category", "Quantity", "Purchase Price", "Sale Price", "Total Price", "Action"), show='headings')
        self.selected_part_list.heading("Name", text="Name")
        self.selected_part_list.heading("Category", text="Category")
        self.selected_part_list.heading("Quantity", text="Quantity")
        self.selected_part_list.heading("Purchase Price", text="Purchase Price")
        self.selected_part_list.heading("Sale Price", text="Sale Price")
        self.selected_part_list.heading("Total Price", text="Total Price")
        self.selected_part_list.heading("Action", text="Action")
        # Table Columns Config
        for col in self.selected_part_list["columns"]:
            self.selected_part_list.column(col, width=100, minwidth=70, stretch=tk.NO)
        # Table Location Config
        self.selected_part_list.grid(row=0, column=0, sticky='nsew')
        # Scrollbars for the table
        v_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.selected_part_list.yview)
        h_scrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.selected_part_list.xview)
        self.selected_part_list.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        # Table Config
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        # Grand Total Label and Field(read-only)
        grand_total_frame = tk.Frame(self.root, bg="skyblue")
        grand_total_frame.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')
        grand_total_frame.grid_columnconfigure(0, weight=1)
        grand_total_frame.grid_columnconfigure(1, weight=0)
        grand_total_frame.grid_columnconfigure(2, weight=0)
        grand_total_frame.grid_columnconfigure(3, weight=1)
        tk.Label(grand_total_frame, text="Grand Total Price:", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue").grid(row=0, column=1, padx=(5,1), pady=1, sticky='e')
        self.grand_total_price_value_label = tk.Label(grand_total_frame, text="0.00", font=("Helvetica", 12), width=15, anchor="w", relief="sunken")
        self.grand_total_price_value_label.grid(row=0, column=2, padx=(5,1), pady=1, sticky='w')

        # Buttons outer frame
        buttons_frame_outer = tk.Frame(self.root, bg="skyblue")
        buttons_frame_outer.grid(row=6, column=0, columnspan=4, pady=(5,20), padx=20, sticky="nsew")
        # Buttons inner frame to hold the buttons
        buttons_frame_inner = tk.Frame(buttons_frame_outer, bg="skyblue")
        buttons_frame_inner.pack(pady=5)
        # Buttons
        tk.Button(buttons_frame_inner, text="Back", command=self.back_to_dashboard_button, font=("Helvetica", 14), bg="#2ECC71", fg="black", width=20).grid(row=0, column=1, padx=(10,25))
        tk.Button(buttons_frame_inner, text="Record Transaction", command=self.handle_record_purchase, font=("Helvetica", 14), bg="#007bff", fg="white", width=20).grid(row=0, column=2, padx=(25,10))

    def back_to_dashboard_button(self):
        self.clear_frame()
        from record_transaction_screen import RecordTransactionScreen
        RecordTransactionScreen(self.root, self.user)

    def on_part_selected(self, event):
        selected_part = self.part_dropdown.get()
        print("Selected Part", selected_part)
        # Fetch item details from inventory based on selected_part
        self.name_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.purchase_price_entry.delete(0, tk.END)
        self.sale_price_entry.delete(0, tk.END)
 
        part_splited_data = selected_part.split(" : ")
        print("Selected part splited-data", part_splited_data)
        self.name_entry.insert(0, part_splited_data[1])
        self.category_entry.insert(0, part_splited_data[2])
        self.purchase_price_entry.insert(0, part_splited_data[3])
        self.sale_price_entry.insert(0, part_splited_data[4])

    def add_purchase_part(self):
        name = self.name_entry.get()
        category = self.category_entry.get()
        quantity = self.quantity_entry.get()
        purchase_price = self.purchase_price_entry.get()
        sale_price = self.sale_price_entry.get()
        # Validations
        if not validate_input(name, category, quantity, purchase_price, sale_price):
            messagebox.showerror("Error", "All fields are required")
            return
        if not quantity.isdigit():
            messagebox.showerror("Error", "Quantity must be an integer")
            return
        if not purchase_price.replace('.', '', 1).isdigit() or not sale_price.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Price must be a number either int or float")
            return
        # Pre-Process data and display in Table
        quantity = int(quantity)
        purchase_price = float(purchase_price)
        sale_price = float(sale_price)
        total_price = quantity * purchase_price
        self.purchase_parts.append((name, category, quantity, purchase_price, sale_price, total_price))
        # Insert Data to table with delete button as "Action" Column value
        part_data = (name, category, quantity, purchase_price, sale_price, total_price)
        self.selected_part_list.insert('', 'end', values=(*part_data, "Delete"))
        # Bind event for editing "Quantity" column
        self.selected_part_list.bind("<Double-1>", self.on_double_click)
        # Bind event for "Delete" action
        self.selected_part_list.bind("<ButtonRelease-1>", self.on_item_click)
        # Calculate updated New Grand Total Price 
        self.update_grand_total_price()
        messagebox.showinfo("Success", f"{name} successfully added to purchase list")
        # Reset form fields to empty for next entry
        self.part_dropdown.set('')
        self.name_entry.delete('', tk.END)
        self.category_entry.delete('', tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.purchase_price_entry.delete(0, tk.END)
        self.sale_price_entry.delete(0, tk.END)

    # Edit Quantity
    def on_double_click(self, event):
        item = self.selected_part_list.selection()[0]  # Get selected row
        col = self.selected_part_list.identify_column(event.x)  # Get the column clicked
        if col == "#3":  # If "Quantity" column (# means column number not index number) is clicked
            self.edit_quantity(item)
    def edit_quantity(self, item):
        # Get the bounding box of the selected row and column for Quantity
        row_bbox = self.selected_part_list.bbox(item, column=2)  # Column index no for "Quantity"
        # Create an Entry widget
        entry = tk.Entry(self.table_frame)
        entry.place(x=row_bbox[0], y=row_bbox[1], width=row_bbox[2], height=row_bbox[3])
        # Re-fill the current quantity(index number) value
        current_quantity = self.selected_part_list.item(item, 'values')[2]
        entry.insert(0, current_quantity)
        # Bind the return key (Enter) to update the table and remove the entry widget
        entry.bind("<Return>", lambda e: self.save_quantity(item, entry))
    def save_quantity(self, item, entry):
        # Get the new quantity entered by the user
        new_quantity = entry.get()
        # Update the quantity value in the table
        values = list(self.selected_part_list.item(item, 'values'))
        values[2] = new_quantity  # Update "Quantity" field
        self.selected_part_list.item(item, values=values)
        # Remove the Entry widget
        entry.destroy()
        # Call the update_total_prices function to recalculate the total price
        self.update_item_total__price()  # No event argument required here


    # Delete Item
    def on_item_click(self, event):
        selected_item = self.selected_part_list.selection()  # Get selected item
        cur_item = self.selected_part_list.item(selected_item)  # Get the item data
        col = self.selected_part_list.identify_column(event.x)  # Identify clicked column
        # Check if "Action" column (# means column no not index number) was clicked
        if col == '#7':  
            index = self.selected_part_list.index(selected_item)  # Get the index of the selected item
            self.delete_item(index)  # Call delete function    
    def delete_item(self, index):
        selected_item = self.selected_part_list.get_children()[index]  # Get the item by its index
        self.selected_part_list.delete(selected_item)  # Delete the selected item row from the table
        # Call update_grand_total after inserting new item row in items table
        self.update_grand_total_price()


    def update_item_total__price(self, event=None):
        # Update the total price for all rows in the table after quantity is edited
        for row_id in self.selected_part_list.get_children():
            row = self.selected_part_list.item(row_id, 'values')
            quantity = float(row[2])
            purchase_price = float(row[3])
            sale_price = float(row[4])
            total_price = quantity * purchase_price
            self.selected_part_list.item(row_id, values=row[:5] + (total_price, "Delete"))
        # Update Grand Total Price After inserting edited quantity row again in table with new quantity
        self.update_grand_total_price()


    def update_grand_total_price(self):
        new_grand_total = sum(float(self.selected_part_list.item(row, 'values')[5]) for row in self.selected_part_list.get_children())
        # Update the Grand Total label's text to display new grand total
        self.grand_total_price_value_label.config(text=str(new_grand_total))


    def show_checkout_form(self, grand_total):
        """Pop-up form to input paid and balance prices."""
        def calculate_balance(event=None):
            try:
                # If the paid_entry is empty, set paid_amount to 0.00
                paid_amount = float(paid_entry.get()) if paid_entry.get() else 0.00
                balance_amount = grand_total - paid_amount
                balance_var.set(f"{balance_amount:.2f}")  # Set balance to 2 decimal points
            except ValueError:
                balance_var.set("Invalid Input")
        def confirm_transaction():
            try:
                # First, get the paid and balance values before destroying the form
                paid_amount = float(paid_entry.get()) if paid_entry.get() else 0.00  # Default to 0.00 if empty
                balance_amount = float(balance_var.get())
                # Close the form after fetching the values
                self.paid_price = paid_amount
                self.balance_price = balance_amount
                # Now destroy the form
                form.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter the Paid price in digits.")
                return  # Removed return None, None since we always have a valid number
        # Create a pop-up form window using Toplevel
        form = tk.Toplevel()
        form.title("MSPMS - Checkout")
        form.geometry("395x320")
        form.minsize(395, 320)
        form.maxsize(395, 320)
        form.config(bg="skyblue")
        # Pop-Up Screen Title
        title = tk.Label(form, text="Checkout", font=("Helvetica", 24, "bold"), fg="black", bg="skyblue")
        title.grid(row=0, column=0, columnspan=2, padx=(45,45), pady=(20,40), sticky="nsew")
        # Grand Total Field (read-only)
        grand_total_label = tk.Label(form, text=f"Grand Total Price :", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue")
        grand_total_label.grid(row=1, column=0, padx=(20,10), pady=5, sticky='w')  # Left align
        grand_total_var =  tk.StringVar(value=f"{grand_total:.2f}")
        grand_total_entry = tk.Entry(form, textvariable=grand_total_var, state="readonly", font=("Helvetica", 12))
        grand_total_entry.grid(row=1, column=1, padx=(10,20), pady=5, sticky='e')  # Right align
        # Paid Price Field
        paid_label = tk.Label(form, text="Paid Price :", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue")
        paid_label.grid(row=2, column=0, padx=(20,10), pady=5, sticky='w')  # Left align
        paid_entry = tk.Entry(form, font=("Helvetica", 12))
        paid_entry.grid(row=2, column=1, padx=(10,20), pady=5, sticky='e')  # Right align
        paid_entry.bind("<KeyRelease>", calculate_balance)
        # Balance Price Field (read-only)        
        balance_label = tk.Label(form, text="Balance Price :", font=("Helvetica", 12, "bold"), fg="black", bg="skyblue")
        balance_label.grid(row=3, column=0, padx=(20,10), pady=5, sticky='w')  # Left align
        balance_var = tk.StringVar()
        balance_entry = tk.Entry(form, textvariable=balance_var, state="readonly", font=("Helvetica", 12))
        balance_entry.grid(row=3, column=1, padx=(10,20), pady=5, sticky='e')  # Right align
        # Confirm Button (Center Align)
        confirm_button = tk.Button(form, text="Confirm Transaction", command=confirm_transaction, font=("Helvetica", 12, "bold"), fg='white', bg='green', width=20)
        confirm_button.grid(row=4, column=0, columnspan=2, pady=(40,20))  # Center align by using columnspan
        # Wait until the form is closed
        form.wait_window()  
        # Return the values after the form is closed
        print(f"Returning final Paid = {self.paid_price} and Balance = {self.balance_price}")
        return self.paid_price, self.balance_price


    def handle_record_purchase(self):
        # Before recording the transaction, check if there are any items in the table
        if not self.selected_part_list.get_children():  # Check if there are no rows
            messagebox.showerror("Error", "No parts added for purchase")
            return 
        # Calculating Grand Total of all items by summing up their Total Prices (Column No 6 Index No 5)
        final_grand_total_price = sum(float(self.selected_part_list.item(row, 'values')[5]) for row in self.selected_part_list.get_children())

        # Show Checkout pop-up form to get Paid and Balance prices
        self.paid_price, self.balance_price = self.show_checkout_form(final_grand_total_price)
        print(f"Received Paid={self.paid_price} & Balance={self.balance_price}")

        try:
            print("Now first adding Purchased Items into spare_parts Table")
            print("In SQLite:")
            stored_purchased_items_sqlite = add_purchased_items_sqlite(self.purchase_parts)
            print("In MySQL:")
            stored_purchased_items_mysql = add_purchased_items_mysql(self.purchase_parts)
            print("And now adding stored_purchased_items into transactions and transaction_items Tables")
            print("In SQLite:")
            record_transaction_sqlite(stored_purchased_items_sqlite, self.user['id'], 'Purchase', final_grand_total_price, self.paid_price, self.balance_price)
            print("In MySQL:")
            record_transaction_mysql(stored_purchased_items_mysql, self.user['id'], 'Purchase', final_grand_total_price, self.paid_price, self.balance_price)
            messagebox.showinfo("Success", "Purchase transaction recorded successfully")
            self.create_widgets()
        except Exception as e:
            messagebox.showerror("Error", "This is exception run")
            messagebox.showerror("Error", f"Failed to record purchase transaction: {e}")



if __name__ == "__main__":
    root = tk.Tk()
    # user =   # user-data is already passing from dashboards
    app = PurchaseTransactionScreen(root, user)
    root.mainloop()




