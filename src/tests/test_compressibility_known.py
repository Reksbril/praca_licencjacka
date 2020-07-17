import sage.all
from sage.graphs.digraph_generators import digraphs
from sage.graphs.digraph import DiGraph

import pytest

from src.homomorphism import compressibility_number


#7 - 198 ms, 8 - 2.8s, 9 - 1m 30s
@pytest.mark.parametrize('n', list(range(2, 9)))
def test_path(n):
    G = digraphs.Path(n)
    assert compressibility_number(G) == n

@pytest.mark.parametrize('n', list(range(1, 8)))
def test_cycle(n):
    G = digraphs.Path(5)
    G.add_path(list(range(5, n + 5)))
    G.add_edges([(0, 5), (4, n + 4)])
    print(G.edges())
    assert compressibility_number(G) == max(6, n + 1)