
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
    cipher = AES.new(key, AES_MODE_AEX)
