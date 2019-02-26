import numpy as np
import pandas as pd
import os
import sqlalchemy
from time import sleep
import pickle
from numbers import Number


def serialize(x):
    if not isinstance(x, (str, Number)):
        return pickle.dumps(x)
    else:
        return x


def unserialize(x):
    if not isinstance(x, (str, Number)):
        return pickle.loads(x)
    else:
        return x


class ScanStoreSQL(object):
    """Generic SQLite parameter scan store."""

    def __init__(self, scanname, scanid=1, datadir=None):
        self.scanname = scanname
        self.scanid = scanname
        if datadir is None:
            datadir = os.getcwd()
        self.datadir = datadir
        _filename = '{}_{}.sqlite'.format(scanname, scanid)
        self.filename = os.path.join(self.datadir, _filename)

    @property
    def engine(self):
        return sqlalchemy.create_engine('sqlite:///' + self.filename)

    def store_df(self, key, df, append=True, **kwargs):
        """Store a Pandas DataFrame in a table."""
        if_exists = 'append' if append else 'replace'
        while True:
            try:
                df.applymap(serialize).to_sql(key, self.engine, if_exists=if_exists)
                break
            except sqlalchemy.exc.OperationalError:
                sleep(0.001)

    def store_row(self, key, array, index=0, columns=None, append=True, **kwargs):
        """Store a numpy array or a list in a table."""
        df = pd.DataFrame([array], columns=columns, index=(index,))
        self.store_df(key, df, append=append)

    def store_dict(self, key, dict, index=0, append=True, **kwargs):
        """Store a dictionary in a table."""
        self.store_row(key,
                       array=list(dict.values()),
                       index=index,
                       columns=list(dict.keys()),
                       **kwargs)

    def store_array(self, key, array, index=None, columns=None, append=True, **kwargs):
        """Store a numpy array in a table."""
        df = pd.DataFrame(array, columns=columns, index=index, dtype=complex)
        self.store_df(key, df, append=append)

    def get(self, key):
        """Return a DataFrame for a given key (table name)."""
        while True:
            try:
                with self.engine.connect() as conn, conn.begin():
                    data = pd.read_sql_table(key, conn)
                break
            except sqlalchemy.exc.OperationalError:
                sleep(0.001)
        data = data.set_index('index')
        return data.applymap(unserialize)

    def drop_table(self, key):
        """Delete (drop) a table"""
        pd.io.sql.execute('DROP TABLE {};'.format(key), self.engine)

    def read_sql(self, sql):
        """Read SQL query into a data frame."""
        return pd.io.sql.read_sql(sql, self.engine)
