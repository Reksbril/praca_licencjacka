from multiprocessing import Process
import os

from tqdm import tqdm

import sage.all
from sage.graphs.digraph import DiGraph

PATH = os.path.dirname(os.path.abspath(__file__))

class Result:
    def __init__(self):
        self.result = False

class Parallel:
    def __init__(self, n_threads, n_graphs_in_thread, is_homomorphic_method, T):
        self.n_threads = n_threads
        self.n_graphs_in_thread = n_graphs_in_thread
        self.is_homomorphic_method = is_homomorphic_method
        self.T = T

    def _get_n_from_lines(self, n):
        for i in range(0, len(self.lines), n):
            yield self.lines[i:i + n]

    def run(self):
        self.lines = open(PATH + "/../tournaments/more_cycles/10.dig6", 'r').readlines()
        chunk_size = self.n_graphs_in_thread * self.n_threads
        for chunk in tqdm(self._get_n_from_lines(chunk_size), total=120):
            if not self._run_in_parallel(chunk):
                return False
        return True

    def _homomorphic_H(self, lines, result):
        for line in lines:
            H = DiGraph(line, format="dig6")
            if any(map(lambda x: all(H.has_edge(e) for e in x.edge_iterator()), self.T)):
                continue
            if not self.is_homomorphic_method(H):
                result.result = False
                return
        result.result = True

    def _run_in_parallel(self, chunk):
        processes = []
        results = []
        for i in range(0, len(chunk), self.n_graphs_in_thread):
            fragment = chunk[i:i + self.n_graphs_in_thread]
            result = Result()
            process = Process(target=self._homomorphic_H, args=(fragment, result,))
            process.start()
            processes.append(process)
            results.append(result)

        for p in processes:
            p.join()

        for j in range(len(results)):
            if not results[j]:
                return False
        return True