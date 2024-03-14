import math
import random

def prime(a) : #Sprawdzanie liczby pierwszej
    b = True
    i = 2
    while i < int(math.sqrt(a))+ 1 :
        if a%i==0:
            b = False
            break
        i+=1
    return b

def nearest_prime (a): #Wyszukiwanie najbliższej liczby pierwszej
    a = int(a)
    if a < 1000:
        a = 1000
    i = a
    while i >= a:
        if prime(i) == True:
            break
        else:
            i += 1
    return i

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def are_coprime(a, b): #Funkcja sprawdzająca, czy liczby są względnie pierwsze
    return gcd(a, b) == 1

def generate_coprime(phi): # Generowanie liczby losowej, która jest względnie pierwsza z podaną liczbą
    while True:
        random_number = random.randint(5, 2*phi)  # Generowanie liczb. Zakres od 2 do 5*phi
        if are_coprime(phi, random_number)==True and prime(random_number)==True:
            return random_number


def generate_private(phi , e):
    while True:
        random_number = random.randint(2, 5*phi)
        if (e*random_number)%phi==1:
            return random_number



if __name__ == '__main__':
    p, q = input().split()  # Wprowadzanie danych przez użytkownika
    p = nearest_prime(p)
    q = nearest_prime(q)
    print("Wybrane liczby pierwsze: ", p, q, '\n') # Znalezinie najblizszych liczb pierwszych (p i q)
    n = p*q
    phi = (p-1)*(q-1)
    e = generate_coprime(phi)
    print("Klucz publiczny: e = ", e, "     n = ", n)
    d = generate_private(phi , e)
    print("Klucz prywatny: d = ", d, "     n = ", n)

    print("\n\n         Szyfrowanie wiadomosci:")
    print("Wpisz wiadomosc: m (m < n) = ", end="") # m - message (wiadomosc)
    m = int(input())
    c = pow (m , e ,n) #pow(base, exp, mod)
    print("Szyfrowana wiadomosc: c = " , c)


    print("\n\n         Deszyfrowanie wiadomosci:")
    print("Szyfrowana wiadomosc: c = ", c) # c - encrypted message (wiadomość zaszyfrowana)
    m_new = pow (c, d, n)
    print("Deszyfrowana wiadomosc: m_new = ", m_new)

    print("\nJeżeli m == m_new, to oznacza że szyfrowanie i deszyfrowanie były poprawne zrobione:")
    print("m = ", m, ", m_new = ", m_new, " - ", end="")
    if m_new == m:
        print("Prawda")
    else:
        print("Falsz")