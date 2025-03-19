import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from tkinter import PhotoImage
from datetime import datetime

# Global variables
client_id = None
tree_transactions = None

# Connect to the database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Adeletdehlia21!",
        database="base_budget"
    )

# Fetch client details by email and password
def login(email, password):
    global client_id
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM client WHERE email = %s AND mot_de_passe = %s", (email, password))
    result = cursor.fetchone()
    conn.close()
    if result:
        client_id = result[0]
        messagebox.showinfo("Connexion réussie", "Vous êtes connecté !")
        show_buttons_after_login()
        return True
    else:
        messagebox.showerror("Erreur", "Email ou mot de passe incorrect.")
        return False

# Show buttons after login
def show_buttons_after_login():
    transactions_btn.pack(fill="x", pady=5, padx=10)
    historique_btn.pack(fill="x", pady=5, padx=10)

# Show transactions history
def fetch_transactions():
    global tree_transactions
    if client_id is None:
        messagebox.showerror("Erreur", "Vous devez être connecté pour voir les transactions.")
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

def add_transaction(montant, type_transaction, categorie):
    if client_id is None:
        messagebox.showerror("Erreur", "Vous devez être connecté pour ajouter une transaction.")
        return

    if not montant or not categorie or not type_transaction:
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return

    try:
        montant = float(montant)
        date_transaction = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = connect_db()
        cursor = conn.cursor()

        # Vérifier si la catégorie existe, sinon l'ajouter
        cursor.execute("SELECT id FROM categories WHERE nom = %s", (categorie,))
        result = cursor.fetchone()

        if result:
            categorie_id = result[0]
        else:
            cursor.execute("INSERT INTO categories (nom) VALUES (%s)", (categorie,))
            conn.commit()
            categorie_id = cursor.lastrowid

        # Insérer la transaction avec la date actuelle
        cursor.execute("INSERT INTO transaction (montant, type, client_id, categorie_id, date) VALUES (%s, %s, %s, %s, %s)",
                       (montant, type_transaction, client_id, categorie_id, date_transaction))
        conn.commit()
        conn.close()

        fetch_transactions()
        messagebox.showinfo("Succès", "Transaction ajoutée avec succès !")

    except ValueError:
        messagebox.showerror("Erreur", "Le montant doit être un nombre valide.")

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

tk.Label(login_frame, text="Email", font=("Arial", 12), bg="white").pack(pady=5)
entry_email = tk.Entry(login_frame)
entry_email.pack(pady=5)

tk.Label(login_frame, text="Mot de passe", font=("Arial", 12), bg="white").pack(pady=5)
entry_password = tk.Entry(login_frame, show="*")
entry_password.pack(pady=5)

def handle_login():
    email = entry_email.get()
    password = entry_password.get()
    if login(email, password):
     login_frame.pack_forget()  
    transaction_frame.pack(fill="both", expand=True) 


login_btn = tk.Button(login_frame, text="Se connecter", bg="#27AE60", fg="white", command=handle_login)
login_btn.pack(pady=20)

transactions_btn = tk.Button(sidebar, text="Transactions", bg="#34495E", fg="white", font=("Arial", 12), relief="flat", command=lambda: fetch_transactions())
historique_btn = tk.Button(sidebar, text="Historique", bg="#34495E", fg="white", font=("Arial", 12), relief="flat", command=lambda: fetch_transactions())

tree_transactions = ttk.Treeview(main_frame, columns=("ID", "Montant", "Type", "Date"))
transaction_frame = tk.Frame(main_frame)
transaction_frame.pack(fill="both", expand=True, pady=10)

tk.Label(transaction_frame, text="Montant:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
entry_montant = tk.Entry(transaction_frame)
entry_montant.grid(row=0, column=1, padx=10, pady=5)

tk.Label(transaction_frame, text="Type:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
type_var = tk.StringVar()
type_dropdown = ttk.Combobox(transaction_frame, textvariable=type_var, values=["Dépôt", "Retrait"])
type_dropdown.grid(row=1, column=1, padx=10, pady=5)

tk.Label(transaction_frame, text="Catégorie:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
entry_categorie = tk.Entry(transaction_frame)
entry_categorie.grid(row=2, column=1, padx=10, pady=5)

add_btn = tk.Button(transaction_frame, text="Ajouter Transaction", bg="#27AE60", fg="white",
                    command=lambda: add_transaction(entry_montant.get(), type_var.get(), entry_categorie.get()))
add_btn.grid(row=3, column=0, columnspan=2, pady=10)

tree_transactions.heading("#1", text="ID")
tree_transactions.heading("#2", text="Montant")
tree_transactions.heading("#3", text="Type")
tree_transactions.heading("#4", text="Date")
tree_transactions.pack(fill="both", expand=True)

root.mainloop()
