import sage.all
from sage.graphs.digraph import DiGraph
from sage.graphs.digraph_generators import digraphs

from src.DiGraphExtended import DiGraphExtended

'''
Plik zawierający funkcje pomocnicze
'''


def iterator_has_exactly_one_element(it):
    '''Zwraca True wtw iterator it ma dokładnie jeden element.
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


def has_exactly_one_cycle_tournament(G):
    '''Zwraca True wtw G jest turniejem skierowanym o dokładnie
    jednym cyklu skierowanym.
    '''
    if not G.is_directed():
        raise ValueError("G musi być grafem skierowanym")
    for edge in [(1, 0), (2, 1), (0, 2)]:
        if not G.has_edge(edge):
            return False
    G_ex = DiGraphExtended(G, keep_removed=True)
    while True:
        if len(G_ex.sinks()) > 0:
            G_ex.step("sink")
        elif len(G_ex.sources()) > 0:
            G_ex.step("source")
        else:
            break
    return G_ex.current_vertex_count() == 3

def tournament_with_one_cycle(k, sink):
    '''Zwraca turniej z dokładnie jednym cyklem. Warto zauważyć
    że taki turniej będzie albo cyklem C_3, albo powstaje poprzez
    dodawanie do C_3 kolejnych wierzchołków, które w danym momencie
    będą źródłami bądź ujściami ([1], komentarz pod Algorytmem 2).

    :param k: Int
        Liczba wierzchołków w turnieju
    :param sink: Bool array
        Kontroluje, w jaki sposób mają być skierowane kolejne krawędzie.
        Jeżeli dirs[i] == True, to wszystkie krawędzie łączące wierzchołek
        i z wierzchołkami o niższych indeksach, będą skierowane w stronę i
        (tzn. i wtedy będzie ujściem).
        Rozmiar dirs powinien być równy k - 3
    :return: DiGraph
        Turniej o k wierzchołkach, zawierający dokładnie jeden cykl.
    '''
    if not isinstance(k, int) or k < 3:
        raise ValueError("k musi być liczbą naturalną większą lub równą 3")
    if len(sink) != k - 3:
        raise ValueError("Długość tablicy sink musi być równa k-3")

    T = DiGraph()
    T.add_cycle([0, 2, 1])

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
            add_sink(T, i + 3)
        else:
            add_source(T, i + 3)

    return T


def rm_sinks_and_sources(G, T, keep_T = False, G_degrees = None, G_vertices = None):
    '''Zwraca kopię grafu G jako DiGraphExtended, która ma
    usunięte wszystkie źródła i ujścia, zgodnie z uwagą pod Algorytmem 2 w [1].

    :param keep_T: Jeżeli jest True, to funkcja zwraca również
    graf T, który został pozbawiony źródeł i ujść.
    :param G_degrees: dict
        Słownik zawierający listy out_degree i in_degree dla G postaci:
        {'sink': <lista out_degree dla G>, 'source': <lista in_degree dla G>}
        Musi być zgodny ze stanem faktycznym. W przeciwnym przypadku funkcja
        da niepoprawny wynik!
    :param G_vertices: dict
        Słownik zawierający listy ujść i źródeł G postaci:
        {'sink': <lista ujść>, 'source': <lista źródeł>}.
        Musi być zgodny ze stanem faktycznym. W przeciwnym przypadku funkcja
        da niepoprawny wynik!
    '''

    exG = DiGraphExtended(G, keep_removed=True, degrees=G_degrees, vertices=G_vertices)
    exT = DiGraphExtended(T, keep_removed=keep_T)

    while True:
        if len(exT.sources()) > 0:
            next_step = 'source'
        elif len(exT.sinks()) > 0:
            next_step = 'sink'
        else:
            if keep_T:
                return exG, exT
            else:
                return exG

        exT.step(next_step)
        try:
            exG.step(next_step)
        except RuntimeError:
            pass

def transitive_tournament(n):
    '''Zwraca turniej tranzytywny, którego krawędzie są sierowane od
    wierzchołka o większym indeksie, do tego o większym.

    :param n: Rozmiar turnieju
    :return: Turniej tranzytywny
    '''
    edges = [(j, i) for j in range(0, n) for i in range(0, j)]
    return DiGraph(edges)
