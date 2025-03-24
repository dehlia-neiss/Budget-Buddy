from connexion import get_connection, verify_password, pepper

def login(email, password):
    """
    Tente de connecter l'utilisateur client avec l'email et le mot de passe fournis.
    Retourne l'ID de l'utilisateur si la connexion réussit, sinon None.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, mot_de_passe FROM client WHERE email = %s", (email,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        user_id, stored_hash = result
        if verify_password(stored_hash, password, pepper):
            return user_id
    return None

def login_banquier(email, password):
    """
    Tente de connecter le banquier avec l'email et le mot de passe fournis.
    Retourne l'ID du banquier si la connexion réussit, sinon None.
    """
    conn = get_connection()
    cursor = conn.cursor()
    # Dans la table 'banquier', l'email est enregistré dans le champ 'mail'
    cursor.execute("SELECT id, mot_de_passe FROM banquier WHERE mail = %s", (email,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        banquier_id, stored_hash = result
        if verify_password(stored_hash, password, pepper):
            return banquier_id
    return None
    