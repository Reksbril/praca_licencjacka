import sage.all
from sage.graphs.digraph import DiGraph

'''
Plik zawierający funkcje pomocnicze
'''


def iterator_has_exactly_one_element(it):
    '''Zwraca True wtw it ma dokładnie jeden element.
    '''
    try:
        next(it)
    except StopIteration:  # 0 elementów
        return False
    try:
        next(it)
    except StopIteration:  # 1 element
        return True
    return False

def has_exactly_one_cycle(G):
    '''Zwraca True wtw G jest grafem skierowanym o dokładnie
    jednym cyklu skierowanym.
    '''
    if not G.is_directed():
        raise ValueError("G musi być grafem skierowanym")
    it = G.all_cycles_iterator(simple=True)
    return iterator_has_exactly_one_element(it)


def tournament_with_one_cycle(k, sink):
    '''Zwraca turniej z dokładnie jednym cyklem. Warto zauważyć
    że taki turniej będzie albo cyklem C_3, albo powstaje poprzez
    dodawanie do C_3 kolejnych wierzchołków, które w danym momencie
    będą źródłami bądź ujściami ([1], komentarz pod Algorytmem 2).

    Parameters
    ----------
    k : integer
        Liczba wierzchołków w turnieju
    dirs : boolean array
        Kontroluje, w jaki sposób mają być skierowane kolejne krawędzie.
        Jeżeli dirs[i] == True, to wszystkie krawędzie łączące wierzchołek
        i z wierzchołkami o niższych indeksach, będą skierowane w stronę i
        (tzn. i wtedy będzie ujściem).
        Rozmiar dirs powinien być równy k - 3

    Returns
    -------
    T : DiGraph
        Turniej o k wierzchołkach, zawierający dokładnie jeden cykl.
    '''
    if not isinstance(k, int) or k < 3:
        raise ValueError("k musi być liczbą naturalną większą lub równą 3")
    if len(sink) != k - 3:
        raise ValueError("Długość tablicy sink musi być równa k-3")

    T = DiGraph()
    T.add_cycle([0, 1, 2])

    def add_source(G, v):
        vertices = G.vertices()
        for u in vertices:
            G.add_edge(v, u)

    def add_sink(G, v):
        vertices = G.vertices()
        for u in vertices:
            G.add_edge(u, v)

    for i, flag in enumerate(sink):
        if flag:
            add_source(T, i + 3)
        else:
            add_sink(T, i + 3)

    return T


#TODO usunąć
def example_function():
    '''Opis

    Parameters
    ----------
    param1 : typ
        opis
    param2 : typ
        opis

    Returns
    -------
    return : typ
        opis
    '''
    pass