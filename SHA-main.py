# import library
import hashlib
 
# initialize a string
str = "www.MyTecBits.com"
 
# enkripsi
encoded_str = str.encode()
 
# create object
hash_obj = hashlib.sha1(encoded_str)
 
# konversi ke hexadecimal
hexa_value = hash_obj.hexdigest()
 
# print
print("\n", hexa_value, "\n")