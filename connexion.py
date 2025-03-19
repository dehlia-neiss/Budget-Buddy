import mysql.connector
import string
import bcrypt

# cnx=mysql.connector.connect(
#     host="localhost",
#     port=3306,
#     user="root",
#     password="",
#     database="base_budget"
# )

# mycursor = cnx.cursor()
# mycursor.execute("select * from client")
# if cnx.is_connected():
#     print("connexion to mysql suceed")

##########################################################################
      
def account_entries():
    name=input("enter your name:")
    firstname=input("enter your first name:")
    mail = input("enter your email:")
    password1=input("enter your password:")
    password2= input("verify your password:")
    if password1==password2:
        print("password valid")  
        for i in range(len(password1)):
            if password1[i] in string.printable:
                print("ok")
            else:
                print("non-usasble character")
                break

        return password1 
    else:
        print("error, not the same password")

############################################################################
pepper= 'chocolatomaco'
def hash_password(password,pepper):
    add_password_pepper= password + pepper
    hashed_password=bcrypt.hashpw(add_password_pepper.encode('utf-8'), bcrypt.gensalt())
    return hashed_password
    # mycursor.execute(f"insert into client(nom,prenom,email,mot_de_passe) values ({name},{firstname},{mail},{password})")

def verify_password(stored_hash,password,pepper):
    password_with_pepper= password+pepper
    return bcrypt.checkpw(password_with_pepper.encode('utf-8'), stored_hash)

############################################################################

new_account=input("do you want to create a new account (y/n):")
if new_account =="y":
    password1=account_entries()
    hashed=hash_password(password1,pepper)
    print(hashed)
    passtry='nene'
    validity=verify_password(hashed,passtry,pepper)
    if validity:
        print("right password")
    else:
        print("wrong password")
    


# cnx.close()