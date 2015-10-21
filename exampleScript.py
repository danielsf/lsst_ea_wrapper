from __future__ import with_statement
from EADBWrapper import EADBWrapper, SysMLObjectList

if __name__ == "__main__":

    dbo = EADBWrapper()
    #objID = dbo.objectIdFromName('Secondary (M2) Adjustment')
    #objID = dbo.objectIdFromName('Calibration of the Atmospheric Transmission')
    #print objID
    family = dbo.getFamilyIDs('Filter Complement', author='Chuck Claver')
    objList = SysMLObjectList(dbo, family)
    with open('test_output.txt', 'w') as output:
        objList.writeFamilyTree(file_handle=output)
