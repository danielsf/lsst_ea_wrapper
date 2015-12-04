from __future__ import with_statement
from EADBWrapper import EADBWrapper, SysMLObject
from collections import OrderedDict

if __name__ == "__main__":

    dbo = EADBWrapper()

    id_dict = OrderedDict()

    # The Object_ID's below were just assembled heuristically by manually
    # inspecting the sysarch database.  Once we have made the schema more
    # uniform, we ought to be able to find these automatically by searching
    # for desired component names.
    id_dict['m1'] = 385259
    id_dict['m2'] = 385268
    id_dict['m3'] = 385279
    id_dict['l1'] = 385271
    id_dict['l2'] = 385283
    id_dict['filter'] = 385275
    id_dict['l3'] = 385276

    with open('trial_optics.txt', 'w') as output_file:
        for name in id_dict:
            output_file.write('\n%s %d\n' % (name, id_dict[name]))
            obj = SysMLObject()
            obj.getData(dbo, id_dict[name])
            for att in obj.attributes:
                output_file.write('%s %s %s %s\n'
                                  % (att, obj.attributes[att]['Default'],
                                     obj.attributes[att]['Type'],
                                     obj.attributes[att]['Notes']))

