import numpy as np
from lsst.sims.catalogs.generation.db import DBObject

__all__ = ["EADBWrapper", "SysMLObject"]

class SysMLObject(object):

    def __init__(self):
        self._name = None
        self._objid = None
        self._parentid = None
        self._version = None
        self._author = None
        self._daughters = None
        self._properties = {}
        self._attributes = {}


    def getData(self, dbo, objid):
        """
        Get the data for this SysMLObject

        @param [in] dbo is an EADBWrapper

        @param [in] objid is an int denoting the objectID of this object
        """

        if self._objid is not None:
            raise RuntimeError("You just tried to populate a SysMLObject"
                               "That is already populated")

        self._objid=objid
        dtype = np.dtype([
                         ('Name', str, 300),
                         ('Object_ID', np.int),
                         ('ParentID', np.int),
                         ('Version', str, 300),
                         ('Author', str, 300)
                        ])

        query = "select t.Name, t.Object_ID, t.ParentID, t.Version, t.Author " \
                 + "from t_object t where t.Object_ID=%d" % objid

        results = dbo._dbo.execute_arbitrary(query, dtype=dtype)
        if len(results)!=1:
            raise RuntimeError("The ObjectID you passed to SysMLObject produced"
                               "%d objects; not 1" % len(results))

        self._name = results['Name'][0]
        self._author = results['Author'][0]
        self._version = results['Version'][0]

        # get daughters
        dtype = np.dtype([('Object_ID', np.int)])
        query = "select t.Object_ID from t_object t where t.ParentID=%d" % objid
        results = dbo._dbo.execute_arbitrary(query, dtype=dtype)
        self._daughters = list(results['Object_ID'])

        # query t_attribute
        dtypeList = [
                     ('Object_ID', np.int),
                     ('Name', str, 300),
                     ('Scope', str, 300),
                     ('Stereotype', str, 300),
                     ('Containment', str, 300),
                     ('IsStatic', str, 300),
                     ('IsCollection', str, 300),
                     ('IsOrdered', str, 300),
                     ('AllowDuplicates', str, 300),
                     ('LowerBound', np.float),
                     ('UpperBound', np.float),
                     ('Container', str, 300),
                     ('Notes', str, 300),
                     ('Derived', str, 300),
                     ('ID', np.int),
                     ('Pos', str, 300),
                     ('GenOption', str, 300),
                     ('Length', str, 300),
                     ('Precision', str, 300),
                     ('Scale', str, 300),
                     ('Const', str, 300),
                     ('Style', str, 300),
                     ('Classifier', str, 300),
                     ('Default', np.float),
                     ('Type', str, 300),
                     ('ea_guid', str, 300),
                     ('StyleEx', str, 300)
                     ]

        dtype = np.dtype(dtypeList)

        query = "select * from t_attribute t where t.Object_ID=%d" % objid
        results = dbo._dbo.execute_arbitrary(query, dtype=dtype)

        for ix in range(len(results)):
            attName = results['Name'][ix]
            self._attributes[attName] = {}
            for column in dtype_list:
                if column[0] != 'Name':
                    self._attributes[attName][column[0]] = results[column[0]][ix]

        # query t_objectproperties
        dtypeList = [
                    ('PropertyID', np.int),
                    ('Object_ID', np.int),
                    ('Property', str, 300),
                    ('Value', str, 300),
                    ('Notes', str, 300),
                    ('ea_guid', str, 300)
                    ]

        dtype = np.dtype(dtypeList)
        query = "select * from t_objectproperties t where t.Object_ID=%d" % objid
        results = dbo._dbo.execute_arbitrary(query, dtype=dtype)
        for ix in range(len(results)):
            pName = results['Property'][ix]
            self._properties[pName] = {}
            for column in dtypeList:
                if column[0]!='Property':
                    self._properties[pName][column[0]] = results[column[0]][ix]


    @property
    def name(self):
        """a string carrying the name of the object"""
        return self._name

    @property
    def objid(self):
        """an int carrying the ID of the object"""
        return self._objid

    @property
    def parent(self):
        """an int carrying the ID of the object's parent"""
        return self._parentid


    @property
    def version(self):
        """a string carrying the version of the object"""
        return self._version

    @property
    def author(self):
        """a string carrying the author of the object"""
        return self._author

    @property
    def daughters(self):
        """a list carrying the IDs of daughter objects"""
        return self._daughters


    @property
    def properties(self):
        """
        A dict carrying properties of the object.
        The dict will be keyed to the property's name.
        The dict will store all of the values associated with
        that property in SysML
        """

        return self._properties

    @property
    def attributes(self):
        """
        A dict carrying the attributes of the object.
        The dict will be keyed to the attribute's name.
        The dict will carry a dict of all of the values
        associated with that attribute in SysML.
        """

        return self._attributes



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


    def _getDaughtersFromObjID(self, objid):
        """
        Recursively return a list of Object_IDs corresponding to the objects
        descended (either directly or indirectly) from an object specified by an
        Object_ID
        """
        query = self._object_query + " where t.ParentID=%d" % objid
        results = self._dbo.execute_arbitrary(query, dtype=self._object_dtype)
        ans = list(results["Object_ID"])
        for aa in results["Object_ID"]:
            new_results = self._getDaughtersFromObjID(aa)
            ans += new_results
        return ans


    def getFamilyIDs(self, name, author=None, version=None):
        """
        Get a list of the Object_IDs of all objects descended (directly or
        indirectly) from a specified object

        @param[in] name is a string denoting the name of the desired object

        @param[in] author is an optional string denoting the author of the
        desired object (in case there are multiple versions)

        @param[in] version is an optional string denoting the version
        of the desired object (in case there are multiple versions)

        @param[out] a list of ints denoting the Object_IDs of all of
        the objects beneath the desired object in its family tree.
        """
        query = self._object_query + " where t.name='%s'" % name

        if author is not None:
            query += " and t.Author='%s'" % author
        if version is not None:
            query += " and t.Version='%s'" % version

        results = self._dbo.execute_arbitrary(query, dtype=self._object_dtype)

        if len(results)>1:
            raise RuntimeError('More than one object match the name you gave. '
                               'Try specifying an author or a version')

        if len(results)==0:
            raise RuntimeError('No objects matched the name you gave.')

        return list(results["Object_ID"]) + self._getDaughtersFromObjID(results["Object_ID"][0])
