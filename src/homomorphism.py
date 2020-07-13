import sage.all
from sage.graphs.digraph import DiGraph
from sage.graphs.connectivity import connected_components_subgraphs, is_connected

from src.helpers import *

from copy import deepcopy


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
    if not has_exactly_one_cycle_tournament(T) or not T.is_tournament():
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


def homomorphic_to_tournament(G, T):
    '''Funkcja sprawdzająca, czy G jest homomorficzny z dowolnym turniejem T. Jeżeli T ma mniej niż 2 cykle, powinniśmy
    używać powyżej zaimplementowanych metod
    :param G: Dowolny graf skierowany, acykliczny
    :param T: Dowolny turniej
    :return: True wtw G jest homomorficzny z T
    '''
    G, T = rm_sinks_and_sources(G, T, True)
    if len(T.vertices()) == 0:
        return len(G.vertices()) == 0
    sorted_G = G.topological_sort()

    def assign(i, A):
        if i == len(sorted_G) - 1:
            # W tym przypadku lista A[v] jest niepusta, więc istnieje dopasowanie dla v.
            return True
        v = sorted_G[i]
        for w in A[v]:
            #A_copy = deepcopy(A)
            A_prev = {}
            L = set(T.neighbors_out(w))
            for z in G.neighbors_out(v):
                #A_copy[z] = A_copy[z] & L
                A_prev[z] = A[z]
                A[z] = A[z] & L
                #if len(A_copy[z]) == 0:
                if len(A[z]) == 0:
                    for z in A_prev.keys():
                        A[z] = A_prev[z]
                    return False
            if assign(i + 1, A):
                return True
            for z in A_prev.keys():
                A[z] = A_prev[z]
        return False


    A = {v: set(T.vertices()) for v in G.vertices()}
    return assign(0, A)


def compressibility_number(G):
    '''Fukcja implementująca główny algrytm.
    :param G: Graf skierowany
    :return: Compressibility number dla G
    '''
    T = []
    i = homomorphic_to_transitive(G)
    T.append(transitive_tournament(i))

    def check_homomorphism(is_homomorphic_method, graphs_filter):
        nonlocal i
        nonlocal T
        while True:
            found_not_homomorphic = False
            T_next = []
            for H in digraphs.tournaments_nauty(i):
                if graphs_filter(H):
                    continue
                # Sprawdzamy, czy H zawiera którykolwiek z grafów w T
                if any(map(lambda x: all(H.has_edge(e) for e in x.edge_iterator()), T)):
                    continue
                if is_homomorphic_method(G, H):
                    T_next.append(H)
                else:
                    found_not_homomorphic = True
                    break
            if found_not_homomorphic:
                i += 1
                T = T + T_next
            else:
                break

    check_homomorphism(is_homomorphic_one_cycle, lambda H: not has_exactly_one_cycle_tournament(H))
    check_homomorphism(homomorphic_to_tournament, lambda H: has_exactly_one_cycle_tournament(H) or H.is_directed_acyclic())
    return i