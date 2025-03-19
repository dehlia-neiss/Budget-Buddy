from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'base_budget.db'

def get_db_connection():
    """Ouvre une connexion à la base de données SQLite."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

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

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Connexion réussie."}), 200
    else:
        return jsonify({"error": "Email ou mot de passe incorrect."}), 401

if __name__ == '__main__':
    app.run(debug=True)
