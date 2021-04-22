import hashlib
from pathlib import Path

BLOCKSIZE = 65536
def file_hash(path):
    #proses hashing file dengan algoritma SHA1
    #input: path ke sebuah file
    #output: hex digest

    hasher = hashlib.sha1()
    with open(path, 'rb') as source:
        buf = source.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = source.read(BLOCKSIZE)

    return(str(hasher.hexdigest()))

def text_hash(message):
    #proses hashing pesan dengan algoritma SHA1
    #input: sebuah pesan (plain)
    #output: hex digest
    
    message = message.encode()
    hash_object = hashlib.sha1(message)
    hexadigest = hash_object.hexdigest()

    return(hexadigest)
