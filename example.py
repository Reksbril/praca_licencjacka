import sage.all
from sage.graphs.digraph import DiGraph

from src.homomorphism import compressibility_number

if __name__ == '__main__':
    digraph = DiGraph("BKA", format="dig6")
    compr = compressibility_number(digraph, upper_bound=5)
    print(compr)
