import sage.all
from sage.graphs.digraph import DiGraph
from sage.graphs.connectivity import connected_components_subgraphs, is_connected


from src.helpers import *


def is_homomorphic_to_C_three(G):
    '''Sprawdza, czy graf G jest homomorficzny z C_3. G nie musi być
    spójny.
    '''
    for H in connected_components_subgraphs(G):
        if not connected_is_homomorphic_to_C_three(H):
            return False
    return True

def connected_is_homomorphic_to_C_three(G):
    '''Sprawdza czy spójny G jest homomorficzny z C_3. Implementacja
    Algorytmu 1 z [1]
    '''
    if not is_connected(G):
        raise ValueError("G musi być grafem spójnym.")

    colors = {}

    def color(v, i):
        if v in colors:
            if colors[v] != i:
                return False
            else:
                return True

        colors[v] = i
        for w in G.neighbors_in(v):
            next_color = (i - 1) % 3
            if not color(w, next_color):
                return False

        for w in G.neighbors_out(v):
            next_color = (i + 1) % 3
            if not color(w, next_color):
                return False

        return True

    return color(G.vertices()[0], 0)


def is_homomorphic_one_cycle(G, T):
    '''Sprawdza czy G jest homomorficzny z turniejem T.
    T musi zawierać dokładnie jeden cykl skierowany. W
    przeciwnym przypadku rzucany jest ValueError
    '''
    if not G.is_directed_acyclic():
        raise ValueError("G musi być skierowany i acykliczny.")
    if not has_exactly_one_cycle(T) or not T.is_tournament():
        raise ValueError("T musi być turniejem i zawierać dokładnie "
                         "jeden cykl skierowany.")

    G = rm_sinks_and_sources(G, T)
    #to co zostało, to pewien graf G, oraz T będący cyklem C_3
    return is_homomorphic_to_C_three(G)


def is_homomorphic_to_transitive_k(G, k):
    '''Funkcja zwraca True wtw G jest homomorficzny z turniejem
    tranzytywnym na k wierzchołkach.
    '''
    if not G.is_directed_acyclic():
        raise ValueError("G musi być skierowany i acykliczny.")
    #krawędzie w T są skierowane od wierzchołka o mniejszym
    #indeksie do wierzchołka o większym indeksie
    colors = dict() #kolory przyporządkowane wierzchołkom
    color = k #obecny kolor
    vertices = G.sinks() #wierzchołki, które w danym obrocie pętli będą kolorowane
    ex = DiGraphExtended(G)

    while len(vertices) > 0 and color > 0:
        for v in vertices:
            #jeżeli wierzchołek ma już kolor, to sprzeczność
            #TODO raczej nie będzie zachodzić, ale na razie zostawię
            if v in colors:
                return False
            colors[v] = color
        color -= 1
        vertices = ex.step('sink')

    return len(colors) == len(G.vertices())


def homomorphic_to_transitive(G):
    '''Funkcja która liczy najmniejsze k takie że G jest homomorficzny
    z turniejem tranzytywnym na k wierzchołkach.
    '''
    k = 1
    while True:
        if is_homomorphic_to_transitive_k(G, k):
            return k
        k += 1
