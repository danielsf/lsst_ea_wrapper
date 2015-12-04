from __future__ import with_statement
import numpy as np
import re
from EADBWrapper import EADBWrapper, SysMLObject
from collections import OrderedDict

def parseComponents(obj, bandpass):
    """
    Read in a SysMLObject and divide it into a list of parameters in the order
    and units expected for optics_0.txt

    If the SysMLObject contains information for two surfaces, the results will
    be broken into two lists, one for each surface.

    Results returned as a list of lists.
    """

    bandpass_to_dex = {'u':0, 'g':1, 'r':2, 'i':3, 'z':4, 'y':5}

    output = []
    first_surface = []
    second_surface = None

    for att in obj.attributes:
        if 'second surface' in obj.attributes[att]['Notes']:
            second_surface = []
            break

    name_root = None
    allowed = ('L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'F')
    for att in obj.attributes:
        name = att[:2].upper()
        if name[0] is 'F':
            name = 'F'
        if name in allowed:
            name_root = name
            break

    if name_root is None:
        return []

    first_surface.append(name_root)
    if second_surface is not None:
        second_surface.append(name_root+"E")

    type_dict = {'L':'lens', 'M':'mirror', 'F':'filter'}
    first_surface.append(type_dict[name_root[0]])
    if second_surface is not None:
        second_surface.append(type_dict[name_root[0]])

    # Populate first_surface and second_surface (if applicable) with
    # place holder values
    for ix in range(13):
        first_surface.append(0.0)
        if second_surface is not None:
            second_surface.append(0.0)

    media_dict = {}
    media_dict['M1'] = ('m1_protAl_Ideal.txt', 'air')
    media_dict['M2'] = ('m2_protAl_Ideal.txt', 'air')
    media_dict['M3'] = ('m3_protAl_Ideal.txt', 'air')
    for ll in ('L1', 'L2', 'L3'):
        media_dict[ll] = ('lenses.txt', 'silica_dispersion.txt')
        media_dict[ll+'E'] = ('lenses.txt', 'air')

    media_dict['F'] = ('filter_%d.txt' % bandpass_to_dex[bandpass], 'silica_dispersion.txt')
    media_dict['FE'] = ('none', 'air')

    first_surface.append(media_dict[first_surface[0]][0])
    first_surface.append(media_dict[first_surface[0]][1])
    if second_surface is not None:
        second_surface.append(media_dict[second_surface[0]][0])
        second_surface.append(media_dict[second_surface[0]][1])

    # Loop over the attributes in the SysMLObject and assign their values to
    # the correct positions in first_surface and second_surface
    for att_name in obj.attributes:
        notes = obj.attributes[att_name]['Notes']
        value = obj.attributes[att_name]['Default']

        if 'filter' in att_name:
            if '-band' in notes and '%s-band' % bandpass not in notes:
                continue

        if 'Infinite' in value:
            value = 0.0
        units = obj.attributes[att_name]['Type']
        active_surface = first_surface
        if 'second surface' in notes:
            active_surface = second_surface

        if 'radius of curvature' in notes or 'radius of the' in notes:
            active_surface[2] = np.abs(np.float(value))

        elif 'clear aperture' in notes:
            if 'inner' in notes:
                dex = 5
            else:
                dex = 4

            if 'diameter' in notes:
                factor = 0.5
            else:
                factor = 1.0

            active_surface[dex] = factor*np.abs(np.float(value))

        elif 'thicknes' in notes:
            if second_surface is not None:
                active_surface = second_surface

            active_surface[3] = np.abs(np.float(value))

        elif 'conic constant' in notes:
            active_surface[6] = np.float(value)

        elif 'aspheric' in notes:
            order_strings = re.findall("\d+.. order", notes)
            order = int(re.findall("\d+..", order_strings[0])[0][:-2])
            dex = order + 4
            active_surface[dex] = 0.001*np.float(value)


    output.append(first_surface)
    if second_surface is not None:
        output.append(second_surface)

    return output


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

    for ibp, bandpass in enumerate(('u', 'g', 'r', 'i', 'z', 'y')):

        with open('test_optics_%d.txt' % ibp, 'w') as output_file:
            for name in id_dict:
                obj = SysMLObject()
                obj.getData(dbo, id_dict[name])
                surface_list = parseComponents(obj, bandpass)
                for surface in surface_list:
                    output_file.write('%s %s ' % (surface[0], surface[1]))
                    for ix in range(2, 7):
                        output_file.write('%.3f ' % surface[ix])
                    for ix in range(7,15):
                        output_file.write('%.4e ' % surface[ix])
                    output_file.write('%s %s\n' % (surface[15], surface[16]))

