from EADBWrapper import EADBWrapper

if __name__ == "__main__":

    dbo = EADBWrapper()
    #objID = dbo.objectIdFromName('Secondary (M2) Adjustment')
    objID = dbo.objectIdFromName('Calibration of the Atmospheric Transmission')
    print objID
    nameList, objList, propDict = dbo.daughterObjectsFromID(objID[1])
    print nameList
    print objList
    print propDict
    dbo.showAttributesFromID(objList[0])
