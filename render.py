import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from datetime import datetime
from auth import login as auth_login   # Import login function from auth.py
from connexion import connect_db      # Import shared database connection

# Global variables
client_id = None
tree_transactions = None

def login_handler():
    global client_id
    email = entry_email.get()
    password = entry_password.get()
    user_id = auth_login(email, password)
    if user_id:
        client_id = user_id
        messagebox.showinfo("Login Successful", "You are now logged in!")
        show_buttons_after_login()
        login_frame.pack_forget()
        transaction_frame.pack(fill="both", expand=True)
    else:
        messagebox.showerror("Error", "Incorrect email or password.")

def show_buttons_after_login():
    transactions_btn.pack(fill="x", pady=5, padx=10)
    history_btn.pack(fill="x", pady=5, padx=10)

def fetch_transactions():
    global tree_transactions
    if client_id is None:
        messagebox.showerror("Error", "You must be logged in to view transactions.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT t.id, t.montant, t.type, t.date FROM transaction t WHERE t.client_id = %s", (client_id,))
    rows = cursor.fetchall()
    conn.close()

    for item in tree_transactions.get_children():
        tree_transactions.delete(item)

    for row in rows:
        tree_transactions.insert("", "end", values=row)

def add_transaction(amount, transaction_type, category):
    if client_id is None:
        messagebox.showerror("Error", "You must be logged in to add a transaction.")
        return

    if not amount or not transaction_type or not category:
        messagebox.showerror("Error", "All fields must be filled.")
        return

    try:
        amount = float(amount)
        transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = connect_db()
        cursor = conn.cursor()

        # Check if the category exists; if not, add it
        cursor.execute("SELECT id FROM categories WHERE nom = %s", (category,))
        result = cursor.fetchone()
        if result:
            category_id = result[0]
        else:
            cursor.execute("INSERT INTO categories (nom) VALUES (%s)", (category,))
            conn.commit()
            category_id = cursor.lastrowid

        # Insert the transaction with the current date
        cursor.execute(
            "INSERT INTO transaction (montant, type, client_id, categorie_id, date) VALUES (%s, %s, %s, %s, %s)",
            (amount, transaction_type, client_id, category_id, transaction_date)
        )
        conn.commit()
        conn.close()
        fetch_transactions()
        messagebox.showinfo("Success", "Transaction added successfully!")
    except ValueError:
        messagebox.showerror("Error", "The amount must be a valid number.")

# --- UI Setup ---

root = tk.Tk()
root.title("Budget Buddy")
root.geometry("900x600")

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

sidebar = tk.Frame(main_frame, bg="#2C3E50", width=200)
sidebar.pack(side="left", fill="y")

logo_image = PhotoImage(file="logo_budget_buddy.png")
logo_image = logo_image.subsample(6, 6)
logo = tk.Label(sidebar, image=logo_image, bg="#2C3E50")
logo.pack(pady=20)

login_frame = tk.Frame(main_frame)
login_frame.pack(fill="both", expand=True)

tk.Label(login_frame, text="Email", font=("Arial", 12)).pack(pady=5)
entry_email = tk.Entry(login_frame)
entry_email.pack(pady=5)

tk.Label(login_frame, text="Password", font=("Arial", 12)).pack(pady=5)
entry_password = tk.Entry(login_frame, show="*")
entry_password.pack(pady=5)

login_btn = tk.Button(login_frame, text="Login", bg="#27AE60", fg="white", command=login_handler)
login_btn.pack(pady=20)

transactions_btn = tk.Button(sidebar, text="Transactions", bg="#34495E", fg="white", font=("Arial", 12), relief="flat", command=fetch_transactions)
history_btn = tk.Button(sidebar, text="History", bg="#34495E", fg="white", font=("Arial", 12), relief="flat", command=fetch_transactions)

tree_transactions = ttk.Treeview(main_frame, columns=("ID", "Amount", "Type", "Date"))
transaction_frame = tk.Frame(main_frame)
transaction_frame.pack(fill="both", expand=True, pady=10)

tk.Label(transaction_frame, text="Amount:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
entry_amount = tk.Entry(transaction_frame)
entry_amount.grid(row=0, column=1, padx=10, pady=5)

tk.Label(transaction_frame, text="Type:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
transaction_type_var = tk.StringVar()
type_dropdown = ttk.Combobox(transaction_frame, textvariable=transaction_type_var, values=["Deposit", "Withdrawal"])
type_dropdown.grid(row=1, column=1, padx=10, pady=5)

tk.Label(transaction_frame, text="Category:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
entry_category = tk.Entry(transaction_frame)
entry_category.grid(row=2, column=1, padx=10, pady=5)

add_btn = tk.Button(transaction_frame, text="Add Transaction", bg="#27AE60", fg="white",
                    command=lambda: add_transaction(entry_amount.get(), transaction_type_var.get(), entry_category.get()))
add_btn.grid(row=3, column=0, columnspan=2, pady=10)

tree_transactions.heading("#1", text="ID")
tree_transactions.heading("#2", text="Amount")
tree_transactions.heading("#3", text="Type")
tree_transactions.heading("#4", text="Date")
tree_transactions.pack(fill="both", expand=True)

root.mainloop()
