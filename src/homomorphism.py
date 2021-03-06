import sage.all
from sage.graphs.digraph import DiGraph
from sage.graphs.connectivity import \
    connected_components_subgraphs, is_connected

from src.helpers import *


class Homomorphism():
    '''Klasa pomocnicza, przechowująca metody sprawdzające różnego rodzaju
    homomorfizmy.
    '''

    def __init__(self, G):
        self.G = G
        self.degrees = {
            'sink': G.out_degree(labels=True),
            'source': G.in_degree(labels=True)
        }
        self._vertices = {
            'sink': G.sinks(),
            'source': G.sources()
        }

    def is_homomorphic_to_C_three(self, G=None):
        '''Sprawdza, czy graf G jest homomorficzny z C_3. G nie musi być
        spójny.

        :param G: DiGraph
            Graf, którego homomorfizm jest sprawdzany. Jeżeli G jest None, to
            sprawdzany jest homomorfizm z self.G
        '''
        if G is None:
            G = self.G

        for H in connected_components_subgraphs(G):
            if not self.connected_is_homomorphic_to_C_three(H):
                return False
        return True

    def connected_is_homomorphic_to_C_three(self, G=None):
        '''Sprawdza czy spójny G jest homomorficzny z C_3. Implementacja
        Algorytmu 1 z [1]

        :param G: DiGraph
            Graf, którego homomorfizm jest sprawdzany. Jeżeli G jest None, to
            sprawdzany jest homomorfizm z self.G
        '''
        if G is None:
            G = self.G

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

    def is_homomorphic_one_cycle(self, T):
        '''Sprawdza czy G jest homomorficzny z turniejem T.
        T musi zawierać dokładnie jeden cykl skierowany. W
        przeciwnym przypadku rzucany jest ValueError
        '''
        if not self.G.is_directed_acyclic():
            raise ValueError("G musi być skierowany i acykliczny.")
        if not has_exactly_one_cycle_tournament(T) or not T.is_tournament():
            raise ValueError("T musi być turniejem i zawierać dokładnie "
                             "jeden cykl skierowany.")

        G = rm_sinks_and_sources(self.G, T, G_vertices=self._vertices,
                                 G_degrees=self.degrees).get_current()
        # to co zostało, to pewien graf G, oraz T będący cyklem C_3
        return self.is_homomorphic_to_C_three(G)

    def is_homomorphic_to_transitive_k(self, k):
        '''Funkcja zwraca True wtw G jest homomorficzny z turniejem
        tranzytywnym na k wierzchołkach.
        '''
        if not self.G.is_directed_acyclic():
            raise ValueError("G musi być skierowany i acykliczny.")
        # krawędzie w T są skierowane od wierzchołka o mniejszym
        # indeksie do wierzchołka o większym indeksie
        colors = dict()  # kolory przyporządkowane wierzchołkom
        color = k  # obecny kolor
        vertices = self.G.sinks()  # wierzchołki, które w danym obrocie pętli
        # będą kolorowane
        ex = DiGraphExtended(self.G)

        while len(vertices) > 0 and color > 0:
            for v in vertices:
                # jeżeli wierzchołek ma już kolor, to sprzeczność
                if v in colors:
                    return False
                colors[v] = color
            color -= 1
            vertices = ex.step('sink')

        return len(colors) == len(self.G.vertices())

    def homomorphic_to_transitive(self):
        '''Funkcja która liczy najmniejsze k takie że G jest homomorficzny
        z turniejem tranzytywnym na k wierzchołkach.
        '''
        k = 1
        while True:
            if self.is_homomorphic_to_transitive_k(k):
                return k
            k += 1

    def homomorphic_to_tournament(self, T):
        '''Funkcja sprawdzająca, czy G jest homomorficzny z dowolnym turniejem
        T. Jeżeli T ma mniej niż 2 cykle, powinniśmy
        używać powyżej zaimplementowanych metod
        :param G: Dowolny graf skierowany, acykliczny
        :param T: Dowolny turniej
        :return: True wtw G jest homomorficzny z T
        '''
        G, T = rm_sinks_and_sources(self.G, T, True, G_vertices=self._vertices,
                                    G_degrees=self.degrees)
        if G.current_vertex_count() == 0:
            return True
        if T.current_vertex_count() == 0:
            return False
        sorted_G = G.topological_sort()

        def assign(i, A):
            if i == len(sorted_G) - 1:
                # W tym przypadku lista A[v] jest niepusta, więc istnieje
                # dopasowanie dla v.
                return True
            v = sorted_G[i]
            for w in A[v]:
                A_prev = {}
                L = set(T.neighbors_out(w))
                assignment_possible = True
                for z in G.neighbors_out(v):
                    A_prev[z] = A[z]
                    A[z] = A[z] & L
                    if len(A[z]) == 0:
                        for z in A_prev.keys():
                            A[z] = A_prev[z]
                        assignment_possible = False
                        break
                if assignment_possible and assign(i + 1, A):
                    return True
                for z in A_prev.keys():
                    A[z] = A_prev[z]
            return False

        A = {v: set(T.vertices()) for v in G.vertices()}
        return assign(0, A)


def compressibility_number(G, upper_bound=10):
    '''Fukcja implementująca główny algrytm.
    :param G:
        Graf skierowany
    :param upper_bound:
        Górna granica, powyżej której kompresyjność nie jest sprawdzana.
    :return:
        Kompresyjność dla G. Zwraca -1, jeżeli kompresyjność jest większa
        od `upper_bound`.
    '''
    homomorphism_helper = Homomorphism(G)

    T = []
    i = homomorphism_helper.homomorphic_to_transitive()
    T.append(transitive_tournament(i))

    def check_homomorphism(is_homomorphic_method, graphs_generator):
        nonlocal i
        nonlocal T
        nonlocal upper_bound
        while i <= upper_bound:
            found_not_homomorphic = False
            T_next = []
            for H in graphs_generator(i):
                # Sprawdzamy, czy H zawiera którykolwiek z grafów w T
                if any(map(lambda x:
                           all(H.has_edge(e) for e in x.edge_iterator()), T)):
                    continue
                if is_homomorphic_method(H):
                    if i < upper_bound:
                        T_next.append(H)
                else:
                    found_not_homomorphic = True
                    if i > 5:
                        break
            if found_not_homomorphic:
                i += 1
                T = T + T_next
            else:
                break

    check_homomorphism(homomorphism_helper.is_homomorphic_one_cycle,
                       lambda x: tournament_iterator(x, 'one_cycle'))
    check_homomorphism(homomorphism_helper.homomorphic_to_tournament,
                       lambda x: tournament_iterator(x, 'more_cycles'))
    return i if i <= upper_bound else -1
