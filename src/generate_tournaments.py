'''
Plik, za pomocą którego tworzone są pliki w katalogu 'tournaments'.
'''
import sage.all
from sage.graphs.digraph_generators import digraphs

import sys
import os
from tqdm import tqdm

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PATH + "/..")

from src.helpers import *

if __name__ == '__main__':
    graphs_counts = [1, 1, 2, 4, 12, 56, 456, 6880, 191536, 9733056]
    if not os.path.exists(PATH + "/../tournaments"):
        os.mkdir(PATH + "/../tournaments")
    if not os.path.exists(PATH + "/../tournaments/one_cycle"):
        os.mkdir(PATH + "/../tournaments/one_cycle")
    if not os.path.exists(PATH + "/../tournaments/more_cycles"):
        os.mkdir(PATH + "/../tournaments/more_cycles")
    for i in range(1, 11):
        one = []
        more = []
        transitive = False  # czy już napotkany był turniej tranzytywny
        print("Generating graphs with %d vertices..." % i)
        for H in tqdm(digraphs.tournaments_nauty(i),
                      total=graphs_counts[i - 3],file=sys.stdout):
            if not transitive and H.is_transitive():
                transitive = True
                continue
            if has_exactly_one_cycle_tournament(H):
                one.append(H.dig6_string() + '\n')
            else:
                more.append(H.dig6_string() + '\n')

        print("Saving to files...")
        file = open(PATH + "/../tournaments/one_cycle/%d.dig6" % i, 'w')
        file.writelines(one)

        file = open(PATH + "/../tournaments/more_cycles/%d.dig6" % i, 'w')
        file.writelines(more)
