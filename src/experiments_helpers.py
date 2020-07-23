import sage.all
from sage.graphs.digraph_generators import digraphs
from sage.graphs.digraph import DiGraph
from sage.graphs.graph import Graph

from src.homomorphism import compressibility_number

import numpy as np
from time import time


def random_cycle_paths_out(max_cycle_len, max_path_len, max_vertices, paths_type, min_cycle_len=1):
    '''Funkcja losująca grafy nieskierowane o dokładnie jedym cyklu, z którego wychodzą ścieżki dwóch typów.
    Pierwszym z nich jest typ "zewnętrzny", czyli ścieżki, które zaczynają się w jednym z wierzchołków cyklu i których
    pozostałe wierzchołki są z cyklem rozłączne. Drugi typ jest "wewnętrzny" TODO dokończyć opis

    :param min_cycle_len: Int
        Minimalna dozwolona długość cyklu.
    :param max_cycle_len: Int
        Największa dozwolona długość cyklu. Jeżeli długość wylosowanego cyklu będzie równa `1`, to wygenerowany zostanie
        wierzchołek, a jeżeli będzie równa `2`, to wygenerowana zostanie krawędź.
    :param max_path_len: Int
        Największa dozwolona długość ścieżki wychodzącej z cyklu.
    :param p: Float
        Określa, z jakim prawdopodobieństwem do grafu zostanie dodana kolejna ścieżka wychodząca.
    :param max_vertices: Int
        Największa dozwolona liczba krawędzi.
    :return: tuple
        Para składająca się z opisanego grafu skierowanego, oraz długości jego najdłuższej ścieżki.
    '''
    if min_cycle_len < 1:
        raise ValueError("Minimalna długość cyklu nie może być mniejsza od 1.")
    if min_cycle_len > max_cycle_len:
        raise ValueError("Minimalna długość cyklu musi być mniejsza lub równa maksymalnej.")
    G = Graph()
    cycle_len = np.random.randint(min_cycle_len, max_cycle_len + 1)
    if cycle_len == 1:
        G.add_vertex(0)
    elif cycle_len == 2:
        G.add_edge((0, 1))
    else:
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
    return G


def random_cycle_paths_inside(max_cycle_len, max_path_len, max_vertices, min_cycle_len=1):



def random_multiple_cycles_connected(n_cycles, max_vertices, max_cycle_len, max_path_len, min_cycle_len=1):
    '''Generuje `n_cycles` rozłącznch cykli według procedury opisanej w `random_cycle_paths_out`. Następnie łączy
    te cykle poprzez scalanie kolejnych losowo wybranych wierzchołków, dopóki graf nie będzie spójny.

    :param n_cycles: Int
        Liczba wygenerowanych rozłącznych cykli.
    :param max_vertices: Int
        Maksymalna dozwolona liczba wierzchołków w zwracanym grafie.
    :param max_cycle_len: Int
        Maksymalna dozwolona długość cyklu spośród tych generowanych na początku. Ostateczny graf może posiadać dłuższe
        cykle!
    :param max_path_len: Int
        Maksymalna dozwolona długość ścieżki wychodzącej z pojedynczego cyklu. Określa jedynie długości ścieżek w
        cyklach generowanych na samym początku, a nie w ostatecznym grafie.
    :param min_cycle_len:
        Minimalna długość generowanych cykli.
    :return:
        Spójny graf nieskierowany
    '''
    G = Graph()
    for i in range(n_cycles):
        H = random_cycle_paths_out(max_cycle_len=max_cycle_len,
                                   min_cycle_len=min_cycle_len,
                                   max_path_len=int(max_path_len/2),
                                   max_vertices=int(max_vertices/n_cycles))
        G = G.disjoint_union(H)
    G.relabel()
    connected_components = G.connected_components()
    while len(connected_components) > 1:
        i, j = np.random.choice(range(len(connected_components)), size=2, replace=False)
        v, = np.random.choice(connected_components[i], size=1)
        u, = np.random.choice(connected_components[j], size=1)
        G.merge_vertices([u, v])
        connected_components = G.connected_components()
    return G


def random_orientation(G, max_path_len):
    '''FUnkcja tworząca losowe acykliczne skierowanie grafu `G`, którego długość najdłuższej ścieżki skierowanej jest
    mniejsza lub równa `max_path_len`.

    :param G: Graph
        Graf, którego skierowanie jest losowane.
    :param max_path_len: Int
        Największa długość ścieżki skierowanej w wyjściowym grafie.
    :return:
        Acykliczny graf skierowany.
    '''
    good_orientation = False
    while not good_orientation: # przeważnie za 1 albo 2 razem
        DiG = G.random_orientation()
        longest_path_len = len(DiG.longest_path().edges())
        good_orientation = DiG.is_directed_acyclic() and longest_path_len <= max_path_len
    return DiG, longest_path_len


def check_compressibility_many(graphs, save_results = None):
    '''Funkcja liczy kompresyjność dla grafów podanych na wejściu.

    :param graphs_generator:
        Iterator, za pomocą którego wytwarzane są kolejne grafy. Powinien zwracać parę `(G, i)`, gdzie `G` jest grafem
        skierowanym, a `i` jest długością najdłuższej ścieżki skierowanej w `G`.
    :param save_results: string
        Plik, do którego zapisane zostaną dane w postaci
        "<graf w formacie dig6> <kompresyjność grafu> <długość najdłuższej ścieżki w grafie>" linijka po linijce
    :return: list
        Lista o długości równej liczbie wygenerowanych grafów składająca się z tupli
        (kompresyjnośc grafu, długość najdłuższej ścieżki w grafie)
    '''
    result = []
    if save_results is not None:
        graphs = []
    for G, longest_path_len in graphs:
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