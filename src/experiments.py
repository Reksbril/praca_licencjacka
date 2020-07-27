from src.experiments_helpers import *

p = random_multiple_cycles_connected(n_cycles=1, max_vertices=20, max_cycle_len=5, max_path_len=10, min_cycle_len=3).plot(layout="planar")
p.save("xdd.png")
#print(check_compressibility_many(lambda : random_cycle_paths_out(5, 20), 100, "kek"))
#plot_graphs("kek", "kekk", compr_path_diff=[2])