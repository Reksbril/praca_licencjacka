# Praca licencjacka

Implementacja algorytmu stanowiącego część pracy licencjackiej. 
Wykorzystuje bibliotekę [SAGE](http://doc.sagemath.org/html/en/index.html).

## Uruchamianie
Aby uruchomić wszystkie testy należy wywołać
```bash
./run_tests.sh "ścieżka do interpretera pythona biblioteki SageMath"
```

Stworzony jest również skrypt pozwalający na szybkie oblizenie kompresyjności dla dowolnego grafu w formacie *dig6*.
Można go użyć w pniższy sposób

```bash
./compressibility.sh "ścieżka do interpretera pythona biblioteki SageMath" "graf w formacie *dig6*" "górne ograniczenie na kompresyjność (opcjonalne, domyślnie=10)"
```

Ponadto w pliku *example.py* można znaleźć prosty przykład użycia zaimplementowanej funkcjonalności jako biblioteki.

## Układ
Katalog *src/* zawiera wszystkie pliki źródłowe, wraz z testami, które znajdują się w *src/tests/*. Katalog 
*tournaments/* zawiera wszystkie turnieje, które są używane w algorytmach. Można je wygenerować, uruchamiają skrypt
*generate_tournaments.sh*. Skrypt *run_tests.sh* pozwala zaś na uruchomienie wszystkich testów jednostkowych.

W katalogu *plots/* znajdują się wszystkie wykresy wykorzystane w pracy. 

Katalog *results/* zawiera wyniki eksperymentów, na których oparty jest ostatni dział pracy.
