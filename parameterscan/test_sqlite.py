import unittest
import parameterscan
import tempfile
from shutil import rmtree
import os
import numpy as np
import numpy.testing as npt


class TestSQLite(unittest.TestCase):
    def test_init(self):
        dir = tempfile.mkdtemp()
        store = parameterscan.ScanStoreSQL('scanname', scanid=5, datadir=dir)
        din = {'bla': 1, 'blo': np.array([1, 2, 3])}
        store.store_dict('mykey', din)
        self.assertTrue(os.path.exists(os.path.join(dir, 'scanname_5.sqlite')))
        dout = store.get('mykey')
        self.assertTrue(len(dout), 1)
        store.store_dict('mykey', din)
        self.assertTrue(len(dout), 1)
        dout = store.get('mykey')
        self.assertTrue(len(dout), 2)
        self.assertEqual(list(din.keys()), list(dout.loc[0].keys()))
        for k, v in din.items():
            npt.assert_array_equal(v, dout.iloc[0][k])
        rmtree(dir)
