# Praca licencjacka

Implementacja algorytmu stanowiącego część pracy licencjackiej. 
Wykorzystuje bibliotekę [SAGE](http://doc.sagemath.org/html/en/index.html).

## Wymagania wstępne
- Biblioteka SAGE: [instalacja](https://doc.sagemath.org/html/en/installation/index.html)
- Katalog *tournaments* zawierający turnieje wykorzystywane w obliczeniach. Jeżeli nie został załączony wraz z kodem źródłowym, można go [pobrać](https://drive.google.com/drive/folders/1Ps4IXg8G11cDnriiiM0vPeOMaGugExiD?usp=sharing) lub wygenerować za pomocą poniższego skryptu
```bash
./generate_tournaments.sh "ścieżka do interpretera pythona biblioteki SageMath"
```


## Uruchamianie
Aby uruchomić wszystkie testy należy wywołać
```bash
./run_tests.sh "ścieżka do interpretera pythona biblioteki SageMath"
```

Stworzony jest również skrypt pozwalający na obliczenie kompresyjności dla dowolnego grafu w formacie *dig6*.
Można go użyć w poniższy sposób

```bash
./compressibility.sh "ścieżka do interpretera pythona biblioteki SageMath" "graf w formacie *dig6*" "górne ograniczenie na kompresyjność (opcjonalne, domyślnie=10)"
```

Ponadto w pliku *example.py* można znaleźć prosty przykład użycia zaimplementowanej funkcjonalności jako biblioteki.


## Układ
W katalogu *src/* znajduje się kod źródłowy implementacji oraz testy jednostkowe. Ponadto można tam znaleźć skrypt wykorzystany przy eksperymentach (*experiments.py*) oraz wszystkie pozostałe skrypty pomocnicze.

W trakcie eksperymentów generowane są katalogi *results/* oraz *plots/*. Ten pierwszy zawiera listę grafów wraz z obliczonymi dla nich kompresyjnościami (dokładny opis znajduje się w *experiments_helpers.py*). 
Drugi z nich zawiera wygenerowane wykresy.
