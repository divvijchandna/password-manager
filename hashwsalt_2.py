from aes_encryption_test import *
from password_maker import *
import hashlib
import os
from getpass import getpass
from pymongo import MongoClient
import ssl

# This is main branch
# shaan : qwerty 
# divvij: 12345

def get_vault_key(master_password, salt, username):

    combine = username + master_password

    key = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        combine.encode('utf-8'), # Convert the password to bytes
        salt, # Provide the salt
        100000, # It is recommended to use at least 100,000 iterations of SHA-256 
    )

    vault_key_wsalt = salt + key
    return vault_key_wsalt


def get_auth_hash(vault_key, salt, master_password):
    
    combine = str(vault_key) + master_password

    key = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        combine.encode('utf-8'), # Convert the password to bytes
        salt, # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
    )

    auth_hash_wsalt = salt + key
    return auth_hash_wsalt

def check_auth_hash(password_to_check, username, auth_hash_wsalt):

    salt_from_storage = auth_hash_wsalt[:32] # 32 is the length of the salt
    key_from_storage = auth_hash_wsalt[32:]

    salt_vault = retrieve_vault_salt(username)

    # Use the exact same setup you used to generate the key, but this time put in the password to check
    vault_key = hashlib.pbkdf2_hmac(
        'sha256',
        (username + password_to_check).encode('utf-8'), # Convert the password to bytes
        salt_vault, 
        100000,
    )

    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        (str(vault_key) + password_to_check).encode('utf-8'), # Convert the password to bytes
        salt_from_storage, 
        100000
    )
    
    
    if new_key == key_from_storage:
        return True
    else:
        return False

def store_auth_hash(username, auth_hash_wsalt, salt_vault):
    # Essesntially creating an account
    uri = "mongodb+srv://divvij:.cabbDvp9V7tTy8@cluster0.tz0g1.mongodb.net/passwordManager?retryWrites=true&w=majority"
    client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

    db = client.passwordManager
    collection = db.masterPasswords

    post = {"username": username, "auth_hash": auth_hash_wsalt, "record": 'Empty', "nonce": 'Empty', "tag": 'Empty', "salt_vault": salt_vault}

    collection.insert_one(post)

def store_record(username, enc_record, nonce, tag):

    uri = "mongodb+srv://divvij:.cabbDvp9V7tTy8@cluster0.tz0g1.mongodb.net/passwordManager?retryWrites=true&w=majority"
    client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

    db = client.passwordManager
    collection = db.masterPasswords

    collection.update_one({"username": username}, {"$set":{"record": enc_record}})
    collection.update_one({"username": username}, {"$set":{"nonce": nonce}})
    collection.update_one({"username": username}, {"$set":{"tag": tag}})

def retrieve_auth_hash(username):

    uri = "mongodb+srv://divvij:.cabbDvp9V7tTy8@cluster0.tz0g1.mongodb.net/passwordManager?retryWrites=true&w=majority"
    client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

    db = client.passwordManager
    collection = db.masterPasswords

    result = collection.find({"username": username})

    return result[0]["auth_hash"]

def retrieve_record(username):

    uri = "mongodb+srv://divvij:.cabbDvp9V7tTy8@cluster0.tz0g1.mongodb.net/passwordManager?retryWrites=true&w=majority"
    client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

    db = client.passwordManager
    collection = db.masterPasswords

    result = collection.find({"username": username})

    return result[0]["record"], result[0]["nonce"], result[0]["tag"]

def retrieve_vault_salt(username):

    uri = "mongodb+srv://divvij:.cabbDvp9V7tTy8@cluster0.tz0g1.mongodb.net/passwordManager?retryWrites=true&w=majority"
    client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

    db = client.passwordManager
    collection = db.masterPasswords

    result = collection.find({"username": username})

    return result[0]["salt_vault"]


print("1.Add Account: a \n2.Check if Master-Password is Correct: c \n3.Add password to Account: ap \n4.View all website-password pairs: v")
print()
option = input('Enter your selection: ')

