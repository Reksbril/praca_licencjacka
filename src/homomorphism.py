import sage.all
from sage.graphs.digraph import DiGraph

from src.helpers import *


def is_homomorphic_one_cycle(G, T):
    '''Funkcja zwraca True wtw G jest homomorficzny z turniejem
    T. T musi zawierać dokładnie jeden cykl skierowany. W
    przeciwnym przypadku rzucany jest ValueError
    '''
    if not G.is_directed_acyclic():
        raise ValueError("G musi być skierowany i acykliczny.")
    if not has_exactly_one_cycle(T) or not T.is_tournament():
        raise ValueError("T musi być turniejem i zawierać dokładnie "
                         "jeden cykl skierowany.")
    pass


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
    out_degrees = G.out_degree(labels=True)

    while len(vertices) > 0 and color > 0:
        next_vertices = []
        for v in vertices:
            #jeżeli wierzchołek ma już kolor, to sprzeczność
            #TODO raczej nie będzie zachodzić, ale na razie zostawię
            if v in colors:
                return False
            colors[v] = color
            #bierzemy sąsiadów v, którzy po usunięciu v staną się "ujściami"
            for in_neigh in G.neighbors_in(v):
                out_degrees[in_neigh] -= 1
                if out_degrees[in_neigh] == 0:
                    next_vertices.append(in_neigh)
        color -= 1
        vertices = next_vertices

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
