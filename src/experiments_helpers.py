import sage.all
from sage.graphs.digraph_generators import digraphs
from sage.graphs.digraph import DiGraph
from sage.graphs.graph import Graph

from src.homomorphism import compressibility_number

import numpy as np
from time import time
import warnings


def random_cycle_paths(max_cycle_len, max_path_len, max_vertices, p=0,
                       min_cycle_len=1):
    '''Funkcja losująca grafy nieskierowane o dokładnie jedym cyklu, z którego
    wychodzą ścieżki dwóch typów. Pierwszym z nich jest typ "zewnętrzny", czyli
    ścieżki, które zaczynają się w jednym z wierzchołków cyklu i których
    pozostałe wierzchołki są z cyklem rozłączne. Drugi typ jest "wewnętrzny",
    do którego należą ścieżki o dwóch wierzchołkach końcowych należących do
    cyklu lub innej ścieżki wewnętrznej. Wszystkie ścieżki wewnętrzne są
    losowane tak, żeby graf był planarny pod warukiem, że rysowanie ścieżek
    wewnętrznych ograniczamy do wnętrza cyklu.

    :param min_cycle_len: Int
        Minimalna dozwolona długość cyklu.
    :param max_cycle_len: Int
        Największa dozwolona długość cyklu. Jeżeli długość wylosowanego cyklu
        będzie równa `1`, to wygenerowany zostanie wierzchołek, a jeżeli będzie
        równa `2`, to wygenerowana zostanie krawędź.
    :param max_path_len: Int
        Największa dozwolona długość ścieżki wychodzącej z cyklu.
    :param p: Float
        Określa, z jakim prawdopodobieństwem do grafu zostanie dodana kolejna
        ścieżka zewnętrzna. Z prawdopodobieństwem `1-p` zostanie dodana krawędź
        wewnętrzna.
    :param max_vertices: Int
        Największa dozwolona liczba krawędzi.
    :return: tuple
        Para składająca się z opisanego grafu skierowanego, oraz listy
        wierzchołków składającej się z wierzchołków cyklu oraz ścieżek
        "zewnętrznych".
    '''
    if p < 0 or p > 1:
        raise ValueError("Niepoprawna wartość prawdopodobieństwa. `p` musi "
                         "należeć do przedziału [0, 1]")
    if min_cycle_len < 1:
        raise ValueError("Minimalna długość cyklu nie może być mniejsza od 1.")
    if min_cycle_len > max_cycle_len:
        raise ValueError("Minimalna długość cyklu musi być mniejsza lub równa "
                         "maksymalnej.")
    if min_cycle_len < 3 and p < 1:
        warnings.warn("Minimalna długość cyklu pozwala na stworzenie cykli "
                      "bez wnętrza, a wartość `p` dopuszcza istnienie ścieżek "
                      "wewnętrznych. W przypadku wylosowania krótkiego cyklu, "
                      "wszystkie ścieżki będą zewnętrzne.")
    G = Graph()
    cycle_len = np.random.randint(min_cycle_len, max_cycle_len + 1)
    if cycle_len == 1:
        p = 1
        G.add_vertex(0)
        outside_vertices = [0]
    elif cycle_len == 2:
        p = 1
        G.add_edge((0, 1))
        outside_vertices = [0, 1]
    else:
        G.add_cycle(list(range(0, cycle_len)))
        outside_vertices = list(range(0, cycle_len))
    n = cycle_len
    got_max_vertices = n >= max_vertices
    cycle_partitions = [list(range(0, n))]
    for i in range(cycle_len):
        if got_max_vertices:
            break
        n_paths = np.random.poisson(1)
        path_lengths = np.random.poisson(lam=int(max_path_len / 2),
                                         size=n_paths)
        for path_length in path_lengths:
            if n + path_length > max_vertices:
                path_length = max_vertices - n
                got_max_vertices = True
            if path_length == 0:
                if got_max_vertices:
                    break
                else:
                    continue
            if np.random.rand(1) > p:
                available_parts = [tab for tab in cycle_partitions if i in tab]
                cycle_part = \
                    available_parts[np.random.randint(0, len(available_parts))]
                j = i
                while j == i:
                    j = np.random.choice(cycle_part)
                # split
                k = 0
                parts = [[], []]
                part_id = 0
                new_path = list(range(n, n + path_length - 1))
                for k in cycle_part:
                    parts[part_id].append(k)
                    if k in [i, j]:
                        if k == i:
                            parts[part_id] += new_path
                        else:
                            parts[part_id] += new_path[::-1]
                        part_id = 1 - part_id
                        parts[part_id].append(k)
                cycle_partitions.remove(cycle_part)
                cycle_partitions.append(parts[0])
                cycle_partitions.append(parts[1])
                G.add_path([i] + new_path + [j])
            else:
                G.add_path([i] + list(range(n, n + path_length)))
                outside_vertices += list(range(n, n + path_length))
            n += path_length
            if got_max_vertices:
                break
    return G, outside_vertices


