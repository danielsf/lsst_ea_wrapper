from __future__ import with_statement
from EADBWrapper import EADBWrapper, SysMLObjectList

if __name__ == "__main__":

    name = 'g-band Response Envelope'
    dbo = EADBWrapper()
    with open('test_output.txt', 'w') as output:
        dbo.writeFamilyTree(name, author='Chuck Claver', file_handle=output)
