from EADBWrapper import EADBWrapper

if __name__ == "__main__":

    dbo = EADBWrapper()
    objID = dbo.objectIdFromName('Secondary (M2) Adjustment')
    print objID
