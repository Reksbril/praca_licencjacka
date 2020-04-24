import sage.all
from sage.graphs.digraph_generators import digraphs

import pytest

from src.homomorphism import *


@pytest.mark.parametrize("k", range(1, 10))
def test_path_k_homomorphic_to_T_k(k):
    P = DiGraph()
    P.add_path(range(k))
    assert is_homomorphic_to_transitive_k(P, k)


@pytest.mark.parametrize("k", range(1, 10))
def test_path_k_not_homomorphic_to_lesser_T_k(k):
    P = DiGraph()
    P.add_path(range(k))
    assert not is_homomorphic_to_transitive_k(P, k - 1)


@pytest.mark.parametrize("k", range(5, 10))
@pytest.mark.parametrize("l", [-1, 0, 1])
def test_T_l_homomorphic_to_T_k(k, l):
    result = (l <= 0)
    l = k + l
    T = digraphs.TransitiveTournament(l)
    assert is_homomorphic_to_transitive_k(T, k) == result


def test_homomorphic_to_transitive():
    P = DiGraph()
    P.add_path(range(10))
    assert homomorphic_to_transitive(P) == 10

@pytest.mark.parametrize("T", [
    DiGraph([(0, 1), (1, 2), (2, 0), (1, 3)]), # nie jest turniejem
    digraphs.TransitiveTournament(4), # jest turniejem bez cykli
    DiGraph([(0, 1), (1, 2), (2, 0), (1, 3), (3, 2), (3, 0)]) # turniej z większą liczbą cykli
])
def test_one_cycle_wrong_T_argument(T):
    G = DiGraph(1)
    with pytest.raises(ValueError):
        is_homomorphic_one_cycle(G, T)

def test_one_cycle_G_homomorphic_to_G():
    #G = DiGraph([(0, 1), (1, 2), (2, 0)])
    #T = DiGraph([(0, 1), (1, 2), (2, 0)]) # G == T
    #assert is_homomorphic_one_cycle(G, T)
    pass
