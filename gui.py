import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Budget Buddy")
        self.geometry("400x400")
        self.configure(bg="#f0f0f0")
        
        self.create_home_screen()

    def create_home_screen(self):
        self.clear_screen()

        label = tk.Label(self, text="Choisissez votre rôle", font=("Arial", 18), bg="#f0f0f0")
        label.pack(pady=20)

        client_button = tk.Button(self, text="Client", font=("Arial", 14), command=self.client_login)
        client_button.pack(pady=10)

        banquier_button = tk.Button(self, text="Banquier", font=("Arial", 14), command=self.banquier_login)
        banquier_button.pack(pady=10)

    def client_login(self):
        self.clear_screen()

        label = tk.Label(self, text="Connexion Client", font=("Arial", 18), bg="#f0f0f0")
        label.pack(pady=20)

        email_label = tk.Label(self, text="E-mail", font=("Arial", 12), bg="#f0f0f0")
        email_label.pack(pady=5)
        self.email_entry = tk.Entry(self, font=("Arial", 12))
        self.email_entry.pack(pady=5)

        password_label = tk.Label(self, text="Mot de passe", font=("Arial", 12), bg="#f0f0f0")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self, text="Se connecter", font=("Arial", 14), command=self.authenticate_client)
        login_button.pack(pady=20)

        register_button = tk.Button(self, text="Créer un compte", font=("Arial", 12), command=self.create_client_account)
        register_button.pack(pady=10)

    def banquier_login(self):
        self.clear_screen()

        label = tk.Label(self, text="Connexion Banquier", font=("Arial", 18), bg="#f0f0f0")
        label.pack(pady=20)

        email_label = tk.Label(self, text="E-mail", font=("Arial", 12), bg="#f0f0f0")
        email_label.pack(pady=5)
        self.email_entry = tk.Entry(self, font=("Arial", 12))
        self.email_entry.pack(pady=5)

        password_label = tk.Label(self, text="Mot de passe", font=("Arial", 12), bg="#f0f0f0")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self, text="Se connecter", font=("Arial", 14), command=self.authenticate_banquier)
        login_button.pack(pady=20)

    def authenticate_client(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        self.current_user_email = email
        self.current_user_role = "Client"

        if self.check_credentials("client", email, password):
            self.open_dashboard("Client", email)
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects ou utilisateur non trouvé")

    def authenticate_banquier(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        self.current_user_email = email
        self.current_user_role = "Banquier"

        if self.check_credentials("banquier", email, password):
            self.open_dashboard("Banquier", email)
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects ou utilisateur non trouvé")

    def check_credentials(self, role, email, password):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Adeletdehlia21!",
                database="base_budget"
            )

            cursor = connection.cursor()
            if role == "client":
                query = "SELECT * FROM client WHERE email = %s AND mot_de_passe = %s"
            else:
                query = "SELECT * FROM banquier WHERE mail = %s AND mot_de_passe = %s"

            cursor.execute(query, (email, password))
            result = cursor.fetchone()

            if result:
                return True
            else:
                return False
        except Error as e:
            messagebox.showerror("Erreur de connexion", f"Erreur de connexion à la base de données: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def open_dashboard(self, role, email):
        self.clear_screen()

        dashboard_label = tk.Label(self, text=f"Tableau de bord {role}", font=("Arial", 18), bg="#f0f0f0")
        dashboard_label.pack(pady=20)

        welcome_label = tk.Label(self, text=f"Bienvenue {role}!", font=("Arial", 14), bg="#f0f0f0")
        welcome_label.pack(pady=20)

        balance_label = tk.Label(self, text="Solde : ", font=("Arial", 14), bg="#f0f0f0")
        balance_label.pack(pady=10)

        balance = self.get_balance(role, email)
        balance_value_label = tk.Label(self, text=f"{balance} €", font=("Arial", 14), bg="#f0f0f0")
        balance_value_label.pack(pady=5)

        transaction_button = tk.Button(self, text="Nouvelle transaction", font=("Arial", 14), command=self.create_transaction)
        transaction_button.pack(pady=10)

        logout_button = tk.Button(self, text="Se déconnecter", font=("Arial", 14), command=self.logout)
        logout_button.pack(pady=10)

    def get_balance(self, role, email):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Adeletdehlia21!",
                database="base_budget"
            )

            cursor = connection.cursor()

            if role == "client":
                query = "SELECT solde FROM client WHERE email = %s"
            else:
                query = "SELECT solde FROM banquier WHERE mail = %s"

            cursor.execute(query, (email,))
            result = cursor.fetchone()

            if result:
                return result[0]
            else:
                return 0

        except Error as e:
            messagebox.showerror("Erreur de connexion", f"Erreur de connexion à la base de données: {e}")
            return 0
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def update_balance(self, email, amount, operation):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Adeletdehlia21!",
                database="base_budget"
            )
            cursor = connection.cursor()

            if operation == "add":
                query = "UPDATE client SET solde = solde + %s WHERE email = %s"
            elif operation == "subtract":
                query = "UPDATE client SET solde = solde - %s WHERE email = %s"

            cursor.execute(query, (amount, email))
            connection.commit()
        except Error as e:
            messagebox.showerror("Erreur", f"Problème lors de la mise à jour du solde: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def handle_transaction(self, email, transaction_type, amount, receiver_email=None):
        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Erreur", "Le montant doit être supérieur à 0.")
                return
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")
            return

        if transaction_type == "Dépôt":
            self.update_balance(email, amount, "add")
            messagebox.showinfo("Succès", "Dépôt effectué avec succès.")

        elif transaction_type == "Retrait":
            current_balance = self.get_balance(email)
            if current_balance >= amount:
                self.update_balance(email, amount, "subtract")
                messagebox.showinfo("Succès", "Retrait effectué avec succès.")
            else:
                messagebox.showerror("Erreur", "Solde insuffisant.")

        elif transaction_type == "Transfert":
            if not receiver_email:
                messagebox.showerror("Erreur", "Veuillez entrer un destinataire.")
                return
            if receiver_email == email:
                messagebox.showerror("Erreur", "Vous ne pouvez pas vous transférer de l'argent.")
                return

            current_balance = self.get_balance(email)
            if current_balance >= amount:
                self.update_balance(email, amount, "subtract")
                self.update_balance(receiver_email, amount, "add")
                messagebox.showinfo("Succès", "Transfert effectué avec succès.")
            else:
                messagebox.showerror("Erreur", "Solde insuffisant.")

        self.open_dashboard("Client", email)

    def create_transaction(self):
        self.clear_screen()

        label = tk.Label(self, text="Nouvelle transaction", font=("Arial", 18), bg="#f0f0f0")
        label.pack(pady=20)

        type_label = tk.Label(self, text="Type de transaction (Dépôt, Retrait, etc.)", font=("Arial", 12), bg="#f0f0f0")
        type_label.pack(pady=5)
        self.transaction_type_entry = tk.Entry(self, font=("Arial", 12))
        self.transaction_type_entry.pack(pady=5)

        amount_label = tk.Label(self, text="Montant", font=("Arial", 12), bg="#f0f0f0")
        amount_label.pack(pady=5)
        self.amount_entry = tk.Entry(self, font=("Arial", 12))
        self.amount_entry.pack(pady=5)

        save_button = tk.Button(self, text="Enregistrer la transaction", font=("Arial", 14), command=self.save_transaction)
        save_button.pack(pady=20)

    def save_transaction(self):
        transaction_type = self.transaction_type_entry.get()
        amount = self.amount_entry.get()

        if not transaction_type or not amount:
            messagebox.showerror("Erreur", "Tous les champs sont requis")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Adeletdehlia21!",
                database="base_budget"
            )

            cursor = connection.cursor()

            amount = float(amount)

            query = "INSERT INTO transaction (`type`, montant) VALUES (%s, %s)"
            cursor.execute(query, (transaction_type, amount))

            connection.commit()
            messagebox.showinfo("Succès", "Transaction enregistrée avec succès")

            self.open_dashboard(self.current_user_role, self.current_user_email)

        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création de la transaction: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def create_client_account(self):
        self.clear_screen()

        label = tk.Label(self, text="Créer un compte Client", font=("Arial", 18), bg="#f0f0f0")
        label.pack(pady=20)

        email_label = tk.Label(self, text="E-mail", font=("Arial", 12), bg="#f0f0f0")
        email_label.pack(pady=5)
        self.new_email_entry = tk.Entry(self, font=("Arial", 12))
        self.new_email_entry.pack(pady=5)

        password_label = tk.Label(self, text="Mot de passe", font=("Arial", 12), bg="#f0f0f0")
        password_label.pack(pady=5)
        self.new_password_entry = tk.Entry(self, font=("Arial", 12), show="*")
        self.new_password_entry.pack(pady=5)

        create_button = tk.Button(self, text="Créer un compte", font=("Arial", 14), command=self.save_new_client)
        create_button.pack(pady=20)

    def save_new_client(self):
        email = self.new_email_entry.get()
        password = self.new_password_entry.get()

        if not email or not password:
            messagebox.showerror("Erreur", "Tous les champs sont requis")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Adeletdehlia21!",
                database="base_budget"
            )

            cursor = connection.cursor()

            query = "INSERT INTO client (email, mot_de_passe) VALUES (%s, %s)"
            cursor.execute(query, (email, password))

            connection.commit()
            messagebox.showinfo("Succès", "Compte client créé avec succès")

            self.create_home_screen()

        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création du compte: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def logout(self):
        self.create_home_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
