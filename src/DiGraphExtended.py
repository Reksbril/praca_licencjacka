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
    '''

    def __init__(self, G, keep_removed = False):
        self.G = G
        self.degrees = {
            'sink' : G.out_degree(labels=True),
            'source' : G.in_degree(labels=True)
        }
        self.vertices = {
            'sink' : G.sinks(),
            'source' : G.sources()
        }
        self.keep_removed = keep_removed
        if keep_removed:
            self.removed = []

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

        if len(self.vertices[rm_type]) == 0:
            raise RuntimeError("Brak wierzchołków do usunięcia")

        other = 'sink' if rm_type == 'source' else 'source'
        result = []
        to_remove = self.vertices[rm_type]
        for v in self.vertices[rm_type]:
            for neigh in self._get_neighbors(rm_type, v):
                self.degrees[rm_type][neigh] -= 1
                if self.degrees[rm_type][neigh] == 0:
                    result.append(neigh)

        self._remove_duplicates(other, rm_type)
        self.vertices[rm_type] = result
        if self.keep_removed:
            self.removed += to_remove
        return result

    def _remove_duplicates(self, rm_type, other):
        '''Usuwa wszystkie źródła jednocześnie będące ujściami (rm_type = 'source')
        lub odwrotnie (rm_type = 'sink'). other jest drugim z typów.
        '''
        self.vertices[rm_type] = list(
            set(self.vertices[rm_type]) - set(self.vertices[other]))

    def _get_neighbors(self, rm_type, v):
        '''W zależności od rm_type, zwraca wierzchołki wychodzące
        lub wchodzące do wierzchołka v.
        '''
        if rm_type == 'sink':
            return self.G.neighbors_in(v)
        else:
            return self.G.neighbors_out(v)

    def sources(self):
        return self.vertices['source']

    def sinks(self):
        return self.vertices['sink']

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
        '''Zwraca wierzchołki, do których prowadzą krawędzi wychodzące z v.
        '''
        return list(set(self.G.neighbors_out(v)) - set(self.removed))