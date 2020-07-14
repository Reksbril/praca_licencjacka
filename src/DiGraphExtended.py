import sage.all
from sage.graphs.digraph import DiGraph
from copy import copy

class DiGraphExtended():
    '''Klasa odpowiedzialna za pamiętanie, które z wierzchołków
    kopii danego grafu skierowanego są ujściami, a które źródłami.
    Ponadto, pozwala na szybkie usuwanie źródeł i ujść z grafu, oraz
    działanie na kopii z usuniętymi wierzchołkami

    :param keep_removed: bool
        Kontroluje, czy pamiętać wierzchołki, które zostały usunięte.
        Potrzebna, jeżeli chcemy odtworzyć graf z usniętymi wierzchołkami.
    :param degrees: dict
        Słownik zawierający listy out_degree i in_degree dla G postaci:
        {'sink': <lista out_degree dla G>, 'source': <lista in_degree dla G>}
        Musi być zgodny ze stanem faktycznym. W przeciwnym przypadku metody
        klasy dadzą niepoprawne wyniki!
    :param vertices: dict
        Słownik zawierający listy ujść i źródeł G postaci:
        {'sink': <lista ujść>, 'source': <lista źródeł>}.
        Musi być zgodny ze stanem faktycznym. W przeciwnym przypadku metody
        klasy dadzą niepoprawne wyniki!
    '''

    def __init__(self, G, keep_removed = False, degrees = None, vertices = None):
        self.G = G
        if degrees is None:
            self.degrees = {
                'sink' : G.out_degree(labels=True),
                'source' : G.in_degree(labels=True)
            }
        else:
            self.degrees = degrees
        if vertices is None:
            self._vertices = {
                'sink' : G.sinks(),
                'source' : G.sources()
            }
        else:
            self._vertices = vertices
        self.keep_removed = keep_removed
        if keep_removed:
            self.removed = []
        self._neighbors_out = {}
        self._neighbors_in = {}
        self.G_neighbors_in = {}
        self.G_neighbors_out = {}

    def step(self, rm_type):
        '''Funkcja usuwająca, w zależności od parametry rm_type,
        źródła lub ujścia z kopii grafu G.

        :param rm_type: string
            Kontroluje, jaki rodzaj wierzchołków może być usunięty.
            * 'sink' - usuwa ujścia
            * 'source' - usuwa źródła
            w przeciwnym przypadku ValueError
        :return: array
            Tablica zawierająca, w zależności od 'rm_type', nowe źródła
            lub ujścia.
        '''

        if rm_type not in ['source', 'sink']:
            raise ValueError("rm_type musi być równy 'source' lub 'sink'.")

        if len(self._vertices[rm_type]) == 0:
            raise RuntimeError("Brak wierzchołków do usunięcia")

        other = 'sink' if rm_type == 'source' else 'source'
        result = []
        to_remove = self._vertices[rm_type]
        for v in self._vertices[rm_type]:
            for neigh in self._get_neighbors(rm_type, v):
                self.degrees[rm_type][neigh] -= 1
                if self.degrees[rm_type][neigh] == 0:
                    result.append(neigh)

        self._remove_duplicates(other, rm_type)
        self._vertices[rm_type] = result
        if self.keep_removed:
            self.removed += to_remove
        self._neighbors_out = {} # Po wykonaniu jakiejkolwiek modyfikacji, usuwa cache
        self._neighbors_in = {}
        return result

    def _remove_duplicates(self, rm_type, other):
        '''Usuwa wszystkie źródła jednocześnie będące ujściami (rm_type = 'source')
        lub odwrotnie (rm_type = 'sink'). other jest drugim z typów.
        '''
        self._vertices[rm_type] = list(
            set(self._vertices[rm_type]) - set(self._vertices[other]))

    def _get_neighbors(self, rm_type, v):
        '''W zależności od rm_type, zwraca wierzchołki wychodzące
        lub wchodzące do wierzchołka v.
        '''
        if rm_type == 'sink':
            if v not in self.G_neighbors_in:
                self.G_neighbors_in[v] = self.G.neighbors_in(v)
            return self.G_neighbors_in[v]
        else:
            if v not in self.G_neighbors_out:
                self.G_neighbors_out[v] = self.G.neighbors_out(v)
            return self.G_neighbors_out[v]

    def sources(self):
        return self._vertices['source']

    def sinks(self):
        return self._vertices['sink']

    def get_current(self):
        '''Zwraca kopię obecnego grafu jako DiGraph. Możliwe tylko jeżeli
        keep_removed = True
        '''
        if not self.keep_removed:
            raise ValueError("Nie można odtworzyć grafu jeżeli nie zostały "
                             "zapamiętane usunięte wierzchołki.")

        kept = list(set(self.G.vertices()) - set(self.removed))
        return self.G.subgraph(vertices=kept, inplace=False)

    def current_vertex_count(self):
        '''Zwraca liczbę wierzchołków, które pozostały w grafie. Możliwe tylko
        jeżeli keep_removed = True
        '''
        if not self.keep_removed:
            raise ValueError("Nie można odtworzyć grafu jeżeli nie zostały "
                             "zapamiętane usunięte wierzchołki.")

        return len(self.G.vertices()) - len(self.removed)

    def neighbors_out(self, v):
        '''Zwraca wierzchołki, do których prowadzą krawędzie wychodzące z v.
        '''
        if not self.keep_removed:
            raise ValueError("Nie można odtworzyć grafu jeżeli nie zostały "
                             "zapamiętane usunięte wierzchołki.")

        if v not in self._neighbors_out:
            self._neighbors_out[v] = list(set(self.G.neighbors_out(v)) - set(self.removed))
        return self._neighbors_out[v]

    def neighbors_in(self, v):
        '''Zwraca wierzchołki, z których prowadzą krawędzie wychodzące z v.
        '''
        if not self.keep_removed:
            raise ValueError("Nie można odtworzyć grafu jeżeli nie zostały "
                             "zapamiętane usunięte wierzchołki.")

        if v not in self._neighbors_in:
            self._neighbors_in[v] = list(set(self.G.neighbors_in(v)) - set(self.removed))
        return self._neighbors_in[v]

    def topological_sort(self):
        '''Zwraca listę wierzchołków posortowaną topologicznie.
        '''
        if not self.keep_removed:
            raise ValueError("Nie można odtworzyć grafu jeżeli nie zostały "
                             "zapamiętane usunięte wierzchołki.")

        sorted_G = self.G.topological_sort()
        for v in self.removed:
            sorted_G.remove(v)
        return sorted_G

    def vertices(self):
        return list(set(self.G.vertices()) - set(self.removed))