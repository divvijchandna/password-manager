import hashlib
import os
from getpass import getpass
from pymongo import MongoClient
import ssl

# This is main branch
# Adding Encrypted vault
# shaan : qwerty 
# divvij: 12345

def get_vault_key(master_password, username):

    salt = os.urandom(32) # Remember this
    combine = username + master_password

    key = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        combine.encode('utf-8'), # Convert the password to bytes
        salt, # Provide the salt
        100000, # It is recommended to use at least 100,000 iterations of SHA-256 
        256
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

    # Use the exact same setup you used to generate the key, but this time put in the password to check
    vault_key = hashlib.pbkdf2_hmac(
        'sha256',
        (username + password_to_check).encode('utf-8'), # Convert the password to bytes
        salt_from_storage, 
        100000,
        256
    )

    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        (str(vault_key) + password_to_check).encode('utf-8'), # Convert the password to bytes
        salt_from_storage, 
        100000
    )

    if new_key == key_from_storage:
        print('Password is correct')
    else:
        print('Password is incorrect')


def store_auth_hash(username, auth_hash_wsalt):

    uri = "mongodb+srv://shaandivvij:divvijshaan@cluster0.kvz4b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

    db = client.passwordManager
    collection = db.masterPasswords

    post = {"username": username, "auth_hash": auth_hash_wsalt}

    collection.insert_one(post)

def retrieve_auth_hash(username):

    uri = "mongodb+srv://shaandivvij:divvijshaan@cluster0.kvz4b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

    db = client.passwordManager
    collection = db.masterPasswords

    result = collection.find({"username": username})

    return result[0]["auth_hash"]

option = input("Add or Check (a/c)? ")

if option == 'a':

    username = input("Username: ")
    password = getpass()

    vault_key_wsalt = get_vault_key(password, username)
    salt = vault_key_wsalt[:32] # 32 is the length of the salt
    vault_key = vault_key_wsalt[32:]
    auth_hash_wsalt = get_auth_hash(vault_key, salt, password)

    store_auth_hash(username, auth_hash_wsalt)

elif option == 'c':

    username = input("Username: ")
    password = getpass()

    auth_hash_wsalt = retrieve_auth_hash(username)

    check_auth_hash(password, username, auth_hash_wsalt)




