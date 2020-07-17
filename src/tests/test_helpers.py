import sage.all
from sage.graphs.digraph import DiGraph

import pytest
from collections import Counter

from src.helpers import *


@pytest.mark.parametrize("case", [
    (False, iter([])),
    (True, iter([1])),
    (False, iter([1, 2]))])
def test_iterator_has_exactly_one_element_false(case):
    assert case[0] == iterator_has_exactly_one_element(case[1])


@pytest.mark.parametrize("case", [
    (False, DiGraph([(0, 1), (1, 2), (0, 2), (1, 3), (2, 3)])), # brak cykli
    (True, DiGraph([(1, 0), (2, 1), (0, 2), (1, 3)])), # dokładnie jeden cykl
    (False, DiGraph([(0, 1), (1, 2), (2, 0), (1, 3), (3, 2)])) # więcej cykli
])
def test_has_one_cycle(case):
    assert case[0] == has_exactly_one_cycle_tournament(case[1])


def test_get_tournament_with_one_cycle():
    T = tournament_with_one_cycle(5, [True, False])
    assert T.is_tournament()
    assert has_exactly_one_cycle_tournament(T)

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
    result = rm_sinks_and_sources(G, T).get_current()
    expected = DiGraph()
    expected.add_cycle([0, 1, 2, 3, 4])
    assert result == expected


def test_rm_sources_less_than_in_T():
    T = tournament_with_one_cycle(6, [False, False, False])
    G = DiGraph()
    G.add_cycle([0, 1, 2, 3, 4])
    result = rm_sinks_and_sources(G, T).get_current()
    expected = DiGraph()
    expected.add_cycle([0, 1, 2, 3, 4])
    assert result == expected


def test_rm_sources_tournament():
    T = tournament_with_one_cycle(6, [False, False, False])
    G = DiGraph()
    G.add_cycle([0, 1, 2, 3, 4])
    _, result = rm_sinks_and_sources(G, T, True)
    result = result.get_current()
    expected = DiGraph()
    expected.add_cycle([0, 2, 1])
    assert result == expected

def test_rm_sinks_sources_complex():
    G = digraphs.Path(5)
    G.add_path(list(range(5, 6)))
    G.add_edges([(0, 5), (4, 5)])
    T = DiGraph([(1, 0), (2, 0), (2, 1), (2, 4), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1),
                 (4, 3), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4)])
    G, T = rm_sinks_and_sources(G, T, keep_T=True)
    assert set(G.removed) == set([0, 4, 5])
    assert set(T.removed) == set([0, 1, 5])


def test_rm_sinks_sources_keep_dicts():
    G = digraphs.Path(5)
    G.add_path(list(range(5, 6)))
    G.add_edges([(0, 5), (4, 5)])
    T = DiGraph([(1, 0), (2, 0), (2, 1), (2, 4), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1),
                 (4, 3), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4)])
    degrees = {
        'sink' : G.out_degree(labels=True),
        'source' : G.in_degree(labels=True)
    }
    vertices = {
        'sink': G.sinks(),
        'source': G.sources()
    }
    rm_sinks_and_sources(G, T, keep_T=True, G_degrees=degrees, G_vertices=vertices)
    assert degrees['sink'] == G.out_degree(labels=True)
    assert degrees['source'] == G.in_degree(labels=True)
    assert vertices['sink'] == G.sinks()
    assert vertices['source'] == G.sources()

def test_rm_sinks_and_sources_double_remove():
    G = DiGraph([(0, 1), (0, 6), (1, 2), (2, 3), (3, 4), (4, 5), (7, 5), (7, 6)])
    T = DiGraph([(1, 0), (2, 0), (2, 1), (2, 4), (3, 0), (3, 1), (3, 2), (4, 0),
                  (4, 1), (4, 3), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4)])
    ex_G = rm_sinks_and_sources(G, T)
    counter = Counter(ex_G.removed)
    for v in [0, 5, 6, 7]:
        assert counter[v] == 1


def test_transitive():
    result = transitive_tournament(5)
    expected = DiGraph([(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2),
                        (4, 0), (4, 1), (4, 2), (4, 3)])
    assert result == expected