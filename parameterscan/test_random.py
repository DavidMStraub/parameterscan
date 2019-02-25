import unittest
import parameterscan
import tempfile
from shutil import rmtree
import numpy as np


def random_par():
    return {'x': np.random.rand(),
            'y': np.random.rand(3, 3)}


def obs_func(par):
    return {'bla': 2 * par['x'] + np.linalg.det(par['y']),
            'blo': 2 * par['x'] + par['y']}


class TestRandom(unittest.TestCase):
    def test_init(self):
        dir = tempfile.mkdtemp()
        store = parameterscan.ScanStoreSQL('scanname', datadir=dir)
        scan = parameterscan.RandomScan(store, random_par, {'obs': obs_func})
        scan.run(batchsize=3, batches=2)
        obs = store.get('obs')
        par = store.get('parameters')
        self.assertTrue(obs.shape == (3 * 2, 2))
        self.assertTrue(par.shape == (3 * 2, 2))
        self.assertEqual(set(par.columns), {'x', 'y'})
        self.assertEqual(set(obs.columns), {'bla', 'blo'})
        rmtree(dir)
