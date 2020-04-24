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