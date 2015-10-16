import numpy as np
from lsst.sims.catalogs.generation.db import DBObject

__all__ = ["EADBWrapper"]

class EADBWrapper(object):

    def __init__(self):

        self._dbo = DBObject(database='sysarch', host='terminal.lsst.org',
                             port='3306', driver='mysql')


    def objectIdFromName(self, name):

        dtype = np.dtype([('name', str, 100), ('ObjectID', np.int)])
        query = "select t.name, t.Object_ID from t_object t where t.name = '%s'" % name
        results = self._dbo.execute_arbitrary(query, dtype=dtype)
        return results['ObjectID']   
