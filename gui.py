import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Budget Buddy")
        self.geometry("400x500")
        self.configure(bg="#f0f0f0")

        self.is_logged_in = False
        
        self.main_frame = tk.Frame(self, bg="#f0f0f0")
        self.main_frame.pack(fill="both", expand=True)
        self.current_user_email = ""
        self.current_user_role = ""
        self.create_home_screen()

    def clear_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def create_home_screen(self):
        self.clear_screen()

        label = tk.Label(self.main_frame, text="Choisissez votre rôle", font=("Arial", 18), bg="#f0f0f0")
        label.pack(pady=40)

        client_button = tk.Button(self.main_frame, text="Client", font=("Arial", 14), command=self.client_login)
        client_button.pack(pady=10, ipadx=10)

        banquier_button = tk.Button(self.main_frame, text="Banquier", font=("Arial", 14), command=self.banquier_login)
        banquier_button.pack(pady=10, ipadx=10)

    def client_login(self):
        self.clear_screen()

        label = tk.Label(self.main_frame, text="Connexion Client", font=("Arial", 18), bg="#f0f0f0")
        label.pack(pady=20)

        email_label = tk.Label(self.main_frame, text="E-mail", font=("Arial", 12), bg="#f0f0f0")
        email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.main_frame, font=("Arial", 12))
        self.email_entry.pack(pady=5, ipady=5)

        password_label = tk.Label(self.main_frame, text="Mot de passe", font=("Arial", 12), bg="#f0f0f0")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.main_frame, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5, ipady=5)

        login_button = tk.Button(self.main_frame, text="Se connecter", font=("Arial", 14), command=self.authenticate_client)
        login_button.pack(pady=20, ipadx=20)

        register_button = tk.Button(self.main_frame, text="Créer un compte", font=("Arial", 12), command=self.create_client_account)
        register_button.pack(pady=10)

    def banquier_login(self):
        self.clear_screen()

        label = tk.Label(self.main_frame, text="Connexion Banquier", font=("Arial", 18), bg="#f0f0f0")
        label.pack(pady=20)

        email_label = tk.Label(self.main_frame, text="E-mail", font=("Arial", 12), bg="#f0f0f0")
        email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.main_frame, font=("Arial", 12))
        self.email_entry.pack(pady=5, ipady=5)

        password_label = tk.Label(self.main_frame, text="Mot de passe", font=("Arial", 12), bg="#f0f0f0")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.main_frame, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5, ipady=5)

        login_button = tk.Button(self.main_frame, text="Se connecter", font=("Arial", 14), command=self.authenticate_banquier)
        login_button.pack(pady=20, ipadx=20)

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

    def obtenir_clients_par_banquier(banquier_id):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Adeletdehlia21!",
            database="base_budget"
        )
        cursor = db.cursor()
        query = "SELECT * FROM client WHERE banquier_id = %s"
        cursor.execute(query, (banquier_id,))
        clients = cursor.fetchall()
        cursor.close()
        return clients

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
            return True if result else False
        except Error as e:
            messagebox.showerror("Erreur de connexion", f"Erreur de connexion à la base de données: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def open_dashboard(self, role, email):
        self.clear_screen()

        full_name = self.get_client_name(email)

        dashboard_label = tk.Label(self.main_frame, text=f"Tableau de bord {role}", font=("Arial", 18), bg="#f0f0f0")
        dashboard_label.pack(pady=20)

        welcome_label = tk.Label(self.main_frame, text=f"Bienvenue {full_name}!", font=("Arial", 14), bg="#f0f0f0")
        welcome_label.pack(pady=20)

        balance_label = tk.Label(self.main_frame, text="Solde : ", font=("Arial", 14), bg="#f0f0f0")
        balance_label.pack(pady=10)

        balance = self.get_balance(role, email)
        balance_value_label = tk.Label(self.main_frame, text=f"{balance} €", font=("Arial", 14), bg="#f0f0f0")
        balance_value_label.pack(pady=5)

        transaction_button = tk.Button(self.main_frame, text="Nouvelle transaction", font=("Arial", 14), command=self.create_transaction)
        transaction_button.pack(pady=10)

        history_button = tk.Button(self.main_frame, text="Historique des transactions", font=("Arial", 14), command=self.show_transaction_history)
        history_button.pack(pady=10)

        logout_button = tk.Button(self.main_frame, text="Se déconnecter", font=("Arial", 14), command=self.logout)
        logout_button.pack(pady=10)

        self.bind("<Escape>", lambda event: self.open_dashboard(role, email))
    
    def get_client_name(self, email):
        conn = mysql.connector.connect(host="localhost", user="root", password="Adeletdehlia21!", database="base_budget")
        cursor = conn.cursor()
        cursor.execute("SELECT nom, prenom FROM client WHERE email = %s", (email,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return f"{result[0]} {result[1]}" 
        return "Utilisateur inconnu" 

    def make_transaction(self, montant):
        self.current_balance += montant

        if self.current_balance < 0:
            self.show_negative_balance_warning()

        self.update_balance_label()

    def show_negative_balance_warning(self):
        # Affiche un message d'alerte lorsque le solde est négatif
        messagebox.showwarning("Solde négatif", "Alerte : Votre solde est maintenant négatif. Veuillez vérifier vos transactions.")

    def update_balance_label(self):
        balance_label = tk.Label(self.main_frame, text=f"Solde actuel : {self.current_balance} €", font=("Arial", 14), bg="#f0f0f0")
        balance_label.pack(pady=5)

    def get_balance(self, role, email):
        if role != "Client":
            return 0

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Adeletdehlia21!",
                database="base_budget"
            )
            cursor = connection.cursor()
            # Récupérer l'id du client
            cursor.execute("SELECT id FROM client WHERE email = %s", (email,))
            result = cursor.fetchone()
            if not result:
                return 0
            client_id = result[0]
            cursor.execute("SELECT type, montant FROM transaction WHERE client_id = %s", (client_id,))
            transactions = cursor.fetchall()
            balance = 0.0
            for t in transactions:
                t_type, amount = t[0], float(t[1])
                if t_type == "Dépôt":
                    balance += amount
                elif t_type == "Retrait":
                    balance -= amount
                elif t_type == "Transfert":
                    balance -= amount
            return balance
        except Error as e:
            messagebox.showerror("Erreur de connexion", f"Erreur de connexion à la base de données: {e}")
            return 0
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def create_transaction(self):
        self.clear_screen()

        transaction_label = tk.Label(self.main_frame, text="Nouvelle transaction", font=("Arial", 18), bg="#f0f0f0")
        transaction_label.pack(pady=20)

        type_label = tk.Label(self.main_frame, text="Type de transaction (Dépôt/Retrait/Transfert)", font=("Arial", 12), bg="#f0f0f0")
        type_label.pack(pady=5)
        self.transaction_type_entry = tk.Entry(self.main_frame, font=("Arial", 12))
        self.transaction_type_entry.pack(pady=5, ipady=5)

        montant_label = tk.Label(self.main_frame, text="Montant", font=("Arial", 12), bg="#f0f0f0")
        montant_label.pack(pady=5)
        self.montant_entry = tk.Entry(self.main_frame, font=("Arial", 12))
        self.montant_entry.pack(pady=5, ipady=5)

        description_label = tk.Label(self.main_frame, text="Description", font=("Arial", 12), bg="#f0f0f0")
        description_label.pack(pady=5)
        self.description_entry = tk.Entry(self.main_frame, font=("Arial", 12))
        self.description_entry.pack(pady=5, ipady=5)

        transaction_button = tk.Button(self.main_frame, text="Confirmer la transaction", font=("Arial", 14), command=self.process_transaction)
        transaction_button.pack(pady=20)

    def process_transaction(self):
        transaction_type = self.transaction_type_entry.get().lower()
        try:
            montant = float(self.montant_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Montant invalide")
            return
        description = self.description_entry.get()

        if transaction_type == "dépôt":
            self.ajouter_solde(montant)
        elif transaction_type == "retrait":
            self.soustraire_solde(montant)
        elif transaction_type == "transfert":
            try:
                client_id_dest = int(description)
            except ValueError:
                messagebox.showerror("Erreur", "Pour un transfert, la description doit contenir l'ID du client destinataire")
                return
            self.transfert_solde(montant, client_id_dest)
        else:
            messagebox.showerror("Erreur", "Type de transaction invalide")
            return

        self.add_transaction_to_history(transaction_type, montant, description)
        messagebox.showinfo("Succès", "Transaction réalisée avec succès!")
        self.open_dashboard(self.current_user_role, self.current_user_email)

    def ajouter_solde(self, montant):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Adeletdehlia21!",
                database="base_budget"
            )
            cursor = connection.cursor()
            # Récupérer l'id du client à partir de l'email
            cursor.execute("SELECT id FROM client WHERE email = %s", (self.current_user_email,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Erreur", "Client non trouvé")
                return
            client_id = result[0]
            query = "INSERT INTO transaction (client_id, type, montant, description, date, categorie_id) VALUES (%s, 'Dépôt', %s, %s, NOW(), 10)"
            cursor.execute(query, (client_id, montant, "Dépôt"))
            connection.commit()
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors du dépôt: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def soustraire_solde(self, montant):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Adeletdehlia21!",
                database="base_budget"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM client WHERE email = %s", (self.current_user_email,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Erreur", "Client non trouvé")
                return
            client_id = result[0]
            query = "INSERT INTO transaction (client_id, type, montant, description, date, categorie_id) VALUES (%s, 'Retrait', %s, %s, NOW(), 2)"
            cursor.execute(query, (client_id, montant, "Retrait"))
            connection.commit()
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors du retrait: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def transfert_solde(self, montant, client_id_dest):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Adeletdehlia21!",
                database="base_budget"
            )
            cursor = connection.cursor()
            # Récupérer l'id du client expéditeur
            cursor.execute("SELECT id FROM client WHERE email = %s", (self.current_user_email,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Erreur", "Client expéditeur non trouvé")
                return
            client_id_source = result[0]
            query = "INSERT INTO transaction (client_id, type, montant, description, date, categorie_id) VALUES (%s, 'Transfert', %s, %s, NOW(), 11)"
            description = f"Transfert vers client {client_id_dest}"
            cursor.execute(query, (client_id_source, montant, description))
            connection.commit()
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors du transfert: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def add_transaction_to_history(self, transaction_type, montant, description):
        pass 

    def show_transaction_history(self):
        self.clear_screen()

        history_label = tk.Label(self.main_frame, text="Historique des Transactions", font=("Arial", 18), bg="#f0f0f0")
        history_label.pack(pady=20)

        # Boutons de filtrage
        filter_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        filter_frame.pack(fill="x", padx=10, pady=10)

        # Bouton d'application du filtre
        filter_button = tk.Button(filter_frame, text="Filtrer", command=self.apply_filters)
        filter_button.grid(row=0, column=4, padx=5, pady=5)

        tree = ttk.Treeview(self.main_frame, columns=("id", "type", "montant", "date", "description"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("type", text="Type")
        tree.heading("montant", text="Montant (€)")
        tree.heading("date", text="Date")
        tree.heading("description", text="Description")
        tree.pack(pady=20)

        transactions = self.get_transaction_history()
        for transaction in transactions:
            tree.insert("", "end", values=transaction)

        back_button = tk.Button(self.main_frame, text="Retour", font=("Arial", 14), command=lambda: self.open_dashboard(self.current_user_role, self.current_user_email))
        back_button.pack(pady=10)

        graph_button = tk.Button(self.main_frame, text="Afficher graphique des transactions", font=("Arial", 14), command=self.show_transaction_graph)
        graph_button.pack(pady=10)

        self.bind("<Escape>", lambda event: self.open_dashboard(self.current_user_role, self.current_user_email))


    def get_transaction_history(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Adeletdehlia21!",
                database="base_budget"
            )
            cursor = connection.cursor()
            # On récupère toutes les transactions du client connecté
            cursor.execute("SELECT id, type, montant, date, description FROM transaction WHERE client_id = (SELECT id FROM client WHERE email = %s)", (self.current_user_email,))
            result = cursor.fetchall()
            return result
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération de l'historique: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                
    def show_transaction_graph(self):
        self.clear_screen()

        # Ajouter un titre pour la page
        graph_label = tk.Label(self.main_frame, text="Graphique des transactions", font=("Arial", 18), bg="#f0f0f0")
        graph_label.pack(pady=20)

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Adeletdehlia21!",
                database="base_budget"
            )
            cursor = connection.cursor()

            # Récupérer l'id du client
            cursor.execute("SELECT id FROM client WHERE email = %s", (self.current_user_email,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Erreur", "Client non trouvé")
                return
            client_id = result[0]

            # Récupérer les types de transactions et leur montant
            cursor.execute("SELECT type, SUM(montant) FROM transaction WHERE client_id = %s GROUP BY type", (client_id,))
            transactions = cursor.fetchall()

            # Fermer la connexion
            connection.commit()

            # Préparer les données pour le graphique
            transaction_types = []
            transaction_amounts = []
            for t in transactions:
                transaction_types.append(t[0])
                transaction_amounts.append(t[1])

            # Créer le graphique
            fig, ax = plt.subplots()
            ax.pie(transaction_amounts, labels=transaction_types, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Pour un graphique circulaire parfait

            canvas = FigureCanvasTkAgg(fig, master=self.main_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=20)

        except Error as e:
            messagebox.showerror("Erreur de connexion", f"Erreur de connexion à la base de données: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    # Méthode get_transactions intégrée sans modification d'autre
    def get_transactions(self, client_id=None, transaction_type=None, category_id=None, 
                         date_start=None, date_end=None, sort_by="date", sort_order="DESC"):
        """Récupère les transactions selon les critères spécifiés"""
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Adeletdehlia21!",
                database="base_budget"
            )
            cursor = connection.cursor(dictionary=True)
            
            # Construire la requête SQL
            query = """
            SELECT t.*, c.nom as categorie_nom
            FROM transaction t
            LEFT JOIN categories c ON t.categorie_id = c.id
            WHERE 1=1
            """
            params = []
            
            # Ajouter les filtres
            if client_id:
                query += " AND t.client_id = %s"
                params.append(client_id)
            
            if transaction_type and transaction_type != "Tous":
                query += " AND t.type = %s"
                params.append(transaction_type)
            
            if category_id and category_id != 0:
                query += " AND t.categorie_id = %s"
                params.append(category_id)
            
            if date_start:
                query += " AND t.date >= %s"
                params.append(date_start)
            
            if date_end:
                query += " AND t.date <= %s"
                params.append(date_end)
            
            # Ajouter le tri
            query += f" ORDER BY t.{sort_by} {sort_order}"
            
            cursor.execute(query, tuple(params))
            transactions = cursor.fetchall()
            return transactions
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des transactions : {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    # Exemple d'utilisation de get_transactions
    def show_filtered_transactions(self):
        """Affiche les transactions filtrées (exemple: uniquement les dépôts)"""
        # Récupérer l'id du client à partir de l'email
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Adeletdehlia21!",
                database="base_budget"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM client WHERE email = %s", (self.current_user_email,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Erreur", "Client non trouvé")
                return
            client_id = result[0]
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération de l'identifiant du client: {e}")
            return
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        # Appel de la méthode get_transactions pour récupérer uniquement les dépôts
        transactions = self.get_transactions(client_id=client_id, transaction_type="Dépôt")

        # Création d'une nouvelle fenêtre pour afficher les transactions
        filter_window = tk.Toplevel(self)
        filter_window.title("Transactions Filtrées")
        filter_window.geometry("600x400")
        
        tree = ttk.Treeview(filter_window, columns=("id", "type", "montant", "date", "categorie"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("type", text="Type")
        tree.heading("montant", text="Montant (€)")
        tree.heading("date", text="Date")
        tree.heading("categorie", text="Catégorie")
        tree.pack(fill="both", expand=True)

        # Insertion des transactions dans le Treeview
        for transaction in transactions:
            tree.insert("", "end", values=(
                transaction.get("id"),
                transaction.get("type"),
                transaction.get("montant"),
                transaction.get("date"),
                transaction.get("categorie_nom")
            ))

        close_button = tk.Button(filter_window, text="Fermer", command=filter_window.destroy)
        close_button.pack(pady=10)

    def logout(self):
        self.is_logged_in = False
        self.current_user_email = ""
        self.current_user_role = ""
        self.clear_screen()
        self.create_home_screen()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
