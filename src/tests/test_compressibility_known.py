import sage.all
from sage.graphs.digraph_generators import digraphs

import pytest

from src.homomorphism import compressibility_number


#8 - 4s, 9 - 2m 39s
#@pytest.mark.parametrize('n', list(range(2, 9)))
def test_path():
    G = digraphs.Path(9)
    assert compressibility_number(G) == 9