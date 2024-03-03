from os import system,name,urandom
from time import sleep 
import sys
import hashlib
import string
import random
import socket
from pythonping import ping

try:
	hostName = socket.gethostname()
	__IP__ = socket.gethostbyname(hostName)
except:
	pass

def clearShell():
	system('cls')

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
class pyPing:
	def pingServer(servername, print=False):
    		if print==True:
        		pingServer = ping(servername, verbose=True)
        		return pingServer
    		else:
        		pingServer = str(ping(servername, verbose=False))
        		pingServerRawText = pingServer.replace("Reply from ", "").replace(" bytes in ", ",").replace(" ", "").replace("ms", "")

        		return pingServerRawText
	def pingSweep(serverhost=''):
		dot = IP.rfind(".")
		serverhost = serverhost[0:dot + 1]
		for i in range(1, 255):
    			host = serverhost + str(i)
    			response = os.system("ping -c 1 -w 1 " + host + " >/dev/null")
 
    			if response == 0:
        			return f'{host} is up'
    			else:
        			return f'{host} is up'
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
	print("__IP__: Your IP address")
	print("hostName: Your host name")
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

