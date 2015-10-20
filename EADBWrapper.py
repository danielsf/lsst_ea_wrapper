import numpy as np
from lsst.sims.catalogs.generation.db import DBObject

__all__ = ["EADBWrapper"]

class EADBWrapper(object):

    def __init__(self):

        self._dbo = DBObject(database='sysarch', host='terminal.lsst.org',
                             port='3306', driver='mysql')

        self._object_list = [('Name', str, 300), ('Object_ID', np.int),
                             ('ParentID', np.int), ('Object_type', str, 300),
                             ('Author', str, 300), ('Version', str, 300),
                             ('Note', str, 300), ('Package_ID', np.int)]

        self._object_dtype = np.dtype(self._object_list)

        self._object_query = 'select'
        for datum in self._object_list:
            if self._object_query!='select':
                self._object_query += ','
            self._object_query += ' t.%s' % datum[0]
        self._object_query += ' from t_object t'


    def objectIdFromName(self, name):

        dtype = np.dtype([('name', str, 300), ('ObjectID', np.int)])
        query = "select t.name, t.Object_ID from t_object t where t.name = '%s'" % name
        results = self._dbo.execute_arbitrary(query, dtype=dtype)
        return results['ObjectID']


    def getDaughters(self, name, author=None, version=None):
        query = self._object_query + " where t.name='%s'" % name
        results = self._dbo.execute_arbitrary(query, dtype=self._object_dtype)

        if len(results)>1:
            raise RuntimeError('More than one object match the name you gave. '
                               'Try specifying an author or a version')

        if len(results)==0:
            raise RuntimeError('No objects matched the name you gave.')
