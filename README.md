# Praca licencjacka

Repozytorium implementacji algorytmu stanowiącego część pracy licencjackiej. 
Wykorzystuje bibliotekę [SAGE](http://doc.sagemath.org/html/en/index.html).

## Algorytm
Wejście: graf skierowany *G* \
Wyjście: compressibility number dla *G* tzn. najmniejsze *k* takie że *G* jest homomorficzny z każdym turniejem na *k* 
wierzchołkach

1. Szukamy *i* takiego że nasz graf jest homomorficzny z turniejem tranzytywnym na *i* wierzchołkach.
2. Zaczynając od *i*, szukamy najmniejszego *j* takiego, że *G* jest homomorficzny z turniejem na *j* wierzchołkach, 
który ma dokładnie jeden cykl skierowany.
3. Zaczynając od *j*, szukamy najmniejszego *k* takiego, że *G* jest homomorficzny z każdym turniejem


##### AD 1
Korzystamy z algorytmu 2 z [1].

#### AD 2
Wykorzystamy uwagę zamieszczoną pod opisem Algorytmu 2 w [1]. TODO: doprecyzować
Jednocześnie warto wykorzystać to, że jeżeli sprawdzany turniej zawiera w sobie turniej tranzytywny o *i* wierzchołkach,
to *G* jest z nim homomorficzny.

#### AD 3
Na razie trzeba będzie zrobić po prostu Brute-force. Jedyną rzeczą, jaką będziemy mogli wykorzystać jest fakt,
że jeżeli badany turniej zawiera turniej już sprawdzony wyżej, to mamy od razu homomorfizm.





# Bibliografia
[1] Hell, Pavol. (2020). Algorithmic aspects of graph homomorphisms. 
