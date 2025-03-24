import string
import bcrypt
import mysql.connector

class Connexion:
    def __init__(self):
        self.pepper = 'chocolatomaco'
        self.db_config = {
            'host': "localhost",
            'port': 3306,
            'user': "root",
            'password': input("mdp:"),
            'database': "base_budget"
        }

    def get_connection(self):
        """Retourne une connexion MySQL."""
        return mysql.connector.connect(**self.db_config)

    def account_entries(self):
        """Récupère les informations utilisateur pour la création de compte."""
        name = self.name_entry.get()
        firstname = self.firstname_entry.get()
        mail = self.mail_entry.get()
        password1 = self.password1_entry.get()
        password2 = self.password2_entry.get()

        if password1 == password2:
            print("Same password")
            if all(c in string.printable for c in password1):
                return password1, name, firstname, mail
            else:
                print("Non-usable character detected.")
                return None
        else:
            print("Error: passwords do not match.")
            return None

    def verification_password(self,password):
        """Vérifie que le mot de passe est sécurisé."""
        uppercase = any(c in string.ascii_uppercase for c in password)
        lowercase = any(c in string.ascii_lowercase for c in password)
        numeral = any(c in string.digits for c in password)
        special = any(c in string.punctuation for c in password)

        if uppercase and lowercase and numeral and special:
            print("Password valid")
            return True
        else:
            print("Password not valid")
            return False

    def hash_password(self, password):
        """Hache le mot de passe avec un pepper et bcrypt."""
        add_password_pepper = password + self.pepper
        hashed_password = bcrypt.hashpw(add_password_pepper.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')  # Convertit bytes → str pour MySQL

    def verify_password(self, stored_hash, password):
        """Vérifie si un mot de passe correspond au hash stocké."""
        password_with_pepper = password + self.pepper
        stored_hash_bytes = stored_hash.encode('utf-8') if isinstance(stored_hash, str) else stored_hash
        return bcrypt.checkpw(password_with_pepper.encode('utf-8'), stored_hash_bytes)

    # def create_account(self):

    #     """Gère la création de compte avec hachage du mot de passe."""
    #     name = self.name_entry.get()
    #     firstname = self.firstname_entry.get()
    #     mail = self.mail_entry.get()
    #     password1 = self.password1_entry.get()
    #     password2 = self.password2_entry.get()

    #     if password1 == password2:
    #         print("Same password")
    #         if all(c in string.printable for c in password1):
    #             password=password1
    #         else:
    #             print("Non-usable character detected.")
    #             return None
    #     else:
    #         print("Error: passwords do not match.")
    #         return None

    #     # data = self.account_entries()
    #     # if not data:
    #     #     return

    #     # password, name, firstname, mail = data

    #     if self.verification_password(password):
    #         hashed = self.hash_password(password)

    #         try:
    #             cnx = self.get_connection()
    #             cursor = cnx.cursor()
    #             query = "INSERT INTO client (nom, prenom, email, mot_de_passe) VALUES (%s, %s, %s, %s)"
    #             cursor.execute(query, (name, firstname, mail, hashed))
    #             cnx.commit()
    #             print("Account created successfully!")
    #         except mysql.connector.Error as e:
    #             print(f"Database error: {e}")
    #         finally:
    #             cursor.close()
    #             cnx.close()
    #     else:
    #         print("Invalid password. Please try again.")

    def login(self):
        """Gère la connexion utilisateur avec vérification du mot de passe."""
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        try:
            cnx = self.get_connection()
            cursor = cnx.cursor()
            query = "SELECT mot_de_passe FROM client WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            if result:
                hashed_password = result[0]
                if self.verify_password(hashed_password, password):
                    print("Login successful!")
                else:
                    print("Wrong password.")
            else:
                print("User not found.")

        except mysql.connector.Error as e:
            print(f"Database error: {e}")

        finally:
            cursor.close()
            cnx.close()