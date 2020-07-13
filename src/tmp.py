import sage.all
from sage.graphs.digraph_generators import digraphs

for G in digraphs.tournaments_nauty(3):
    print(G.edges())