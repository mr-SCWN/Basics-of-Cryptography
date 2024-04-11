import os
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# Definicje rozmiarów plików i trybów
file_sizes = [1024*1000, 1024 * 10000, 1024 * 100000]  # na przykład: 1000KB, 10000KB, 100000KB
modes_list = [modes.ECB(), modes.CBC(os.urandom(16)), modes.OFB(os.urandom(16)),
              modes.CFB(os.urandom(16)), modes.CTR(os.urandom(16))]

# Funkcja do szyfrowania i deszyfrowania
def encrypt_decrypt(mode, data):
    # Generowanie klucza i inicjalizacja szyfrowania
    key = os.urandom(32)  # Długość klucza 256 bitów
    cipher = Cipher(algorithms.AES(key), mode, backend=default_backend())
    encryptor = cipher.encryptor()
    decryptor = cipher.decryptor()

    # Szyfrowanie danych
    start_time = time.time()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    encrypt_time = time.time() - start_time

    # Deszyfrowanie danych
    start_time = time.time()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    decrypt_time = time.time() - start_time

    return encrypt_time, decrypt_time


# Przeprowadzenie testów
for size in file_sizes:
    data = os.urandom(size)
    print(f"Testowanie rozmiaru pliku: {size} bajtów")
    for mode in modes_list:
        mode_name = type(mode).__name__
        encrypt_time, decrypt_time = encrypt_decrypt(mode, data)
        print(f"Tryb: {mode_name} - Czas szyfrowania: {encrypt_time:.6f} s, Czas deszyfrowania: {decrypt_time:.6f} s")


# Analiza propagacji błędów w różnych trybach pracy
print("\n\n\n\nAnaliza propagacji błędów")

def simulate_error_in_ciphertext(ciphertext: bytes, error_position: int) -> bytes:
    """
    Symuluje błąd w szyfrogramie poprzez odwrócenie bitu na określonej pozycji.
    """
    error_byte_array = bytearray(ciphertext)
    # Upewnij się, że pozycja błędu jest w zakresie długości szyfrogramu
    if error_position < len(error_byte_array):
        error_byte_array[error_position] ^= 1  # Odwrócenie bitu na wybranej pozycji
    return bytes(error_byte_array)


def add_padding(data: bytes, block_size: int) -> bytes:
    """
    Dodaje dopełnienie do danych, aby ich długość była wielokrotnością wielkości bloku.
    """
    padder = padding.PKCS7(block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data


def remove_padding(data: bytes, block_size: int) -> bytes:
    """
    Usuwa dopełnienie z danych po deszyfrowaniu.
    """
    unpadder = padding.PKCS7(block_size).unpadder()
    unpadded_data = unpadder.update(data) + unpadder.finalize()
    return unpadded_data


def encrypt_decrypt_with_error(mode: modes.Mode, backend, key: bytes, data: bytes, iv: bytes = None) -> tuple:
    """
    Szyfruje dane, wprowadza błąd do szyfrogramu, a następnie deszyfruje dane, zwracając oryginalne dane, szyfrogram i odszyfrowane dane.
    """
    block_size = algorithms.AES.block_size
    padded_data = add_padding(data, block_size)

    cipher = Cipher(algorithms.AES(key), mode, backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Wprowadzenie błędu do szyfrogramu
    error_ciphertext = simulate_error_in_ciphertext(ciphertext, 10)  # Błąd wprowadzony na 10 pozycji

    decryptor = cipher.decryptor()
    decrypted_padded_data_with_error = decryptor.update(error_ciphertext) + decryptor.finalize()
    decrypted_data_with_error = remove_padding(decrypted_padded_data_with_error, block_size)

    return data, ciphertext, decrypted_data_with_error


def demonstrate_error_propagation(data: bytes):
    """
    Demonstruje propagację błędu w różnych trybach pracy algorytmu szyfrowania.
    """
    key = os.urandom(32)
    iv = os.urandom(16)
    backend = default_backend()

    modes_list = [
        modes.ECB(),
        modes.CBC(iv),
        modes.OFB(iv),
        modes.CFB(iv),
        modes.CTR(iv)
    ]

    for mode in modes_list:
        mode_name = type(mode).__name__
        original_data, ciphertext, decrypted_data_with_error = encrypt_decrypt_with_error(mode, backend, key, data, iv)

        print(f"Tryb: {mode_name}")
        print(f"Wiadomosć wejsciowa: {original_data}\n")
        print(f"Tekst zaszyfrowany (z błędem): {bytes(ciphertext[:20])}...")  # Pokazuje fragment szyfrogramu
        print(f"Wiadomosć wyjsciowa (z błędem): {decrypted_data_with_error}\n\n\n")


data = b"This is a test message for encryption"
demonstrate_error_propagation(data)




# Pomocnicza funkcja do wykonania operacji XOR na dwóch blokach danych
def xor_blocks(block1, block2):
    return bytes(a ^ b for a, b in zip(block1, block2))

# Zmodyfikowana funkcja szyfrowania i deszyfrowania dla trybu CBC używającego ECB
def encrypt_decrypt_cbc_ecb(key, data, iv):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend)
    block_size = algorithms.AES.block_size // 8  # Wielkość bloku w bajtach

    # Dodanie dopełnienia do danych, aby ich długość była wielokrotnością wielkości bloku
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    data = padder.update(data) + padder.finalize()

    encrypted_data = b''
    previous_block = iv

    # Szyfrowanie blok po bloku
    for i in range(0, len(data), block_size):
        # XOR danych z poprzednim zaszyfrowanym blokiem (lub IV dla pierwszego bloku)
        block = xor_blocks(data[i:i + block_size], previous_block)
        encryptor = cipher.encryptor()
        encrypted_block = encryptor.update(block) + encryptor.finalize()
        encrypted_data += encrypted_block
        previous_block = encrypted_block

    # Deszyfrowanie również wymaga użycia ECB i operacji XOR, ale w odwrotnej kolejności
    decrypted_data = b''
    previous_block = iv

    for i in range(0, len(encrypted_data), block_size):
        decryptor = cipher.decryptor()
        decrypted_block = decryptor.update(encrypted_data[i:i + block_size]) + decryptor.finalize()
        decrypted_block = xor_blocks(decrypted_block, previous_block)
        previous_block = encrypted_data[i:i + block_size]
        decrypted_data += decrypted_block

    # Usunięcie dopełnienia z odszyfrowanych danych
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return encrypted_data, decrypted_data

print("\n\n\n")
key = os.urandom(32)  # AES-256
iv = os.urandom(16)  # Wielkość bloku AES to 128 bitów
data = b"Przykladowe dane do zaszyfrowania"
print("Dane do zaszyfrowania: ", data)
encrypted_data, decrypted_data = encrypt_decrypt_cbc_ecb(key, data, iv)
print("Zaszyfrowane dane:", encrypted_data)
print("Odszyfrowane dane:", decrypted_data)