import hashlib

print("Wpisz frazę wejsciową:" , end=" ")
input_string = input()
bit_massive = []
print ("Kod binarny: ", end="")
for i in range(len(input_string)):
    bit_massive.append(bin(ord(input_string[i]))[2:])
    print(bin(ord(input_string[i]))[2:], end=" ")
print("\n")


# Convert the string to bytes
input_bytes = input_string.encode()
# MD5
hash_md5 = hashlib.md5(input_bytes).hexdigest()
print('MD5:', hash_md5)

# SHA-1
hash_sha1 = hashlib.sha1(input_bytes).hexdigest()
print('SHA-1:', hash_sha1)

# SHA-256 (part of SHA-2 family)
hash_sha256 = hashlib.sha256(input_bytes).hexdigest()
print('SHA-256:', hash_sha256)

# SHA3-256 (part of SHA-3 family)
hash_sha3_256 = hashlib.sha3_256(input_bytes).hexdigest()
print('SHA3-256:', hash_sha3_256)