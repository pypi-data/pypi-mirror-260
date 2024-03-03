from os import system,name,urandom
from time import sleep 
import sys
import hashlib
import string
import random

def clearShell():
    if name == 'nl':
        _ = system('cls')
    else:
        _ = system('clear')
        
def type(message, interval=""):
    for i in message:
        sys.stdout.write(i)
        sys.stdout.flush()
        if interval:
            sleep(float(interval))
        else:
            sleep(0.01)
            
def list_directory():
    system('dir')
def wait(milliseconds):
    sleep(milliseconds)
def salt(chars, unencoded):
    salt = urandom(chars)
    if unencoded == True:
        return str(salt)
    elif unencoded == False:
        saltEncoded = str(salt)
        saltEncoded2 = saltEncoded.encode()
        return saltEncoded2
        
def hash(string,method=""):
    stringRaw = str(string).encode(encoding="utf-8")
    if method == "sha256":
        algorithm = hashlib.sha256()
    elif method == "md5":
        algorithm = hashlib.md5()
    else:
        raise ValueError("Invalid Algorithm")
    algorithm.update(stringRaw)
    return stringRaw,algorithm.hexdigest()
    
class pyRandom:
    def string(case=""):
        if case == "lowercase":
            return random.choice(string.ascii_lowercase)
        elif case == "uppercase":
            return random.choice(string.ascii_uppercase)
        else:
            return random.choice(string.ascii_letters)
    def number(LowerNumber,HigherNumber):
        return random.randint(LowerNumber,HigherNumber)

    charList = ['!','@','#','$','%','^','&','*','*','(',')','-', '_','=','+','`','~',',','<','.','>',';',':','{','}','[',']','|']
    charRandom = random.choice(charList)
    
class pyHelp:
    def all():
        print("clearShell(): clears shell\nlist_directory(): Lists directories within the active directory")
        print("type(text): Only accepts 1 argument and replaces 'print' with a type writer effect")
        print("wait(seconds): same as sleep() but saves the importing of time")
        print("salt(amountOfCharacters, [encoded?] True | False)")
        print("hash(string, method), hashes string with the supported methods: md5, sha256")
        print("pyRandom Class")
        print("---------------")
        print("string([optional] case= uppercase | lowercase)")
        print("number(firstNumber, secondNumber): generates one random number between the two argued numbers")
        print("charRandom: returns random generated symbol [utf-8]")

