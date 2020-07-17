import sage.all
from sage.graphs.digraph_generators import digraphs
from src.homomorphism import compressibility_number
'''
from time import time
G = digraphs.Path(10)
start = time()
c = compressibility_number(G)
leng = time() - start
print(leng)
'''

G = digraphs.Path(5)
G.add_path(list(range(5, 6)))
G.add_edges([(0, 5), (4, 5)])
print(G.edges())
assert compressibility_number(G) == 6