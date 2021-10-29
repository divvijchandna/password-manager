import hashlib
import os
from getpass import getpass
from pymongo import MongoClient
import ssl

# password = 'password123'

def get_hashed_password(password):

    salt = os.urandom(32) # Remember this

    key = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        password.encode('utf-8'), # Convert the password to bytes
        salt, # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
    )

    hash_storage = salt + key
    return hash_storage

def check_password(password_to_check, hash_storage):

    salt_from_storage = hash_storage[:32] # 32 is the length of the salt
    key_from_storage = hash_storage[32:]

    # Use the exact same setup you used to generate the key, but this time put in the password to check
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password_to_check.encode('utf-8'), # Convert the password to bytes
        salt_from_storage, 
        100000
    )

    if new_key == key_from_storage:
        print('Password is correct')
    else:
        print('Password is incorrect')


def store_password(username, hash_storage):

    uri = "mongodb+srv://divvij:.cabbDvp9V7tTy8@cluster0.tz0g1.mongodb.net/passwordManager?retryWrites=true&w=majority"
    client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

    db = client.passwordManager
    collection = db.masterPasswords

    post = {"username": username, "password_hash": hash_storage}

    collection.insert_one(post)

def retrieve_password(username):

    uri = "mongodb+srv://divvij:.cabbDvp9V7tTy8@cluster0.tz0g1.mongodb.net/passwordManager?retryWrites=true&w=majority"
    client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

    db = client.passwordManager
    collection = db.masterPasswords

    result = collection.find({"username": username})

    return result[0]["password_hash"]

option = input("Add or Check (a/c)? ")

if option == 'a':

    username = input("Username: ")
    password = getpass()

    hash_storage = get_hashed_password(password)

    store_password(username, hash_storage)

elif option == 'c':

    username = input("Username: ")
    password = getpass()

    hash_storage = retrieve_password(username)
    print(hash_storage)

    check_password(password, hash_storage)



# check_password('blahblah', hash_storage)

