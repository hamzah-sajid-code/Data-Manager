import os
import datetime
import time
import json
from simplecrypt import encrypt, decrypt

def encryptText(key, string):
    ciphercode = encrypt(key, string)
    final = ciphercode.hex()
    return final

def encryptFile(key, fileName):
    with open(fileName, "rb") as f:
        data = f.read()
    ciphercode = encrypt(key, data)
    final = ciphercode.hex()
    return final


def decryptData(key, encryptedString):
    dataInBytes = bytes.fromhex(encryptedString)
    decryptDataVal = decrypt(key, dataInBytes)
    final = decryptDataVal.decode("utf-8")
    return final


def decryptFile(key, fileName):
    with open(fileName, "rb") as f:
        data = f.read()
    decryptDataVal = decrypt(key, data)
    final = decryptDataVal.decode("utf-8")
    return final

def logout():
    os.system("cls")
    os.system("py loginAndSignUp.py")