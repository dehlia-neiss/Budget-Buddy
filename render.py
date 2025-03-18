import tkinter as tk
from tkinter import ttk
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Adeletdehlia21!",
        database="base_budget"
    )

root = tk.Tk()
root.title("Budget Buddy")
root.geometry("900x600")

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

sidebar = tk.Frame(main_frame, bg="#2C3E50", width=200)
sidebar.pack(side="left", fill="y")

logo = tk.Label(sidebar, text="💰", font=("Arial", 24), bg="#2C3E50", fg="white")
logo.pack(pady=20)

buttons = [
    ("Accueil", lambda: show_frame(accueil)),
    ("Transactions", lambda: show_frame(transactions)),
    ("Statistiques", lambda: show_frame(stats)),
    ("authentification",lambda: show_frame(authentification))
]

for text, command in buttons:
    btn = tk.Button(sidebar, text=text, command=command, bg="#34495E", fg="white", font=("Arial", 12), relief="flat")
    btn.pack(fill="x", pady=5, padx=10)

content_frame = tk.Frame(main_frame, bg="white")
content_frame.pack(side="right", fill="both", expand=True)

accueil = tk.Frame(content_frame, bg="white")
transactions = tk.Frame(content_frame, bg="white")
stats = tk.Frame(content_frame, bg="white")

for frame in (accueil, transactions, stats):
    frame.grid(row=0, column=0, sticky="nsew")

tk.Label(accueil, text="Bienvenue sur Budget Buddy", font=("Arial", 16), bg="white").pack(pady=20)

tree = ttk.Treeview(transactions, columns=("ID", "Montant", "Type", "Date"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Montant", text="Montant")
tree.heading("Type", text="Type")
tree.heading("Date", text="Date")
tree.pack(fill="both", expand=True, padx=20, pady=20)

def fetch_transactions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT t.id, t.montant, t.type, t.date FROM transaction t JOIN client c ON t.client_id = c.id JOIN categories ca ON t.categorie_id = ca.id")
    rows = cursor.fetchall()
    conn.close()

    for item in tree.get_children():
        tree.delete(item)

    for row in rows:
        tree.insert("", "end", values=row)

btn_refresh = tk.Button(transactions, text="Actualiser", command=fetch_transactions, bg="#27AE60", fg="white")
btn_refresh.pack(pady=10)

def show_frame(frame):
    frame.tkraise()

show_frame(accueil)

root.mainloop()
