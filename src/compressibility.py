import sage.all
from sage.graphs.digraph import DiGraph

import sys
import os
PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PATH + "/..")

from src.homomorphism import compressibility_number

if __name__ == '__main__':
    graph_dig6 = sys.argv[1]
    if len(sys.argv) == 3:
        upper_bound = sys.argv[2]
    digraph = DiGraph(graph_dig6, format="dig6")
    if len(sys.argv) == 3:
        compr = compressibility_number(digraph, upper_bound)
    else:
        compr = compressibility_number(digraph)
    print(compr)
