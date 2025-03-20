from connexion import connect_db, verify_password

def login(email, password):
    """
    Attempts to log in the user with the given email and password.
    Returns the user ID if successful; otherwise, returns None.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, mot_de_passe FROM client WHERE email = %s", (email,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        user_id, stored_hash = result
        if verify_password(stored_hash, password):
            return user_id
    return None
