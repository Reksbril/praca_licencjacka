import sage.all
from sage.graphs.digraph_generators import digraphs

import pytest

from src.homomorphism import compressibility_number


#7 - 552 ms, 8 - 4s, 9 - ??
#@pytest.mark.parametrize('n', list(range(2, 9)))
def test_path():
    G = digraphs.Path(8)
    assert compressibility_number(G) == 8