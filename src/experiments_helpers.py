import sage.all
from sage.graphs.digraph_generators import digraphs
from sage.graphs.digraph import DiGraph
from sage.graphs.graph import Graph

from src.homomorphism import compressibility_number

import numpy as np
from time import time


def random_cycle_paths_out(max_path_len, max_vertices):
    '''Funkcja losująca grafy będące skierowaniami grafów nieskierowanych o dokładnie jedym cyklu, z którego wychodzą
    rozłączne ścieżki.

    :param max_path_len: Int
        Największa dozwolona długość ścieżki skierowanej.
    :param max_vertices: Int
        Największa dozwolona liczba krawędzi.
    :return: tuple
        Para skłądająca się z opisanego grafu skierowanego, oraz długości jego najdłuższej ścieżki.
    '''
    G = Graph()
    # losowanie krawędzi
    cycle_len = np.random.randint(3, max_path_len + 2) # [3, max_path_len + 2)
    G.add_cycle(list(range(0, cycle_len)))
    n = cycle_len
    got_max_vertices = n >= max_vertices
    for i in range(cycle_len):
        if got_max_vertices:
            break
        n_paths = np.random.poisson(1)
        path_lengths = np.random.poisson(lam=int(max_path_len / 2), size=n_paths)
        for path_length in path_lengths:
            if n + path_length > max_vertices:
                path_length = max_vertices - n
                got_max_vertices = True
            G.add_path([i] + list(range(n, n + path_length)))
            n += path_length
            if got_max_vertices:
                break

    # losowanie orientacji
    good_orientation = False
    while not good_orientation: # przeważnie za 1 albo 2 razem
        DiG = G.random_orientation()
        longest_path_len = len(DiG.longest_path().edges())
        good_orientation = DiG.is_directed_acyclic() and longest_path_len <= max_path_len
    return DiG, longest_path_len


def check_compressibility_many(graphs_generator, n_checks, save_results = None):
    '''Funkcja liczy kompresyjność dla 'n_checks' grafów, które są wygenerowane przez 'graphs_generator'.

    :param graphs_generator:
        Funkcja, za pomocą której wytwarzane są kolejne grafy.
    :param n_checks: Int
        Liczba grafów, które będą wygenerowane
    :param save_results: string
        Plik, do którego zapisane zostaną dane w postaci
        "<graf w formacie dig6> <kompresyjność grafu> <długość najdłuższej ścieżki w grafie>"
        linijka po linijce
    :return: list
        Lista o długośc 'n_checks' składająca się z tupli (kompresyjnośc grafu, długość najdłuższej ścieżki w grafie)
    '''
    result = []
    if save_results is not None:
        graphs = []
    for i in range(n_checks):
        G, longest_path_len = graphs_generator()
        if save_results is not None:
            graphs.append(G.dig6_string())
        compressibility = compressibility_number(G)
        result.append((compressibility, longest_path_len))
    if save_results is not None:
        lines_to_write = ["%s %d %d\n" % (graphs[i], result[i][0], result[i][1]) for i in range(n_checks)]
        file = open(save_results, 'w')
        file.writelines(lines_to_write)
    return result

def plot_graphs(file_in, dir_out, compressibility=None, path_len=None, compr_path_diff=None):
    '''Funkcja rysująca grafy, które zostały zapisane w pliku 'file_in' i spełniające kryteria określone przez
    ostatnie trzy parametry opisane poniżej.

    :param file_in: string
        Ścieżka do pliku, z którego pobierane są grafy.
    :param dir_out: string
        Ścieżka do katalogu, w którym zostaną zapisane rysunki.
    :param compressibility: list
        Lista określająca, jaką kompresowalność muszą mieć grafy, żeby zostały narysowane. Jeżeli równe 'None', to brak
        ograniczeń.
    :param path_len: list
        Lista określająca, jaką długość najdłuższej ścieżki muszą mieć grafy, żeby zostały narysowane. Jeżeli równe
        'None', to brak ograniczeń.
    :param compr_path_diff: list
        Lista określająca, jaką różnicę pomiędzy kompresowalnością, a długośćią najdłuższej ścieżki muszą mieć grafy,
        żeby zostały narysowane. Jeżeli równe 'None', to brak ograniczeń.
    '''
    file = open(file_in, 'r')
    i = 0
    if dir_out[-1] != '/':
        dir_out += "/"
    for line in file:
        graph, comp, path = line.split()
        comp = int(comp)
        path = int(path)
        if compressibility is not None:
            if comp not in compressibility:
                continue
        if path_len is not None:
            if path not in path_len:
                continue
        if compr_path_diff is not None:
            if comp - path not in compr_path_diff:
                continue
        p = DiGraph(graph).plot(title="Longest path: %d, Compressibility: %d" % (path, comp))
        p.save(dir_out + "%d.png" % i)
        i += 1