def random_multiple_cycles_connected(n_cycles, max_vertices, max_cycle_len,
                                     max_path_len, p, min_cycle_len=1):
    '''Generuje `n_cycles` rozłącznch cykli według procedury opisanej w
    `random_cycle_paths`. Następnie łączy te cykle poprzez scalanie kolejnych
    losowo wybranych wierzchołków, dopóki graf nie będzie spójny.

    :param n_cycles: Int
        Liczba wygenerowanych rozłącznych cykli.
    :param max_vertices: Int
        Maksymalna dozwolona liczba wierzchołków w zwracanym grafie.
    :param max_cycle_len: Int
        Maksymalna dozwolona długość cyklu spośród tych generowanych na
        początku. Ostateczny graf może posiadać dłuższe cykle!
    :param max_path_len: Int
        Maksymalna dozwolona długość ścieżki wychodzącej z pojedynczego cyklu.
        Określa jedynie długości ścieżek w cyklach generowanych na samym
        początku, a nie w ostatecznym grafie.
    :param min_cycle_len:
        Minimalna długość generowanych cykli.
    :param p: Float:
        Określa, z jakim prawdopodobieństwem do grafu zostanie dodana kolejna
        ścieżka zewnętrzna. Z prawdopodobieństwem `1-p` zostanie dodana krawędź
        wewnętrzna. Opis typów ścieżek znajduje się w opisie
        `random_cycle_paths`.
    :return:
        Spójny graf nieskierowany
    '''
    G = Graph()
    outside_vertices = []
    for i in range(n_cycles):
        H, out = random_cycle_paths(max_cycle_len=max_cycle_len,
                                    min_cycle_len=min_cycle_len,
                                    max_path_len=int(max_path_len/2),
                                    max_vertices=int(max_vertices/n_cycles),
                                    p=p)
        outside_vertices.append([(i, v) for v in out])
        H.relabel(lambda v: (i, v))
        G = G.union(H)
    while len(outside_vertices) > 1:
        i, j = np.random.choice(range(len(outside_vertices)), size=2,
                                replace=False)
        out_i = outside_vertices[i]
        out_j = outside_vertices[j]
        v_id, = np.random.choice(len(out_i), size=1)
        v = out_i[v_id]
        u_id, = np.random.choice(len(out_j), size=1)
        u = out_j[u_id]
        G.merge_vertices([u, v])
        out_new = out_i + out_j
        out_new.remove(v)  # v merged
        outside_vertices.remove(out_i)
        outside_vertices.remove(out_j)
        outside_vertices.append(out_new)
    G.relabel()
    return G


def random_orientation(G, max_path_len):
    '''Funkcja tworząca losowe acykliczne skierowanie grafu `G`,
    którego długość najdłuższej ścieżki skierowanej jest mniejsza lub równa
    `max_path_len`.

    :param G: Graph
        Graf, którego skierowanie jest losowane.
    :param max_path_len: Int
        Największa długość ścieżki skierowanej w wyjściowym grafie.
    :return: tuple
        Para składająca się z acyklicznego grafu skierowanego, oraz długości
        jego najdłuższej ścieżki skierowanej.
    '''
    good_orientation = False
    while not good_orientation:
        DiG = G.random_orientation()
        longest_path_len = len(DiG.longest_path().edges())
        good_orientation = \
            DiG.is_directed_acyclic() and longest_path_len <= max_path_len
    return DiG, longest_path_len


def check_compressibility_many(graphs_iterator, upper_bound,
                               save_results=None):
    '''Funkcja liczy kompresyjność dla grafów podanych na wejściu.

    :param graphs_iterator:
        Iterator, za pomocą którego wytwarzane są kolejne grafy. Powinien
        zwracać parę `(G, i)`, gdzie `G` jest grafem skierowanym, a `i` jest
        długością najdłuższej ścieżki skierowanej w `G`.
    :param save_results: string
        Plik, do którego zapisane zostaną dane w postaci
        "<graf w formacie dig6> <kompresyjność grafu>\
         <długość najdłuższej ścieżki w grafie>"
        linijka po linijce
    :param upper_bound: Int
        Liczba, do której jest liczona kompresyjność. Jeżeli okaże się, że jest
        ona wyższa, to zwracane jest -1.
    :return: list
        Lista o długości równej liczbie wygenerowanych grafów składająca się z
        tupli (kompresyjnośc grafu, długość najdłuższej ścieżki w grafie).
        Górna granica, do której sprawdzana jest kompresyjność to 9, ze względu
        bardzo długi czas trwania obliczeń powyżej tej liczby.
    '''
    result = []
    if save_results is not None:
        graphs = []
    for G, longest_path_len in graphs_iterator:
        if save_results is not None:
            graphs.append(G.dig6_string())
        compressibility = compressibility_number(G, upper_bound=upper_bound)
        result.append((compressibility, longest_path_len))
    if save_results is not None:
        lines_to_write = ["%s %d %d\n" % (graphs[i], result[i][0],
                                          result[i][1])
                          for i in range(len(graphs))]
        file = open(save_results, 'w')
        file.writelines(lines_to_write)
    return result


def plot_graphs(file_in, dir_out, compressibility=None, path_len=None,
                compr_path_diff=None):
    '''Funkcja rysująca grafy, które zostały zapisane w pliku 'file_in' i
    spełniające kryteria określone przez ostatnie trzy parametry opisane
    poniżej.

    :param file_in: string
        Ścieżka do pliku, z którego pobierane są grafy.
    :param dir_out: string
        Ścieżka do katalogu, w którym zostaną zapisane rysunki.
    :param compressibility: list
        Lista określająca, jaką kompresowalność muszą mieć grafy, żeby zostały
        narysowane. Jeżeli równe 'None', to brak ograniczeń.
    :param path_len: list
        Lista określająca, jaką długość najdłuższej ścieżki muszą mieć grafy,
        żeby zostały narysowane. Jeżeli równe 'None', to brak ograniczeń.
    :param compr_path_diff: list
        Lista określająca, jaką różnicę pomiędzy kompresowalnością, a długośćią
        najdłuższej ścieżki muszą mieć grafy, żeby zostały narysowane. Jeżeli
        równe 'None', to brak ograniczeń.
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
        p = DiGraph(graph).plot(title="Longest path: %d, Compressibility: %d"
                                      % (path, comp))
        p.save(dir_out + "%d.png" % i)
        i += 1
