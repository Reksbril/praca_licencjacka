import sage.all
from sage.graphs.digraph_generators import digraphs
from src.homomorphism import compressibility_number


from time import time

def path():
    G = digraphs.Path(10)
    start = time()
    c = compressibility_number(G)
    leng = time() - start
    print(leng)

def cycle():
    G = digraphs.Path(6)
    G.add_path(list(range(6, 12)))
    G.add_path(list(range(12, 19)))
    G.add_edges([(0, 6), (12, 5), (18, 11)])
    assert compressibility_number(G) == 8

path()