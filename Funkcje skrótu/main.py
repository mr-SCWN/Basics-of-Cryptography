import hashlib
import os
import time


print("Wpisz frazę wejściową:", end=" ")
input_string = input()
bit_massive = []
print("Kod binarny: ", end="")
for i in range(len(input_string)):
    bit_massive.append(bin(ord(input_string[i]))[2:])
    print(bin(ord(input_string[i]))[2:], end=" ")
print("\n")

# Convert the string to bytes
input_bytes = input_string.encode()

# MD5
start_time = time.perf_counter()
hash_md5 = hashlib.md5(input_bytes).hexdigest()
end_time = time.perf_counter()
print('MD5:', hash_md5, "\nCzas:", (end_time - start_time) * 1000, "ms\n")

# SHA-1
start_time = time.perf_counter()
hash_sha1 = hashlib.sha1(input_bytes).hexdigest()
end_time = time.perf_counter()
print('SHA-1:', hash_sha1, "\nCzas:", (end_time - start_time) * 1000, "ms\n")

# SHA-256 (part of SHA-2 family)
start_time = time.perf_counter()
hash_sha256 = hashlib.sha256(input_bytes).hexdigest()
end_time = time.perf_counter()
print('SHA-256:', hash_sha256, "\nCzas:", (end_time - start_time) * 1000, "ms\n")

# SHA3-256 (part of SHA-3 family)
start_time = time.perf_counter()
hash_sha3_256 = hashlib.sha3_256(input_bytes).hexdigest()
end_time = time.perf_counter()
print('SHA3-256:', hash_sha3_256, "\nCzas:", (end_time - start_time) * 1000, "ms\n")

# SHA3-512(part of SHA-3 family)
start_time = time.perf_counter()
hash_sha3_512 = hashlib.sha3_512(input_bytes).hexdigest()
end_time = time.perf_counter()
print('SHA3-512:', hash_sha3_512, "\nCzas:", (end_time - start_time) * 1000, "ms\n\n\n")




# Wybrana funkcja skrótu: SHA-256
def hash_function(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()

data_samples = [str(n) for n in range(1000)]
hash_prefixes = [hash_function(data)[:3] for data in data_samples]

collisions = {}

for i, prefix in enumerate(hash_prefixes):
    if prefix not in collisions:
        collisions[prefix] = [data_samples[i]]
    else:
        collisions[prefix].append(data_samples[i])

collisions = {k: v for k, v in collisions.items() if len(v) > 1}

num_collisions = sum(len(v)-1 for v in collisions.values())
print(f"Liczba kolizji na pierwszych 12 bitach skrótu: {num_collisions}")
print("Przykłady kolizji:")
for k, v in list(collisions.items())[:5]:
    print(f"{k}: {v}")



# Wybrana funkcja skrótu: SHA-256
def sha256(input_bytes):
    return hashlib.sha256(input_bytes).digest()

def flip_bit(byte_array, bit_index):
    byte_index, bit_offset = divmod(bit_index, 8)
    flipped = byte_array[byte_index] ^ (1 << bit_offset)
    return byte_array[:byte_index] + bytes([flipped]) + byte_array[byte_index+1:]

def compare_hashes(original_hash, modified_hash):
    differences = 0
    for original_byte, modified_byte in zip(original_hash, modified_hash):
        differences += bin(original_byte ^ modified_byte).count('1')
    return differences

original_input = os.urandom(64)  # 512-bitowe losowe wejście
original_hash = sha256(original_input)

total_differences = 0
num_bits = len(original_input) * 8  # Liczba bitów wejściowych

for bit_index in range(num_bits):
    modified_input = flip_bit(original_input, bit_index)
    modified_hash = sha256(modified_input)
    differences = compare_hashes(original_hash, modified_hash)
    total_differences += differences

average_differences = total_differences / num_bits
print(f"\n\n\nŚrednia liczba zmienionych bitów: {average_differences}")
print(f"Prawdopodobieństwo:{average_differences/256}")
