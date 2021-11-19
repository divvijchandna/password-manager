
# Code from https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256

import base64
import hashlib
from getpass import getpass
from Crypto import Random
from Crypto.Cipher import AES
import os

class AESCipher(object):

    def __init__(self): 
        self.bs = AES.block_size

    def encrypt(self, raw, key):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc, key):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


aes = AESCipher()

raw_text = input("Enter Raw text: ")

salt = os.urandom(32)
password = input("Enter Password: ")
password = str(password)
key = hashlib.pbkdf2_hmac(
    'sha256', # The hash digest algorithm for HMAC
    password.encode('utf-8'), # Convert the password to bytes
    salt, # Provide the salt
    100000, # It is recommended to use at least 100,000 iterations of SHA-256 
    256
)

enc_text = aes.encrypt(raw_text, key)

print("encrypted text: ")
print()
print(enc_text)

password = input("Enter Password: ")
password = str(password)
key = hashlib.pbkdf2_hmac(
    'sha256', # The hash digest algorithm for HMAC
    password.encode('utf-8'), # Convert the password to bytes
    salt, # Provide the salt
    100000, # It is recommended to use at least 100,000 iterations of SHA-256 
    256
)

dec_text = aes.decrypt(raw_text, key)


print("decrypted text: ")
print()
print(dec_text)


