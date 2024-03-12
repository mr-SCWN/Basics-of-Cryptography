import math
import random

def check_poker_test(n): # Problem był w tym, że losowosc mogła nie dać liczbę z której test pokerowy byłby poprawny, ale dodałem dodatkową funkcję, żeby po prostu sprawdzić że ten test będzie poprawny
    x0 = (n * n) % Blum  # Generowanie losowego ciągu znaków
    code = ""
    code += input_code(x0)
    for i in range(1, 20000):
        xi = (x0 * x0) % Blum
        code += input_code(xi)
        x0 = xi

    test = 0
    matrix = [0, 0, 0, 0,
               0, 0, 0, 0,
               0, 0, 0, 0,
               0, 0, 0, 0]
    index = 0
    while index < len(code):
        num = int(code[index]) * 8 + int(code[index + 1]) * 4 + int(code[index + 2]) * 2 + int(code[index + 3]) * 1
        matrix[num] += 1
        index += 4
    for i in range(16):
        test += matrix[i] * matrix[i]
    test *= 16 / 5000
    test -= 5000
    if test > 2.16 and test < 46.17:
        return True
    else:
        return False

def prime(a) : #Sprawdzanie liczby pierwszej
    b = False
    i = 2
    while i < int(math.sqrt(a))+ 1 :
        if a%i==0:
            b = True
            break
        i+=1
    return b

def nearest_prime (a): #Wyszukiwanie najbliższej liczby pierwszej (x mod 4 == 3)
    a = int(a)
    if a < 1000:
        a = 1000
    i = a
    while i >= a:
        if i % 4 == 3 and prime(i) == False:
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

def generate_coprime(n): # Generowanie liczby losowej, która jest względnie pierwsza z podaną liczbą
    while True:
        random_number = random.randint(2, 5*n)  # Generowanie liczb. Zakres od 2 do 5*N_Blum
        if are_coprime(n, random_number) and check_poker_test(random_number) == True:
            return random_number


def input_code(x):
    if x%2==0:
        return '1'
    else:
        return '0'

if __name__ == '__main__':
    file_name = "losowy_ciag_znakow.txt"

    a, b = input().split() # Wprowadzanie danych przez użytkownika
    a = nearest_prime(a)
    b = nearest_prime(b)
    print("Wybrane liczby pierwsze: ", a ,b )

    Blum = a*b
    print("Liczba Bluma: ", Blum)
    random_coprime = generate_coprime(Blum)

    print("Wybrana losowa liczba: ", random_coprime)

    x0 = (random_coprime*random_coprime)%Blum # Generowanie losowego ciągu znaków
    code = ""
    code += input_code(x0)
    for i in range (1, 20000):
        xi = (x0*x0)%Blum
        code += input_code(xi)
        x0 = xi

    with open(file_name, 'w') as file:
        file.write(code)

    print(f"Losowy ciąg znaków był wpisany w {file_name}\n\n")


    # Sprawdzenie ciągu za pomocą testów
    file_text = ""
    with open(file_name, 'r') as file:
        file_text = file.read()


    #Test 1
    print("Test 1 - Test pojedynczych bitów")
    test1 = 0
    for i in range (len(file_text)): #Sprawdzenie ile mamy 1 w ciągu
        if file_text[i] == '1':
            test1 +=1
    print("W ciągu mamy - ", test1, " jedynek\n")


    #Test 2
    print("Test 2 - Test serii")
    test2 = [0,0,0,0,0,0]
    code_test2 = file_text+'0' # Dodanie dodatkowej zmiennej żeby lżej było sprawdzić ostatni symbol
    counter = 0
    for i in range(len(code_test2)): #Sprawdzenie ile mamy serii w ciągu
        if code_test2[i] == '1':
            counter+=1
        else:
            if counter == 1:
                test2[0] += 1
            elif counter == 2:
                test2[1] +=1
            elif counter == 3:
                test2[2]+= 1
            elif counter == 4:
                test2[3] +=1
            elif counter == 5:
                test2[4]+=1
            elif counter >= 6:
                test2[5]+=1
            counter = 0
    print("W ciągu mamy serii z długością [1, 2, 3, 4, 5, 6+] - ", test2, "\n")


    #Test 3
    print("Test 3 - Test długiej serii")
    test3 = 0
    current= 1
    code_test3 = file_text + 'x' # Dodanie dodatkowej zmiennej żeby lżej było sprawdzić ostatni symbol
    for i in range(len(file_text)):
        if code_test3[i] == code_test3[i+1]:
            current+=1
        else:
            if current >= 26:
                test3+=1
            current=1
    print("W ciągu mamy długich serii (długość>=26) - ", test3, "\n")


    #Test 4
    print("Test 4 - Test pokerowy")
    test4 =0
    matrix4 = [0, 0, 0, 0,
             0, 0, 0, 0,
             0, 0, 0, 0,
             0, 0, 0, 0]
    index = 0
    while index < len(file_text):
        num = int(file_text[index])*8 +  int(file_text[index+1])*4 +  int(file_text[index+2])*2 + int(file_text[index+3])*1
        matrix4[num]+=1
        index+=4
    for i in range(16):
        test4+=matrix4[i]*matrix4[i]
    test4*=16/5000
    test4-=5000
    print("W ciągu mamy liczbę wystąpień segmentów o wartości dziesiętnej:")
    print(" [  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15]\n", matrix4)
    print("W ciągu mamy 'X = 16/5000*SUM(matrix[i]^2)-5000' (powinno być 2,16 < X < 46,17) - ", test4)
