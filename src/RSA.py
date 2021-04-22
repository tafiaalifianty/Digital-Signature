from utils import *

def generate_key(size):
    #pembangkitan kunci publik dan privat seukuran size bits
    #input: ukuran kunci
    #output: pasangan (d, e, n) kunci

    p = get_new_prime(size)
    q = get_new_prime(size)
    n = p*q

    totient = (p-1) * (q-1)
    e = random.randint(1, totient)

    while(gcd(e, totient) != 1):
        e = random.randint(1, totient)
    
    for k in range(1, totient):
        if((e * k) % totient == 1):
            break

    d = k
    
    key = (int(d), e, n)

    return(key)

def encrypt(key, message):
    #enkripsi pesan dengan algoritma RSA
    #input: key adalah kunci pasangan nilai, pesan adalah plain
    #output: cipher berupa hex string

    publicKey, n = key
    result = []
    plain = []

    for i in message:
        ascii_code = ''
        for j in range(len(str(ord(i))), 3):
            ascii_code = '0' + ascii_code
        ascii_code += str(ord(i))
        plain.append(ascii_code)
    
    plain = list(chunkstring("".join(plain), len(str(n))-1))
    
    for x in plain:
        cipher = pow(int(x), publicKey, n)
        cipher_code = ''
        for i in range(len(format(cipher, 'x')), 4):
            cipher_code = '0' + cipher_code
        cipher_code += format(cipher, "x")
        result.append(cipher_code)

    return("".join(result))

def decrypt(key, message):
    #dekripsi pesan dengan algoritma RSA
    #input: key adalah kunci pasangan nilai, pesan adalah cipher (hex string)
    #output: plain string
    
    private, n = key
    
    cipher = list(chunkstring(message, 4))
    message = []
    for x in cipher:
        ascii_code = int(x, 16)
        plain = pow(ascii_code, private, n)
        plain_code = ''
        for i in range(len(str(plain)), len(str(n))-1):
            plain_code = '0' + plain_code
        plain_code += str(plain)
        message.append(plain_code)
    message = "".join(message)

    message = list(chunkstring(message, 3))
    result = ''
    for k in message:
        result += chr(int(k))

    return(result)
    
