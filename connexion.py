import mysql.connector
import bcrypt

# Define a pepper to strengthen password hashing
PEPPER = 'chocolatomaco'

def hash_password(password):
    """
    Adds a pepper to the password and returns its hash.
    """
    password_with_pepper = password + PEPPER
    hashed_password = bcrypt.hashpw(password_with_pepper.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')  # Store as string for DB

def verify_password(stored_hash, password):
    """
    Verifies if the provided password matches the stored hash.
    """
    password_with_pepper = password + PEPPER
    return bcrypt.checkpw(password_with_pepper.encode('utf-8'), stored_hash.encode('utf-8'))

def connect_db():
    """
    Establishes a connection to the MySQL database.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Adeletdehlia21!",
        database="base_budget",
        auth_plugin="mysql_native_password"
    )

def create_account(email, password):
    """
    Creates a new user account with a hashed password.
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Check if the email already exists
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        print("⚠️ Email already registered. Try logging in.")
        conn.close()
        return False

    # Hash the password and insert into the database
    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
    
    conn.commit()
    conn.close()
    print("✅ Account created successfully!")
    return True
