import pathlib
import multiprocessing as mp
import matplotlib.pyplot as plt
from collections import Counter

from src.experiments_helpers import *

max_n_cycles = 4
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
PLOTS_PATH = str(pathlib.Path(__file__).parent.absolute()) + "/../plots/"

def generate_and_calculate():
    for p in [1, 0.5, 0]:
        processes = []
        for j in range(1, max_n_cycles + 1):
            out_file = "%.1f:%d.out" % (p, j)
            process = mp.Process(target=check_compressibility_many,
                           args=(experiments_iterator(p, j), ),
                           kwargs={"upper_bound":8, "save_results":PATH + out_file})
            processes.append(process)
            process.start()

def plot_hist(ax, data, title, save_file, xlabel=True):
    bins = np.array([0, 1, 2, 3, 4, 5])

    _, bins, patches = ax.hist(data, bins=bins, rwidth=0.5)

    xlabels = ['', '1', '2', '3', '4+', '']
    N_labels = len(xlabels)
    ax.set_xlim([1, 5])
    ax.set_xticks(np.arange(N_labels) + 0.5)
    ax.set_xticklabels(xlabels)

    ax.set_title(title)
    if xlabel:
        ax.set_xlabel("Różnica pomiędzy kompresyjnością, a długością najdłuższej ścieżki skierowanej.")
    ax.set_ylabel("Liczba grafów")


def plots_p():
    titles = {1: "Tylko ścieżki zewnętrzne (typ 1)",
              0.5: "Kombinacja ścieżek zewnętrznych i wewnętrznych (typ 2)",
              0: "Tylko ścieżki wewnętrzne (typ 3)"}
    fig, axs = plt.subplots(3, 1, figsize=(6, 9))
    for i, p in enumerate([1, 0.5, 0]):
        diff_tab = []
        for j in range(1, max_n_cycles + 1):
            in_file = PATH + "%.1f:%d.out" % (p, j)
            for line in open(in_file, 'r'):
                _, compressibility, path_len = line.split()
                compressibility = int(compressibility)
                path_len = int(path_len)
                if compressibility != -1:
                    diff = compressibility - path_len
                    if diff > 4:
                        diff = 4
                else:
                    diff = 4
                diff_tab.append(diff)
        plot_hist(axs[i], diff_tab, titles[p], "hist:%.1f.png" % p)

    for ax in axs.flat:
        ax.label_outer()
    fig.savefig(PLOTS_PATH + "hist_p_comparison.png")
    fig.show()


def plots_p_1_diff_cycles():
    fig, axs = plt.subplots(2, 2, figsize=(6, 6))
    for j in range(1, max_n_cycles + 1):
        diff_tab = []
        in_file = PATH + "%.1f:%d.out" % (1, j)
        for line in open(in_file, 'r'):
            _, compressibility, path_len = line.split()
            compressibility = int(compressibility)
            path_len = int(path_len)
            if compressibility != -1:
                diff = compressibility - path_len
                if diff > 4:
                    diff = 4
            else:
                diff = 4
            diff_tab.append(diff)

        for kk in [1, 2, 3, 4]:
            print("%d cycles" % j)
            print(len([a for a in diff_tab if a == kk]))

        cykl = "cykl" if j == 1 else "cykle"
        plot_hist(axs[int((j-1)/2), (j-1)%2], diff_tab, "%d %s" % (j, cykl), "hist:1.0:%d.png" % j, False)

    for ax in axs.flat:
        ax.label_outer()
    fig.savefig(PLOTS_PATH + "hist_j_comparison.png")
    fig.show()


