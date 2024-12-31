
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Replace with your MySQL password
            database="retail_db"
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def fetch_query(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

class RetailApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Retail Management System")
        self.root.geometry("800x600")
        self.create_tables()
        self.main_menu()

    def create_tables(self):
        self.db.execute_query("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10,2) NOT NULL
        )
        """)
        self.db.execute_query("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT,
            quantity INT NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            transaction_date DATE NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
        """)

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Retail Management System", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="Manage Products", command=self.manage_products, width=30).pack(pady=10)
        tk.Button(self.root, text="Record Transactions", command=self.record_transaction, width=30).pack(pady=10)
        tk.Button(self.root, text="View Transactions", command=self.view_transactions, width=30).pack(pady=10)

    def manage_products(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Manage Products", font=("Arial", 16)).pack(pady=10)
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="Product Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(form_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Product Price:").grid(row=1, column=0, padx=5, pady=5)
        price_entry = tk.Entry(form_frame)
        price_entry.grid(row=1, column=1, padx=5, pady=5)

        def add_product():
            name = name_entry.get()
            price = price_entry.get()
            if not name or not price:
                messagebox.showwarning("Input Error", "All fields are required!")
                return
            try:
                price = float(price)
                if price <= 0:
                    raise ValueError
                self.db.execute_query("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
                messagebox.showinfo("Success", "Product added successfully!")
                name_entry.delete(0, tk.END)
                price_entry.delete(0, tk.END)
                refresh_products()
            except ValueError:
                messagebox.showwarning("Input Error", "Price must be a positive number!")

        tk.Button(form_frame, text="Add Product", command=add_product).grid(row=2, columnspan=2, pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)
        product_list = ttk.Treeview(self.root, columns=("ID", "Name", "Price"), show="headings")
        product_list.heading("ID", text="ID")
        product_list.heading("Name", text="Name")
        product_list.heading("Price", text="Price")
        product_list.pack(fill=tk.BOTH, expand=True)

        def refresh_products():
            for row in product_list.get_children():
                product_list.delete(row)
            rows = self.db.fetch_query("SELECT * FROM products")
            for row in rows:
                product_list.insert("", tk.END, values=row)

        refresh_products()

    def record_transaction(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Record Transaction", font=("Arial", 16)).pack(pady=10)
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="Select Product:").grid(row=0, column=0, padx=5, pady=5)
        product_dropdown = ttk.Combobox(form_frame, state="readonly")
        product_dropdown.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        quantity_entry = tk.Entry(form_frame)
        quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        def load_products():
            products = self.db.fetch_query("SELECT id, name FROM products")
            product_dropdown["values"] = [f"{p[0]} - {p[1]}" for p in products]

        def save_transaction():
            product_selection = product_dropdown.get()
            quantity = quantity_entry.get()
            if not product_selection or not quantity:
                messagebox.showwarning("Input Error", "All fields are required!")
                return
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    raise ValueError
                product_id = int(product_selection.split(" - ")[0])
                product_price = self.db.fetch_query("SELECT price FROM products WHERE id=%s", (product_id,))[0][0]
                total_price = product_price * quantity
                transaction_date = datetime.now().date()
                self.db.execute_query(
                    "INSERT INTO transactions (product_id, quantity, total_price, transaction_date) VALUES (%s, %s, %s, %s)",
                    (product_id, quantity, total_price, transaction_date)
                )
                messagebox.showinfo("Success", "Transaction recorded successfully!")
                product_dropdown.set("")
                quantity_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showwarning("Input Error", "Quantity must be a positive integer!")

        load_products()
        tk.Button(form_frame, text="Save Transaction", command=save_transaction).grid(row=2, columnspan=2, pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def view_transactions(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="View Transactions", font=("Arial", 16)).pack(pady=10)
        transaction_list = ttk.Treeview(self.root, columns=("ID", "Product", "Quantity", "Total Price", "Date"), show="headings")
        transaction_list.heading("ID", text="ID")
        transaction_list.heading("Product", text="Product")
        transaction_list.heading("Quantity", text="Quantity")
        transaction_list.heading("Total Price", text="Total Price")
        transaction_list.heading("Date", text="Date")
        transaction_list.pack(fill=tk.BOTH, expand=True)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

        def refresh_transactions():
            for row in transaction_list.get_children():
                transaction_list.delete(row)
            rows = self.db.fetch_query("""
            SELECT t.id, p.name, t.quantity, t.total_price, t.transaction_date
            FROM transactions t
            JOIN products p ON t.product_id = p.id
            """)
            for row in rows:
                transaction_list.insert("", tk.END, values=row)

        refresh_transactions()

if __name__ == "__main__":
    root = tk.Tk()
    app = RetailApp(root)
    root.mainloop()
