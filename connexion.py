import mysql.connector
import string
import bcrypt

cnx=mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="base_budget"
)

mycursor = cnx.cursor()
mycursor.execute("select * from client")
for i in mycursor:
    print(i)
if cnx.is_connected():
    print("connexion to mysql suceed")

##########################################################################
      
def account_entries():
    name=input("enter your name:")
    firstname=input("enter your first name:")
    mail = input("enter your email:")
    password1=input("enter your password:")
    password2= input("verify your password:")
    if password1==password2:
        print("same password")  
        for i in range(len(password1)):
            if password1[i] in string.printable:
                print("ok")
            else:
                print("non-usasble character")
                break
        return password1, name, firstname, mail 
    else:
        print("error, not the same password")

def verification_password(password1):
    if any (a in string.ascii_uppercase for a in password1):
        uppercase=True
    else:
        uppercase=False
    if any (a in string.ascii_lowercase for a in password1):
        lowercase=True
    else:
        lowercase=False
    if any (a in string.digits for a in password1):
        numeral=True
    else:
        numeral=False
    if any (a in string.punctuation for a in password1):
        charaspe=True
    else:
        charaspe=False
    if uppercase and lowercase and numeral and charaspe:
        print("password valid")
        all=True
    else:
        print("password not valid")
        all=False
    return all


############################################################################


def hash_password(password,pepper):
    add_password_pepper= password + pepper
    hashed_password=bcrypt.hashpw(add_password_pepper.encode('utf-8'), bcrypt.gensalt())
    return hashed_password
   

def verify_password(stored_hash,password,pepper):
    password_with_pepper= password+pepper
    stored_hash_bytes = stored_hash.encode('utf-8') if isinstance(stored_hash, str) else stored_hash
    return bcrypt.checkpw(password_with_pepper.encode('utf-8'), stored_hash_bytes)

############################################################################

pepper= 'chocolatomaco'
new_account=input("do you want to create a new account (y/n):")
if new_account =="y":
    password1,name,firstname,mail=account_entries()
    all=verification_password(password1)
    if all:
        hashed=hash_password(password1,pepper)
        print(hashed)
        mycursor.execute(f"insert into client(nom,prenom,email,mot_de_passe) values (%s,%s,%s,%s)",(name,firstname,mail,hashed))
        cnx.commit()
        cnx.close()
    else: 
        print('invalid, try again')
else:
    print('no new account')

newlog=input("Do you want to try to login (y/n):")
if newlog=="y":
    mycursor = cnx.cursor()
    nametry=input("enter your user name:")
    passtry=input("enter your password :")
    mycursor.execute(f"select mot_de_passe from client where nom = %s",(nametry,))
    result=mycursor.fetchone()
    if result:
        hashed=result[0]
        validity=verify_password(hashed,passtry,pepper)
        if validity:
            print("right password")
            mycursor.execute(f"select * from client where nom = %s", (nametry,))
            user_data=mycursor.fetchall()
            print(user_data)
            cnx.commit()
            cnx.close()
        else:
            print("wrong password")
    else:
        print("user not found")
cnx.close()