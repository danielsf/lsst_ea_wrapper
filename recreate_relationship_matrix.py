from __future__ import with_statement
import numpy as np
from EADBWrapper import EADBWrapper

if __name__ == "__main__":

    eadbo = EADBWrapper()
    dbo = eadbo._dbo
    property_dtype = np.dtype([('Object_ID', np.int),
                               ('Property', str, 300),
                               ('PropertyID', np.int),
                               ('Value', str, 300),
                               ('Notes', str, 300)])

    property_query = "select t.Object_ID, t.Property, t.PropertyID, " \
                      + "t.Value, t.Notes from t_objectproperties t " \
                      + "where t.Property like '%lsstrequire%'"

    results = dbo.execute_arbitrary(property_query, dtype=property_dtype)
    print results
    print len(results)


