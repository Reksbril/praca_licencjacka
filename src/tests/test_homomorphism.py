import sage.all
from sage.graphs.digraph_generators import digraphs

import pytest

from src.homomorphism import *


@pytest.mark.parametrize("k", range(1, 10))
def test_path_k_homomorphic_to_T_k(k):
    P = DiGraph()
    P.add_path(range(k))
    assert Homomorphism(P).is_homomorphic_to_transitive_k(k)


@pytest.mark.parametrize("k", range(1, 10))
def test_path_k_not_homomorphic_to_lesser_T_k(k):
    P = DiGraph()
    P.add_path(range(k))
    assert not Homomorphism(P).is_homomorphic_to_transitive_k(k - 1)


@pytest.mark.parametrize("k", range(5, 10))
@pytest.mark.parametrize("l", [-1, 0, 1])
def test_T_l_homomorphic_to_T_k(k, l):
    result = (l <= 0)
    l = k + l
    T = digraphs.TransitiveTournament(l)
    assert Homomorphism(T).is_homomorphic_to_transitive_k(k) == result


def test_homomorphic_to_transitive():
    P = DiGraph()
    P.add_path(range(10))
    assert Homomorphism(P).homomorphic_to_transitive() == 10


@pytest.mark.parametrize("T", [
    DiGraph([(0, 1), (1, 2), (2, 0), (1, 3)]),  # nie jest turniejem
    digraphs.TransitiveTournament(4),  # jest turniejem bez cykli
    DiGraph([(0, 1), (1, 2), (2, 0), (1, 3), (3, 2), (3, 0)])  # więcej cykli
])
def test_one_cycle_wrong_T_argument(T):
    G = DiGraph(1)
    with pytest.raises(ValueError):
        Homomorphism(G).is_homomorphic_one_cycle(T)


def test_homomorphic_to_C_three_simple():
    G = DiGraph([
        (0, 1), (1, 2),
        (3, 4), (4, 5)
    ], format='list_of_edges')
    assert Homomorphism(G).is_homomorphic_to_C_three()


def test_homomorphic_to_C_three_path():
    G = DiGraph()
    G.add_path(range(10))
    assert Homomorphism(G).is_homomorphic_to_C_three()


def test_not_homomorphic_to_C_three_simple():
    G = DiGraph([
        (0, 1), (1, 2), (0, 2)
    ], format='list_of_edges')
    assert not Homomorphism(G).is_homomorphic_to_C_three()


def test_homomorphic_to_T_one_cycle_simple():
    T = DiGraph([
        (1, 0), (2, 1), (0, 2),
        (0, 3), (1, 3), (2, 3),
        (4, 0), (4, 1), (4, 2), (4, 3)
    ], format='list_of_edges')
    G = DiGraph([
        (3, 5)
    ], format='list_of_edges')
    G.add_path([6, 0, 1, 2, 3, 4, 5])

    assert Homomorphism(G).is_homomorphic_one_cycle(T)


@pytest.mark.parametrize("case", [
    ([(0, 1), (1, 2),(3, 4), (4, 5)], True),
    ([(0, 1), (1, 2),(3, 4), (4, 5), (5, 6), (6, 7), (7, 8)], True),
    ([(0, 1), (1, 2), (0, 2)], False)
])
def test_homomorphic_to_tournament_C_three(case):
    G = DiGraph(case[0], format='list_of_edges')
    T = DiGraph([(0, 1), (1, 2), (2, 0)], format='list_of_edges')
    assert Homomorphism(G).homomorphic_to_tournament(T) == case[1]


def test_tree_homomorphic_to_tournaments():
    G = DiGraph([(0, 1), (1, 2), (1, 3), (0, 4), (4, 5), (6, 4),
                 (7, 6), (0, 8), (8, 9), (8, 10), (10, 11), (11, 12), (13, 7)],
                format='list_of_edges')
    for T in digraphs.tournaments_nauty(5):
        assert Homomorphism(G).homomorphic_to_tournament(T)


@pytest.mark.parametrize('k', [3, 4])
def test_tree_not_homomorphic_to_transitive(k):
    G = DiGraph([(0, 1), (1, 2), (1, 3), (0, 4), (4, 5), (6, 4),
                 (7, 6), (0, 8), (8, 9), (8, 10), (10, 11), (11, 12), (13, 7)],
                format='list_of_edges')
    T = digraphs.TransitiveTournament(k)
    assert not Homomorphism(G).homomorphic_to_tournament(T)


@pytest.mark.parametrize('edges', [
    [(0, 1), (1, 2), (1, 3), (0, 4), (4, 5), (6, 4), (7, 6), (0, 8), (8, 9),
     (8, 10), (10, 11), (11, 12), (13, 7)]
])
@pytest.mark.parametrize('expected', [5])
def test_compressibility(edges, expected):
    G = DiGraph(edges)
    assert compressibility_number(G) == expected


def test_homomorphic():
    G = DiGraph([(0, 1), (0, 2), (1, 2), (1, 3), (3, 4), (5, 4)])
    H = DiGraph([(0, 2), (0, 3), (1, 0), (2, 1), (3, 1), (3, 2)])
    assert Homomorphism(G).homomorphic_to_tournament(H)
