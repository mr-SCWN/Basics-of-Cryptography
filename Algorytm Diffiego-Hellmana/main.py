import random
from sympy import isprime, primitive_root

def generate_large_prime(length): #Generowanie liczby dużej ('lenghth' bit)
    while True:
        num = random.getrandbits(length)
        if isprime(num): #sprawdzenie że wygenerowana liczba jest pierwszą
            return num

def diffie_hellman():
    print("Wpisz ilosc bitów dla pierwszej liczby n:", end=" ")
    C = int(input())
    n = generate_large_prime(C) # wygenerowanie liczb: n (duża liczba pierwsza) i g (pierwiastek pierwotny modulo n)
    g = primitive_root(n)
    print("\nWygenerowaba liczba pierwsza: ", n)
    print("Wygenerowany pierwiastek pierwotny:", g, "\n")
    x = random.randrange(2, n - 1) # wybieramy losową liczbe całkowitą x i obliczamy klucz prywatny
    X = pow(g, x, n)

    y = random.randrange(2, n - 1) # wybieramy losową liczbe całkowitą y i obliczamy klucz prywatny
    Y = pow(g, y, n)

    print("Losowa liczba x = ", x, "\nklucz prywatny X: ", X)
    print("Losowa liczba y = " ,y, "\nKlucz prywatny Y: ", Y, "\n\n")

    k_A = pow(Y, x, n) # obliczamy kluczy sesyjne
    k_B = pow(X, y, n)

    print(f"Klucz sesji obliczony przez A: {k_A}")
    print(f"Klucz sesji obliczony przez B: {k_B}")
    if k_A == k_B:
        return True
    else:
        return False


if __name__ == '__main__':

    if diffie_hellman():
        print("\nPrawda: k_A == k_B")
    else:
        print("\nFałsz: k_A != k_B")