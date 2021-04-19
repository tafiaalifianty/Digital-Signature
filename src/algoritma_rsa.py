import random
import binascii
import codecs

def convert(s): # Convert string to ASCII
    return ([ord(c) for c in s])

def gcd(a, b):
    if (b != 0):
        return gcd(b, a%b)
    else:
        return a

def modulusInverse(a, b):
    for x in range(1, b):
        if (a * x) % b == 1:
            return x
    return -1

def fastModulusInverse(a, b):
    return fast(a, b-2, b)

def fast(x, y, z):
    result = 1
    while y > 0:
        if y % 2 == 1:
            result = (result * x) % z
        y = y // 2
        x = (x * x) % z
    return result


def isPrime(x):
    flag = True
    if (x <= 1):
        flag = False
    # 2 and 3 are prime
    elif (x >= 4):
        if (x % 2 == 0 or x % 3 == 0):
            flag = False    # x is not prime
        else: 
            j = int(pow(x, 1/2)) + 1
            for i in range (5, j, 6):
                if (x % i == 0 or x % (i+2) == 0):
                    flag = False    # x is not prime
                    break
    return flag
    

def generateKey(p, q):
    # calculate n
    n = p * q

    # totient of n = (p-1)(q-1)
    t = (p-1)*(q-1)

    # choose a number as public key
    publicKey = random.randrange(1, t)

    # check if publicKey is coprime with t
    c = gcd(publicKey,t)
    while c != 1:
        publicKey = random.randrange(1,t)
        c = gcd (publicKey,t)
    
    # create private key
    privateKey = modulusInverse(publicKey, t)

    # return public and private key
    return ((publicKey, n) , (privateKey, n))


def encrypt(key, message, mode):
    publicKey, n = key
    result = []

    if(mode == '1'): #input text
        for i in message:
            cipher = pow(ord(i), publicKey, n)
            result.append(hex(cipher))

    else: #file
        for i in message:
            print(i)
            cipher = pow(i, publicKey, n)
            result.append("%02X" % cipher)  # cipher format in 2-digit hex as string
        result = codecs.decode(''.join(result), 'hex_codec').decode('latin-1')

    return result
    

def decrypt(key, message, mode):
    privateKey, n = key
    result = []

    if(mode == '1'): #input text
        for i in message:
            plain = (int(i, 16) for i in message)   # convert i from base 16 to base 10
        for j in plain:
            p = pow(j, privateKey, n)
            result.append(p)
            
    else: #file
        for i in message:
            cipher = pow(i, privateKey, n)
            result.append("%02X" % cipher)  # cipher format in 2-digit hex as string
        result = codecs.decode(''.join(result), 'hex_codec').decode('latin-1')
    
    return result


'''
if __name__ == '__main__':

    p = int(input(" Enter p (must a prime number): "))
    q = int(input(" Enter q (must a prime number): "))

    public, private = generateKey(p, q)

    print(" *** Your public key is ", public, " and your private key is ", private)

    message = input(" Enter a message (plaintext): ")
    encrypted_msg = encrypt(public, message)
    
    print(" Your plaintext: ", message)
    print(" Your message in ASCII", convert(message))
    print(" Your encrypted message in hexadecimal is: ", (encrypted_msg))
    

    print(" Decrypting message with private key ", private, " . . .")

    decrypted_msg = decrypt(private,encrypted_msg)
    print(" Your message in ASCII is: ", decrypted_msg)
    print(" Your message: ", ''.join(chr(i) for i in decrypted_msg))

# p sama q paling ngga >= 11 (?)
# n gabisa kurang dari ASCII plaintext
'''