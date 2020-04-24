import sage.all
from sage.graphs.digraph import DiGraph
from sage.graphs.digraph_generators import digraphs
import pytest

from src.DiGraphExtended import DiGraphExtended


@pytest.mark.parametrize('type', ['sink', 'source'])
def test_no_sinks(type):
    G = DiGraph()
    G.add_cycle([0, 1, 2])
    ex = DiGraphExtended(G)
    with pytest.raises(RuntimeError):
        ex.step(type)

@pytest.mark.parametrize('case', [
    {'type' : 'sink', 'vertices' : [3, 2, 1, 0]},
    {'type' : 'source', 'vertices' : [1, 2, 3, 4]}
])
def test_extended_tournament(case):
    T = digraphs.TransitiveTournament(5)
    ex = DiGraphExtended(T)
    for i in case['vertices']:
        assert ex.step(case['type']) == [i]


def test_sinks_sources_simple():
    G = DiGraph()
    G.add_edge(0, 1)
    ex = DiGraphExtended(G)

    assert ex.sources() == [0]
    assert ex.sinks() == [1]

def test_sinks_then_source():
    G = DiGraph()
    G.add_edge(0, 1)
    G.add_edge(0, 2)
    ex = DiGraphExtended(G)
    assert ex.step('sink') == [0]

def test_sinks_then_source_duplicates():
    G = DiGraph()
    G.add_vertex(0)
    G.add_edge(1, 2)
    ex = DiGraphExtended(G)
    ex.step('sink')
    assert ex.sources() == [1]

def test_get_current():
    G = DiGraph()
    G.add_edges([(0, 1), (1, 2), (1, 3), (1, 4)])
    ex = DiGraphExtended(G, keep_removed=True)
    ex.step('sink')

    result = ex.get_current()
    expected = DiGraph()
    expected.add_edges([(0, 1)])

    assert result == expected