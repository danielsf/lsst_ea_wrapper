from __future__ import with_statement
import os
import sys
import xml.etree.ElementTree as etree

prefix = "{http://schema.omg.org/spec/XMI/2.1}"
id_tag = '%sid' % prefix


def format_documentation(doc_string):
    n_char = 50+4
    doc_string = doc_string.replace('\n',' ')
    if len(doc_string)<n_char-4:
        return '    '+doc_string

    word_list = doc_string.split(' ')
    start_pt=0
    output_str = '    '
    last_broke = 0
    for word in word_list:
        if len(output_str)+len(word)>last_broke+n_char:
            output_str += '\n'
            output_str += '    '
            last_broke=len(output_str)

        output_str += word+' '

    return output_str


class ParameterTree(object):

    def __init__(self, fileName):
        tree = etree.parse(fileName)
        doc_dict, units_dict = self.generate_documentation_dict(tree)
        values_dict = self.get_values(tree)

        self.parameter_dict = {}
        for param_name in values_dict:
            local_dict = {}
            local_dict['values'] = values_dict[param_name]
            if param_name in doc_dict:
                local_dict['documentation'] = format_documentation(doc_dict[param_name])
            if param_name in units_dict:
                local_dict['units'] = units_dict[param_name]
            else:
                local_dict['units'] = ''

            self.parameter_dict[param_name] = local_dict


    def write_parameter(self, param_name, handle=sys.stdout):
        if param_name not in self.parameter_dict:
            return
        local_dict = self.parameter_dict[param_name]
        handle.write('\n%s\n' % param_name)
        if 'documentation' in local_dict:
            handle.write('%s\n' % local_dict['documentation'])
        handle.write('    ####\n')
        for val_name in local_dict['values']:
            vv = local_dict['values'][val_name]
            if isinstance(vv, unicode):
                vv = vv.encode(errors='ignore')
            handle.write('    '+val_name+': '+str(vv)+' '+str(local_dict['units'])+'\n')


    def generate_documentation_dict(self, tree):
        """
        Walk through an element tree, adding attributes to _documentation_dict
        """

        documentation_dict = {}
        units_dict = {}

        for ee in tree.iter():
            if ee.tag == 'attribute':
                for ii in ee:
                    if ii.tag== 'documentation' and 'value' in ii.attrib:
                        documentation_dict[ee.attrib['name']] = ii.attrib['value']
                    if ii.tag == 'properties' and 'type' in ii.attrib:
                        units_dict[ee.attrib['name']] = ii.attrib['type']

        return documentation_dict, units_dict


    def get_values(self, tree):
        """
        Walk through an element tree, finding all of the nestedClassifiers
        and getting their values
        """
        value_dict = {}

        for ee in tree.iter():
            if ee.tag == 'ownedAttribute' and 'name' in ee.attrib:
                name = ee.attrib['name']
                local_value_dict = self._get_values(ee)
                if local_value_dict is not None:
                    value_dict[name] = local_value_dict

        return value_dict


    def _get_values(self, element):
        """
        Return a dict of the default, upper, and lower values
        associated with an element
        """

        output = {}

        for ee in element:
            if ee.tag == 'defaultValue':
                output['defaultValue'] = ee.attrib['value']
            elif ee.tag == 'lowerValue':
                output['lowerValue'] = ee.attrib['value']
            elif ee.tag == 'upperValue':
                output['upperValue'] = ee.attrib['value']

        if len(output)==0:
            return None
        else:
            return output



if __name__ == "__main__":

    data_dir = os.path.join("/Users", "danielsf", "physics", "lsst_150412")
    data_dir = os.path.join(data_dir, "Development", "garage", "SysML")
    data_dir = os.path.join(data_dir, "xmi", "systematic_data")
    list_of_file_names = os.listdir(data_dir)

    tree_dict = {}
    for file_name in list_of_file_names:
        local_tree = ParameterTree(os.path.join(data_dir, file_name))
        tree_dict[file_name] = local_tree

    printed_params = {}

    with open("test_output.sav", "w") as output_file:

        for file_name in tree_dict:

            local_tree = tree_dict[file_name]

            for param_name in local_tree.parameter_dict:
                if param_name in printed_params:
                    print "WARNING %s in %s and %s\n" \
                    % (param_name, file_name, printed_params[param_name])

                    printed_params[param_name].append(file_name)
                else:
                    printed_params[param_name] = [file_name]

                local_tree.write_parameter(param_name, output_file)
