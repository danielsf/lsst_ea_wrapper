import numpy as np
from lsst.sims.catalogs.generation.db import DBObject

__all__ = ["EADBWrapper"]

class EADBWrapper(object):

    def __init__(self):

        self._dbo = DBObject(database='sysarch', host='terminal.lsst.org',
                             port='3306', driver='mysql')

        self._objSearchDtype = np.dtype([('name', str, 100), ('ObjectID', np.int)])


    def objectIdFromName(self, name):

        query = "select t.name, t.Object_ID from t_object t where t.name = '%s'" % name
        results = self._dbo.execute_arbitrary(query, dtype=self._objSearchDtype)
        return results['ObjectID']


    def daughterObjectsFromID(self, parentID):
 
        dtype = np.dtype([('name',str,100), ('ObjectID',np.int)])
        query = "select t.name, t.Object_ID from t_object t where t.ParentID = %d" % parentID
        results = self._dbo.execute_arbitrary(query, dtype=dtype)
        nameList = results['name']
        objIdList = results['ObjectID']

        propertyIdList = []
        dtype = np.dtype([('PropertyID', np.int)])
        for objId in objIdList:
            query = "select t.PropertyID from t_objectproperties t where t.Object_ID = %d" % objId
            results = self._dbo.execute_arbitrary(query, dtype=dtype)
            if len(results)!=1:
                 raise RuntimeError("Not sure what to do; got more than one property in daughterObjectsFromID")
            propertyIdList.append(results['PropertyID'][0])

        return nameList, objIdList, propertyIdList
