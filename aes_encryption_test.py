
# Code from https://www.youtube.com/watch?v=GYCVmMCRmTM

import base64
import hashlib
from getpass import getpass
from Crypto import Random
from Crypto.Cipher import AES
import os
from secrets import token_bytes

def encrypt(msg, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode('ascii'))
    return nonce, ciphertext, tag

def decrypt(key, nonce, tag, ciphertext):
    cipher = AES.new(key, AES.MODE_EAX, nonce = nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        return plaintext.decode('ascii')
    except:
        return False



password = input('Enter password: ')

salt = os.urandom(32) # Remember this
key = hashlib.pbkdf2_hmac(
    'sha256', # The hash digest algorithm for HMAC
    password.encode('utf-8'), # Convert the password to bytes
    salt, # Provide the salt
    100000 # It is recommended to use at least 100,000 iterations of SHA-256 
)

msg = input("Enter plaintext: ")
nonce, ciphertext, tag = encrypt(msg, key)
print('Ciphertext is: ', ciphertext)

plaintext = decrypt(key, nonce, tag, ciphertext)
if not plaintext:
    print('Message is corrupted')
else:
    print('Plaintext: ', plaintext)
    print('key type:', type(key))
    print('key size: ', len(key))
    print('nonce type:', type(nonce))
    print('nonce size: ', len(nonce))
    print('tag type:', type(tag))
    print('tag size: ', len(tag))

