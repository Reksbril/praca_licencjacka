import sage.all
from sage.graphs.digraph_generators import digraphs
from src.homomorphism import compressibility_number

G = digraphs.Path(8)
assert compressibility_number(G) == 8