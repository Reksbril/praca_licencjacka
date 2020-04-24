import sage.all
from sage.graphs.digraph import DiGraph

import pytest

from src.helpers import *


@pytest.mark.parametrize("case", [
    (False, iter([])),
    (True, iter([1])),
    (False, iter([1, 2]))])
def test_iterator_has_exactly_one_element_false(case):
    assert case[0] == iterator_has_exactly_one_element(case[1])


@pytest.mark.parametrize("case", [
    (False, DiGraph([(0, 1), (1, 2), (0, 2), (1, 3), (2, 3)])), # brak cykli
    (True, DiGraph([(0, 1), (1, 2), (2, 0), (1, 3)])), # dokładnie jeden cykl
    (False, DiGraph([(0, 1), (1, 2), (2, 0), (1, 3), (3, 2)])) # więcej cykli
])
def test_has_one_cycle(case):
    assert case[0] == has_exactly_one_cycle(case[1])


def test_get_tournament_with_one_cycle():
    T = tournament_with_one_cycle(5, [True, False])
    assert T.is_tournament()
    assert has_exactly_one_cycle(T)

def test_tournament_with_one_cycle_last_source():
    T = tournament_with_one_cycle(5, [True, False])
    assert T.sources() == [4]

def test_tournament_with_one_cycle_last_sink():
    T = tournament_with_one_cycle(5, [False, True])
    assert T.sinks() == [4]

@pytest.mark.parametrize("k", [-1, 0, 1, 2])
def test_get_tournament_with_one_cycle_wrong_k(k):
    with pytest.raises(ValueError):
        tournament_with_one_cycle(k, [])


@pytest.mark.parametrize("dirs", [
    [],
    [True],
    [True, False, True],
])
def test_get_tournament_with_one_cycle_wrong_dirs(dirs):
    with pytest.raises(ValueError):
        tournament_with_one_cycle(5, dirs)


def test_rm_sources():
    T = tournament_with_one_cycle(6, [False, False, False])
    G = DiGraph([
        (5, 0), (6, 5), (6, 4), (7, 6), (7, 3), (7, 2)
    ])
    G.add_cycle([0, 1, 2, 3, 4])
    result = rm_sinks_and_sources(G, T)
    expected = DiGraph()
    expected.add_cycle([0, 1, 2, 3, 4])
    assert result == expected