'''
Plik, za pomocą którego tworzone są pliki w katalogu 'tournaments'.
'''
import sage.all
from sage.graphs.digraph_generators import digraphs

import sys
from tqdm import tqdm

from src.helpers import *


if __name__ == '__main__':
    graphs_counts = [1, 1, 2, 4, 12, 56, 456, 6880, 191536, 9733056]
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
        file = open("../tournaments/one_cycle/%d.dig6" % i, 'w')
        file.writelines(one)

        file = open("../tournaments/more_cycles/%d.dig6" % i, 'w')
        file.writelines(more)
