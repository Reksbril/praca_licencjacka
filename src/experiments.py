import pathlib
import multiprocessing as mp

from src.experiments_helpers import *


max_n_cycles = 5
max_vertices = 30
N = 10
max_cycle_len = 7
max_oriented_path_len = 5

def experiments_iterator(p, j):
    for i in range(N):
        G = random_multiple_cycles_connected(n_cycles=j,
                                             max_vertices=max_vertices,
                                             max_cycle_len=max_cycle_len,
                                             max_path_len=int(max_cycle_len/2)+1,
                                             p=p,
                                             min_cycle_len=3)
        G, l = random_orientation(G, max_oriented_path_len)
        print("(%.1f, %d): generated %s for i=%d" %(p, j, G.dig6_string(), i))
        yield G, l


PATH = str(pathlib.Path(__file__).parent.absolute()) + "/../results/"


for p in [1, 0.5, 0]:
    processes = []
    for j in range(1, max_n_cycles + 1):
        out_file = "%.1f:%d.out" % (p, j)
        process = mp.Process(target=check_compressibility_many,
                       args=(experiments_iterator(p, j), ),
                       kwargs={"upper_bound":8, "save_results":PATH + out_file})
        processes.append(process)
        #check_compressibility_many(experiments_iterator(p, j), upper_bound=8, save_results=PATH + out_file)
        process.start()



