from multiprocessing import Process

class Result:
    def __init__(self):
        self.result = False

def homomorphic_H(T, tab, res, is_homomorphic_method):
    for H in tab:
        if any(map(lambda x: all(H.has_edge(e) for e in x.edge_iterator()), T)):
            continue
        if not is_homomorphic_method(H):
            res.result = False
            return
    res.result = True

def run_in_parallel(T, H_tab, fragment_size, is_homomorphic_method):
    processes = []
    results = []
    for i in range(0, len(H_tab), fragment_size):
        fragment = H_tab[i:i + fragment_size]
        result = Result()
        process = Process(target=homomorphic_H, args=(T, fragment, res, is_homomorphic_method,))
        p.start()
        processes.append(p)
        results.append(result)

    for p in processes:
        p.join()

    for j in range(len(results)):
        if not results[j]:
            return False
    return True