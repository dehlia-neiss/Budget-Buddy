from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Adeletdehlia21!",
        database="base_budget"
    )

@app.route('/login', methods=['POST'])
def login():
    """
    Vérifie le login et le mot de passe fournis via un formulaire.
    Attendu en form-data : 
        - email : l'adresse email de l'utilisateur
        - password : le mot de passe (en clair)
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"error": "Email et mot de passe requis."}), 400

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM client WHERE email = %s AND mot_de_passe = %s", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Connexion réussie.", "client_id": user[0]}), 200
    else:
        return jsonify({"error": "Email ou mot de passe incorrect."}), 401

if __name__ == '__main__':
    app.run(debug=True)
