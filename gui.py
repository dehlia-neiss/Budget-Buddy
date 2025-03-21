import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
from connexion import get_connection, hash_password, verify_password, pepper
from auth import login, login_banquier

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Budget Buddy")
        self.geometry("400x400")
        self.configure(bg="#f0f0f0")
        self.create_home_screen()

    def create_home_screen(self):
        self.clear_screen()
        label = tk.Label(self, text="Bienvenue sur Budget Buddy", font=("Arial", 18), bg="#f0f0f0")
        label.pack(pady=20)

        # Bouton pour la connexion client
        client_button = tk.Button(self, text="Connexion Client", font=("Arial", 14), command=self.show_client_login)
        client_button.pack(pady=10)

        # Bouton pour la connexion banquier
        banquier_button = tk.Button(self, text="Connexion Banquier", font=("Arial", 14), command=self.show_banquier_login)
        banquier_button.pack(pady=10)

        # Bouton pour créer un compte client
        register_button = tk.Button(self, text="Créer un compte Client", font=("Arial", 14), command=self.show_register_screen)
        register_button.pack(pady=10)

    def show_client_login(self):
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

        submit_button = tk.Button(self, text="Se connecter", font=("Arial", 14), command=self.authenticate_client)
        submit_button.pack(pady=20)

        back_button = tk.Button(self, text="Retour", font=("Arial", 12), command=self.create_home_screen)
        back_button.pack(pady=5)

    def authenticate_client(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        user_id = login(email, password)
        if user_id:
            messagebox.showinfo("Succès", "Connexion client réussie")
            self.open_dashboard_client()
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")

    def show_banquier_login(self):
        self.clear_screen()
        label = tk.Label(self, text="Connexion Banquier", font=("Arial", 18), bg="#f0f0f0")
        label.pack(pady=20)

        email_label = tk.Label(self, text="E-mail", font=("Arial", 12), bg="#f0f0f0")
        email_label.pack(pady=5)
        self.banq_email_entry = tk.Entry(self, font=("Arial", 12))
        self.banq_email_entry.pack(pady=5)

        password_label = tk.Label(self, text="Mot de passe", font=("Arial", 12), bg="#f0f0f0")
        password_label.pack(pady=5)
        self.banq_password_entry = tk.Entry(self, font=("Arial", 12), show="*")
        self.banq_password_entry.pack(pady=5)

        submit_button = tk.Button(self, text="Se connecter", font=("Arial", 14), command=self.authenticate_banquier)
        submit_button.pack(pady=20)

        back_button = tk.Button(self, text="Retour", font=("Arial", 12), command=self.create_home_screen)
        back_button.pack(pady=5)

    def authenticate_banquier(self):
        email = self.banq_email_entry.get()
        password = self.banq_password_entry.get()
        banq_id = login_banquier(email, password)
        if banq_id:
            messagebox.showinfo("Succès", "Connexion banquier réussie")
            self.open_dashboard_banquier()
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")

    def show_register_screen(self):
        self.clear_screen()
        label = tk.Label(self, text="Créer un compte Client", font=("Arial", 18), bg="#f0f0f0")
        label.pack(pady=20)

        email_label = tk.Label(self, text="E-mail", font=("Arial", 12), bg="#f0f0f0")
        email_label.pack(pady=5)
        self.reg_email_entry = tk.Entry(self, font=("Arial", 12))
        self.reg_email_entry.pack(pady=5)

        password_label = tk.Label(self, text="Mot de passe", font=("Arial", 12), bg="#f0f0f0")
        password_label.pack(pady=5)
        self.reg_password_entry = tk.Entry(self, font=("Arial", 12), show="*")
        self.reg_password_entry.pack(pady=5)

        register_button = tk.Button(self, text="Créer", font=("Arial", 14), command=self.register)
        register_button.pack(pady=20)

        back_button = tk.Button(self, text="Retour", font=("Arial", 12), command=self.create_home_screen)
        back_button.pack(pady=5)

    def register(self):
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()
        hashed = hash_password(password, pepper)
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO client (email, mot_de_passe) VALUES (%s, %s)", (email, hashed))
            connection.commit()
            messagebox.showinfo("Succès", "Compte client créé avec succès")
            self.create_home_screen()
        except Error as e:
            messagebox.showerror("Erreur", str(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def open_dashboard_client(self):
        self.clear_screen()
        label = tk.Label(self, text="Tableau de bord Client", font=("Arial", 18), bg="#f0f0f0")
        label.pack(pady=20)
        logout_button = tk.Button(self, text="Se déconnecter", font=("Arial", 14), command=self.create_home_screen)
        logout_button.pack(pady=10)

    def open_dashboard_banquier(self):
        self.clear_screen()
        label = tk.Label(self, text="Tableau de bord Banquier", font=("Arial", 18), bg="#f0f0f0")
        label.pack(pady=20)
        logout_button = tk.Button(self, text="Se déconnecter", font=("Arial", 14), command=self.create_home_screen)
        logout_button.pack(pady=10)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
