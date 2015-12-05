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

    property_results = dbo.execute_arbitrary(property_query,
                                             dtype=property_dtype)

    property_id_list = property_results['Object_ID']

    connection_dtype = np.dtype([('Btm_Mid_Label', str, 300),
                                ('Start_Object_ID', np.int),
                                ('End_Object_ID', np.int)])

    connection_query = "select c.Btm_Mid_Label, c.Start_Object_ID, " \
                       + "c.End_Object_ID from t_connector c " \
                       + "inner join t_objectproperties p " \
                       + "on p.Object_ID = c.Start_Object_ID " \
                       + "where p.Property like '%lsstrequire%'"

    result = dbo.execute_arbitrary(connection_query,
                                   dtype=connection_dtype)

    print result
    print len(result)

