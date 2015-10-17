from EADBWrapper import EADBWrapper

if __name__ == "__main__":

    dbo = EADBWrapper()
    objID = dbo.objectIdFromName('Secondary (M2) Adjustment')
    print objID
    nameList, objList, propList = dbo.daughterObjectsFromID(objID[0])
    print nameList
    print objList
    print propList
    dbo.showAttributesFromID(objList[0])
