
# Code from https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256

import base64
import hashlib
from getpass import getpass
from Crypto import Random
from Crypto.Cipher import AES
import os
from secrets import token_bytes

key = token_bytes(32)

def encrypt(msg):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode('ascii'))
    return nonce, ciphertext, tag

def decrypt(nonce, ciphertext, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce = nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        return plaintext.decode('ascii')
    except:
        return False

msg = input("Enter plaintext: ")
nonce, ciphertext, tag = encrypt(msg)
print('Ciphertext is: ', ciphertext)

plaintext = decrypt(nonce, ciphertext, tag)
if not plaintext:
    print('Message is corrupted')
else:
    print('Plaintext: ', plaintext)

