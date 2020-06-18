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


def test_homomorphic_to_C_three_simple():
    G = DiGraph([
        (0, 1), (1, 2),
        (3, 4), (4, 5)
    ], format='list_of_edges')
    assert is_homomorphic_to_C_three(G)


def test_homomorphic_to_C_three_path():
    G = DiGraph()
    G.add_path(range(10))
    assert is_homomorphic_to_C_three(G)


def test_not_homomorphic_to_C_three_simple():
    G = DiGraph([
        (0, 1), (1, 2), (0, 2)
    ], format='list_of_edges')
    assert not is_homomorphic_to_C_three(G)


def test_homomorphic_to_T_one_cycle_simple():
    T = DiGraph([
        (0, 1), (1, 2), (2, 0),
        (0, 3), (1, 3), (2, 3),
        (4, 0), (4, 1), (4, 2), (4, 3)
    ], format='list_of_edges')
    G = DiGraph([
        (3, 5)
    ], format='list_of_edges')
    G.add_path([6, 0, 1, 2, 3, 4, 5])

    assert is_homomorphic_one_cycle(G, T)


@pytest.mark.parametrize("case", [
    ([(0, 1), (1, 2),(3, 4), (4, 5)], True),
    ([(0, 1), (1, 2),(3, 4), (4, 5), (5, 6), (6, 7), (7, 8)], True),
    ([(0, 1), (1, 2), (0, 2)], False)
])
def test_homomorphic_to_tournament_C_three(case):
    G = DiGraph(case[0], format='list_of_edges')
    T = DiGraph([(0, 1), (1, 2), (2, 0)], format='list_of_edges')
    assert homomorphic_to_tournament(G, T) == case[1]


def test_tree_homomorphic_to_tournaments():
    G = DiGraph([(0, 1), (1, 2), (1, 3), (0, 4), (4, 5), (6, 4),
                 (7, 6), (0, 8), (8, 9), (8, 10), (10, 11), (11, 12), (13, 7)],
                format='list_of_edges')
    for T in digraphs.tournaments_nauty(5):
        assert homomorphic_to_tournament(G, T)

@pytest.mark.parametrize('k', [3, 4])
def test_tree_not_homomorphic_to_transitive(k):
    G = DiGraph([(0, 1), (1, 2), (1, 3), (0, 4), (4, 5), (6, 4),
                 (7, 6), (0, 8), (8, 9), (8, 10), (10, 11), (11, 12), (13, 7)],
                format='list_of_edges')
    T = digraphs.TransitiveTournament(k)
    assert not homomorphic_to_tournament(G, T)


@pytest.mark.parametrize('edges', [
    [(0, 1), (1, 2), (1, 3), (0, 4), (4, 5), (6, 4), (7, 6), (0, 8), (8, 9), (8, 10), (10, 11), (11, 12), (13, 7)],
])
@pytest.mark.parametrize('expected', [5])
def test_compressibility(edges, expected):
    G = DiGraph(edges)
    assert compressibility_number(G) == expected
