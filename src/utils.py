import random

def is_prime(number):
    #memeriksa apakah number merupakan bilangan prima atau bukan
    #input: sebuah big integer positif
    #output: True jika number prima, False jika tidak
    #asumsi number selalu valid

    if(number < 2):
        is_prime = False
    else:
        is_prime = True

    i = 2
    while((is_prime) and (i < number)):
        if(number % i == 0):
            is_prime = False
        else:
            i += 1
    
    return(is_prime)


def get_new_prime(size):
    #membangkitkan bilangan prima dengan ukuran size bits
    #input: ukuran bilangan dalam bit
    #output: sebuah bilangan prima size bits dengan MSB = 1
    #asumsi size selalu valid (> 0)

    upper_bound = (2**size)-1
    lower_bound = 2**(size-1)
    number = random.randint(lower_bound, upper_bound)
    while(not is_prime(number)):
        number = random.randint(lower_bound, upper_bound)
    
    return(number)

def gcd(a, b):
    #mencari nilai GCD dari a dan b
    #input: 2 bilangan positif
    #output: GCD 2 bilangan
    #asumsi input selalu valid

    if (b != 0):
        return gcd(b, a%b)
    else:
        return a

# Write file in write
def write_file(text, filename, mode):
    with open(filename, mode) as f:
        f.write(text)

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))