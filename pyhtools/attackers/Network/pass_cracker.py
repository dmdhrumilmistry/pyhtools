import hashlib
from pyhtools.UI.colors import *

class HashCracker:
    '''
    Class to crack hashed passwords obtained via ARP poisoning, MITM, etc.
    
    Args:
        mode (str) : hash type of password to crack.
        path (str) : path to plaintext passwords file.
        hash (int) : hash  you want to crack.
    
    Methods:
        crack : Cracks hashed value by bruteforcing plaintext passwords through user-specific algorithm.
    '''

    def __init__(self):
        self.mode = self.args.mode
        self.path = self.args.path
        self.hash_to_decrypt = self.args.hash
      
    def crack(self):  
        with open(self.path, 'r') as f:
            print(BRIGHT_YELLOW + 'Decrypting...')
            for line in f.readlines():
                if self.mode == 'md5':
                    hash_object = hashlib.md5(line.strip().encode())
                    hashed_word = hash_object.hexdigest()
                    if hashed_word == self.hash_to_decrypt:
                        print(BRIGHT_WHITE + f'[+] Password Found from MD5 hash: {line.strip()}')
                        exit(0)
                
                elif self.mode == 'sha1':
                    hash_object = hashlib.sha1(line.strip().encode())
                    hashed_word = hash_object.hexdigest()
                    if hashed_word == self.hash_to_decrypt:
                        print(BRIGHT_WHITE + f'[+] Password Found from SHA-1 hash: {line.strip()}')
                        exit(0)
                        
                elif self.mode == 'sha2':
                    hash_object = hashlib.sha256(line.strip().encode())
                    hashed_word = hash_object.hexdigest()
                    if hashed_word == self.hash_to_decrypt:
                        print(BRIGHT_WHITE + f'Password found from SHA-2 hash: {line.strip()}')
                        exit(0)
            
            print(BRIGHT_RED + '[-] Password Not Found.')