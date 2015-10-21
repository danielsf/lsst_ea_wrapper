from EADBWrapper import EADBWrapper, SysMLObject

if __name__ == "__main__":

    objectName = 'm3Presciption'

    dbo = EADBWrapper()
    objid = dbo.objectIdFromName(objectName)
    print '\nAvailable Object_IDs for %s: ' % objectName,objid
    print '\n------------------\n'
    obj = SysMLObject()
    obj.getData(dbo, objid[0])
    obj.printObject()
