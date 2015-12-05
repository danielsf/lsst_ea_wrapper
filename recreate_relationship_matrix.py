from __future__ import with_statement
import numpy as np
from EADBWrapper import EADBWrapper

if __name__ == "__main__":

    eadbo = EADBWrapper()
    dbo = eadbo._dbo

    # Query t_connector for all of the connections between two properties
    # labeled as 'LSSTRequirement'

    connection_dtype = np.dtype([('Btm_Mid_Label', str, 300),
                                ('Start_Object_ID', np.int),
                                ('End_Object_ID', np.int)])

    connection_query = "select c.Btm_Mid_Label, c.Start_Object_ID, " \
                       + "c.End_Object_ID from t_connector c " \
                       + "inner join t_objectproperties p " \
                       + "on p.Object_ID = c.Start_Object_ID " \
                       + "where p.Property like '%lsstrequire%'"

    connection_list = dbo.execute_arbitrary(connection_query,
                                           dtype=connection_dtype)


    # Query t_object for all of the objects at either end of those
    # connections

    object_dtype = np.dtype([('Name', str, 300),
                             ('Object_ID', np.int)])

    object_query = "select distinct o.Name, o.Object_ID from t_object o " \
                   + "inner join t_connector c " \
                   + "on c.End_Object_ID=o.Object_ID " \
                   + "or c.Start_Object_ID=o.Object_ID " \
                   + "inner join t_objectproperties p " \
                   + "on p.Object_ID = c.Start_Object_ID " \
                   + "where p.Property like '%lsstrequire%'"

    object_list = dbo.execute_arbitrary(object_query,
                                        dtype=object_dtype)


    with open('test_matrix.txt', 'w') as output_file:
        for connection in connection_list:
            cc = connection['Btm_Mid_Label'].replace('\r','')
            cc = cc.replace('\n', '')
            cc = cc.strip()
            if cc != 'None':
            
                start_dex = np.where(object_list['Object_ID'] == connection['Start_Object_ID'])[0][0]
                end_dex = np.where(object_list['Object_ID'] == connection['End_Object_ID'])[0][0]
                start_name = object_list['Name'][start_dex].replace('\n','')
                start_name = start_name.replace('\r', '')
                end_name = object_list['Name'][end_dex].replace('\n','')
                end_name = end_name.replace('\r', '')
                output_file.write("%s %s %s\n" % (start_name, cc, end_name))
