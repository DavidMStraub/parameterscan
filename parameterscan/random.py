import uuid
import pandas as pd
import multiprocessing
import schwimmbad
from functools import partial


class RandomScan():
    """Random parameter scan."""

    def __init__(self, store, parfunc, funcdic):
        self.store = store
        self.parfunc = parfunc
        self.funcdic = funcdic

    def get_parameters(self, size=1):
        return [self.parfunc() for _ in range(size)]

    def get_results(self, parameters, key):
        return self.funcdic[key](parameters)

    def run(self, batchsize=1, batches=1, threads=1):
        if threads == 1:
            pool = schwimmbad.SerialPool()
        else:
            pool = multiprocessing.Pool()
        for i in range(batches):
            par_list = self.get_parameters(size=batchsize)
            indices = [uuid.uuid4().hex for i in range(batchsize)]
            df = pd.DataFrame(par_list, index=indices)
            self.store.store_df('parameters', df, append=True)
            for key in self.funcdic:
                worker = partial(_run_single, scan=self, key=key)
                results = list(pool.map(worker, par_list))
                df = pd.DataFrame(results, index=indices)
                self.store.store_df(key, df, append=True)
        pool.close()


def _run_single(p, scan, key):
    return scan.get_results(p, key)