# def plots_p_1_vertex_count():
#     for j in range(1, max_n_cycles + 1):
#         results = {}
#         in_file = PATH + "%.1f:%d.out" % (1, j)
#         for line in open(in_file, 'r'):
#             graph, compressibility, path_len = line.split()
#             compressibility = int(compressibility)
#             path_len = int(path_len)
#             vertices = len(DiGraph(graph).vertices())
#             if compressibility != -1:
#                 diff = compressibility - path_len
#                 if diff > 4:
#                     diff = 4
#             else:
#                 diff = 4
#             if vertices not in results:
#                 results[vertices] = []
#             results[vertices].append(diff)
#         for k in results.keys():
#             results[k] = sum(results[k]) / len(results[k])
#
#         plt.scatter(results.keys(), results.values())
#         plt.xlabel("Liczba wierzchołków")
#         plt.ylabel("Średnia różnica")
#         cykl = "cyklu" if j == 1 else "cykli"
#         plt.title("Zależność pomiędzy liczbą wierzchołków, a różnicą\n"
#                   " kompresyjności i długości ścieżki skierowanej\n"
#                   " dla grafów złożonych z %d %s z ścieżkami zewnętrznymi." % (j, cykl))
#         plt.savefig(PLOTS_PATH + "scatter:1.0:%d.png" % j)
#         plt.show()

def plot_density():
    densities = []
    compr_minus_path = []
    for p in [1, 0.5, 0]:
        for j in range(1, max_n_cycles + 1):
            in_file = PATH + "%.1f:%d.out" % (p, j)
            for line in open(in_file, 'r'):
                graph, compressibility, path_len = line.split()
                compressibility = int(compressibility)
                path_len = int(path_len)
                graph = DiGraph(graph)
                density = len(graph.edges()) / len(graph.vertices())
                densities.append(density)
                if compressibility != -1:
                    diff = compressibility - path_len
                    if diff > 4:
                        diff = 4
                else:
                    diff = 4
                compr_minus_path.append(diff)
    plt.scatter(densities, compr_minus_path)
    plt.xlabel("Gęstość")
    plt.ylabel("Kompresyjność - długość najdłuższej ścieżki")

    plt.yticks(np.arange(1, 5), ['1', '2', '3', '4+'])

    plt.savefig(PLOTS_PATH + "density.png")

    plt.show()

def plot_triangles():
    triangles_num = []
    compr_minus_path = []
    for p in [1, 0.5, 0]:
        for j in range(1, max_n_cycles + 1):
            in_file = PATH + "%.1f:%d.out" % (p, j)
            for line in open(in_file, 'r'):
                graph, compressibility, path_len = line.split()
                compressibility = int(compressibility)
                path_len = int(path_len)
                graph = DiGraph(graph).to_undirected()
                triangles_num.append(graph.triangles_count())
                if compressibility != -1:
                    diff = compressibility - path_len
                    if diff > 4:
                        diff = 4
                else:
                    diff = 4
                compr_minus_path.append(diff)

    #plt.scatter(triangles_num, compr_minus_path, c=s)
    plt.scatter(triangles_num, compr_minus_path)
    plt.xlabel("Liczba trójkątów")
    plt.ylabel("Kompresyjność - długość najdłuższej ścieżki")

    plt.yticks(np.arange(1, 5), ['1', '2', '3', '4+'])

    plt.savefig(PLOTS_PATH + "triangles.png")

    plt.show()


# def plot_all():
#     p_tab = []
#     z_tab = []
#     for p in [1, 0.5, 0]:
#         for j in range(1, max_n_cycles + 1):
#             in_file = PATH + "%.1f:%d.out" % (p, j)
#             for line in open(in_file, 'r'):
#                 _, compressibility, path_len = line.split()
#                 p_tab.append(int(path_len))
#                 compressibility = int(compressibility)
#                 if compressibility == -1:
#                     compressibility = 9
#                 z_tab.append(compressibility)
#
#     plt.scatter(p_tab, z_tab)
#     plt.xlabel("Długość najdłuższej ścieżki skierowanej")
#     plt.ylabel("Kompresyjność")
#
#     plt.yticks(np.arange(4, 10), ['4', '5', '6', '7', '8', '9+'])
#
#     plt.savefig(PLOTS_PATH + "all.png")
#
#     plt.show()

plots_p()
plots_p_1_diff_cycles()
plot_density()
plot_triangles()