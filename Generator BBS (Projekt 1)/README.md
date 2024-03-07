# Generator	 BBS
Generator BBS (Blum-Blum-Shub) to algorytm polegający na obliczaniu reszt kwadratowych modulo n. Pozwala	na	generowanie	kluczy	strumieniowych	o	określonej długości	 w	 sposób	 pseudolosowy.	 Podstawową	 trudność	 użycia	 algorytmu	 stanowi	 wyznaczenie liczby	Bluma,	 czyli	liczby	N=p*q, przy	 założeniu,	 że	 p	i	 q	to	odpowiednio	duże liczby	 pierwsze,	 przystające	 do	 3	 modulo	 4,	 od	 których	 zależy	 bezpieczeństwo	 i	 jakość	generatora.

## Rozwiązanie 
Rozwiązanie zostało zaimplementowane w języku Python (plik `main.py`, przy użyciu bibliotek `math` i `random`. Zaimplementowano również testy w celu sprawdzenia poprawności wygenerowanego losowego ciągu znaków.

### Informacja o implementacji
[Więcej informacji o implementacji](https://github.com/mr-SCWN/Podstawy-Kryptografii/blob/main/Generator%20BBS%20(Projekt%201)/Generatory_ciagow.pdf)
### Informacja o testach
[Więcej informacji o testach](https://github.com/mr-SCWN/Podstawy-Kryptografii/blob/main/Generator%20BBS%20(Projekt%201)/Testy.pdf)
### Przykładowe rozwiązanie 
![Przykładowe rozwiązanie](https://github.com/mr-SCWN/Podstawy-Kryptografii/assets/101336193/d2cbca58-2118-4f4a-935f-1c8bf42c9f88)
