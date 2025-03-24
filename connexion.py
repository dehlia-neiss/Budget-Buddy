import mysql.connector
import string
import bcrypt

# Configuration de la connexion à la base de données
db_config = {
    'host': "localhost",
    'port': 3306,
    'user': "root",
    'password': "",
    'database': "base_budget"
}

def get_connection():
    """Retourne une nouvelle connexion MySQL en utilisant la configuration définie."""
    return mysql.connector.connect(**db_config)

def account_entries_cli():
    """
    Demande à l'utilisateur les informations pour créer un compte (pour usage CLI uniquement).
    Retourne un tuple (mot_de_passe, nom, prenom, email) si réussi, sinon None.
    """
    nom = input("Entrez votre nom : ")
    prenom = input("Entrez votre prénom : ")
    email = input("Entrez votre email : ")
    password1 = input("Entrez votre mot de passe : ")
    password2 = input("Vérifiez votre mot de passe : ")
    if password1 == password2:
        print("Les mots de passe correspondent.")
        for char in password1:
            if char in string.printable:
                print("ok")
            else:
                print("Caractère non utilisable détecté.")
                break
        return password1, nom, prenom, email 
    else:
        print("Erreur : les mots de passe ne correspondent pas.")
        return None

def verification_password(password):
    """
    Vérifie si le mot de passe contient au moins une majuscule, une minuscule, un chiffre et un caractère spécial.
    Retourne True si valide, sinon False.
    """
    uppercase = any(c in string.ascii_uppercase for c in password)
    lowercase = any(c in string.ascii_lowercase for c in password)
    numeral = any(c in string.digits for c in password)
    special = any(c in string.punctuation for c in password)
    
    if uppercase and lowercase and numeral and special:
        print("Mot de passe valide")
        return True
    else:
        print("Mot de passe non valide")
        return False

def hash_password(password, pepper):
    """
    Ajoute le pepper au mot de passe et retourne le mot de passe haché avec bcrypt.
    """
    password_with_pepper = password + pepper
    hashed_password = bcrypt.hashpw(password_with_pepper.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

def verify_password(stored_hash, password, pepper):
    """
    Vérifie que le mot de passe fourni (avec pepper) correspond au hash stocké.
    Retourne True si le mot de passe est correct, sinon False.
    """
    password_with_pepper = password + pepper
    stored_hash_bytes = stored_hash.encode('utf-8') if isinstance(stored_hash, str) else stored_hash
    return bcrypt.checkpw(password_with_pepper.encode('utf-8'), stored_hash_bytes)

# Pepper partagé utilisé pour le hachage des mots de passe
pepper = 'chocolatomaco'

if __name__ == "__main__":
    # Section de test en ligne de commande
    cnx = get_connection()
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM client")
    for i in cursor:
        print(i)
    if cnx.is_connected():
        print("Connexion à MySQL réussie.")
    
    new_account = input("Voulez-vous créer un nouveau compte (y/n) : ")
    if new_account.lower() == "y":
        result = account_entries_cli()
        if result:
            password, nom, prenom, email = result
            if verification_password(password):
                hashed = hash_password(password, pepper)
                print("Mot de passe haché :", hashed)
                cursor.execute(
                    "INSERT INTO client(nom, prenom, email, mot_de_passe) VALUES (%s, %s, %s, %s)", 
                    (nom, prenom, email, hashed)
                )
                cnx.commit()
            else:
                print('Mot de passe invalide, veuillez réessayer.')
    else:
        print('Aucun compte créé.')
    
    newlog = input("Voulez-vous vous connecter (y/n) : ")
    if newlog.lower() == "y":
        nom_try = input("Entrez votre nom d'utilisateur : ")
        pass_try = input("Entrez votre mot de passe : ")
        cursor.execute("SELECT mot_de_passe FROM client WHERE nom = %s", (nom_try,))
        result = cursor.fetchone()
        if result:
            stored_hash = result[0]
            if verify_password(stored_hash, pass_try, pepper):
                print("Mot de passe correct")
                cursor.execute("SELECT * FROM client WHERE nom = %s", (nom_try,))
                user_data = cursor.fetchall()
                print(user_data)
            else:
                print("Mot de passe incorrect")
        else:
            print("Utilisateur non trouvé")
    cnx.close()

