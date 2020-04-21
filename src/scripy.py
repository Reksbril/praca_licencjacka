from sage.all import *

gen = digraphs.tournaments_nauty(4)
for g in gen:
    print(g.edges())
