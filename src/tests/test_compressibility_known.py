import sage.all
from sage.graphs.digraph_generators import digraphs
from sage.graphs.digraph import DiGraph

import pytest

from src.homomorphism import compressibility_number


@pytest.mark.parametrize('n', list(range(2, 9)))
def test_path(n):
    G = digraphs.Path(n)
    assert compressibility_number(G) == n

@pytest.mark.parametrize('n', list(range(1, 8)))
def test_cycle(n):
    G = digraphs.Path(5)
    G.add_path(list(range(5, n + 5)))
    G.add_edges([(0, 5), (4, n + 4)])
    assert compressibility_number(G) == max(6, n + 1)

@pytest.mark.parametrize('n', list(range(1, 7)))
@pytest.mark.parametrize('m', list(range(1, 8)))
def test_cycle_bigger(n, m):
    G = digraphs.Path(6)
    G.add_path(list(range(6, n + 6)))
    G.add_path(list(range(n + 6, n + m + 6)))
    G.add_edges([(0, 6), (n + 6, 5), (n + m + 5, n + 5)])
    assert compressibility_number(G) == max(6, n + 1, m + 1)

@pytest.mark.parametrize('n', list(range(11, 16)))
def test_compressibility_big(n):
    G = digraphs.Path(n)
    assert compressibility_number(G) == -1