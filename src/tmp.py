import sage.all
from sage.graphs.digraph_generators import digraphs
from homomorphism import compressibility_number

from time import time
G = digraphs.Path(10)
start = time()
c = compressibility_number(G)
leng = time() - start
print(leng)