if option == 'a':

    username = input("Username: ")
    password = getpass()
    salt1 = os.urandom(32) # Remember this
    salt2 = os.urandom(32) # Remember this

    vault_key_wsalt = get_vault_key(password, salt1, username)
    salt = vault_key_wsalt[:32] # 32 is the length of the salt
    vault_key = vault_key_wsalt[32:]
    auth_hash_wsalt = get_auth_hash(vault_key, salt2, password)

    store_auth_hash(username, auth_hash_wsalt, salt1)
    print('Done')

elif option == 'c':

    username = input("Username: ")
    password = getpass()

    auth_hash_wsalt = retrieve_auth_hash(username)

    check = check_auth_hash(password, username, auth_hash_wsalt)
    if check:
        print('Password is correct')
    else:
        print('Password is incorrect')


elif option == 'ap':

    username = input("Username: ")
    password = getpass()

    auth_hash_wsalt = retrieve_auth_hash(username)

    check = check_auth_hash(password, username, auth_hash_wsalt)

    # salt_from_storage = auth_hash_wsalt[:32] # 32 is the length of the salt
    # key_from_storage = auth_hash_wsalt[32:]

    if not check:
        print('Password is incorrect. Try again.')
    else:
        # vault_key_wsalt = get_vault_key(password, username)
        record, nonce, tag = retrieve_record(username)
        website = str(input("Website name: "))
        password_length = int(input("Password length: "))
        password_record = str(make_password(password_length))

        email_user = str(input("Enter email used for website login: "))

        vault_salt = retrieve_vault_salt(username)
        vault_key_wsalt = get_vault_key(password, vault_salt, username)
        vault_key = vault_key_wsalt[32:]

        if(record == 'Empty'):
            nonce, ciphertext, tag = encrypt(website+'||'+email_user+'||'+password_record, vault_key)
            store_record(username, ciphertext, nonce, tag)
        else:
            dec_record = decrypt(vault_key, nonce, tag, record)
            websites_all = []
            emails_all = []
            passwords_all = []
            for tup in dec_record.split('|||'):
                li = str(tup).split('||')
                websites_all.append(str(li[0]).lower())
                emails_all.append(str(li[1]).lower())
                passwords_all.append(str(li[2]))
            
            flag = 0
            if (website.lower() in websites_all) and (email_user.lower() in emails_all):
                indices_of_website = [i for i, x in enumerate(websites_all) if x == website]
                for ind in indices_of_website:
                    if(emails_all[ind] == email_user.lower()):
                        flag = 1
                        passwords_all[ind] = password_record
                        dec_record = ''
                        dec_record = websites_all[0] + '||' + emails_all[0] + '||' + passwords_all[0]
                        for i in range(1, len(websites_all)):
                            dec_record = dec_record + '|||' + websites_all[i] + '||' + emails_all[i] + '||' + passwords_all[i]
                        break

            if(flag==0):
                dec_record = dec_record + '|||' + website + '||' + email_user + '||' + password_record

            nonce, ciphertext, tag = encrypt(dec_record, vault_key)
            store_record(username, ciphertext, nonce, tag) 

elif option == 'v':

    username = input("Username: ")
    password = getpass()

    auth_hash_wsalt = retrieve_auth_hash(username)

    check = check_auth_hash(password, username, auth_hash_wsalt)

    # salt_from_storage = auth_hash_wsalt[:32] # 32 is the length of the salt
    # key_from_storage = auth_hash_wsalt[32:]

    if not check:
        print('Password is incorrect. Try again.')
    else:
        # vault_key_wsalt = get_vault_key(password, username)
        record, nonce, tag = retrieve_record(username)
        salt_vault = retrieve_vault_salt(username)
        vault_key_wsalt = get_vault_key(password, salt_vault, username)
        vault_key = vault_key_wsalt[32:]
        if(record == 'Empty'):
            print(record)
        else:
            dec_record = decrypt(vault_key, nonce, tag, record)
            print(dec_record)