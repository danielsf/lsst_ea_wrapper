import sys
import xml.etree.ElementTree as etree

__all__ = ["Parameter", "ParameterTree", "write_keyword_params"]

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


def _should_be_written(parameter, keyword):
    key = keyword.lower()
    if key in parameter.name.lower():
        return True

    if parameter.doc is not None:
        if key in parameter.doc.lower():
            return True

    return False


def write_keyword_params(list_of_params, keyword, handle=sys.stdout):

    for param in list_of_params:
        write_it = False
        if isinstance(keyword, list):
            for key in keyword:
                write_it = _should_be_written(param, key)
                if write_it:
                    break

        else:
            write_it = _should_be_written(param, keyword)

        if write_it:
            param.write_param(handle=handle)



class Parameter(object):

    def __init__(self, name, doc=None, units=None, values=None, source=None):
        self._name = name
        if doc is not None:
            self._doc = doc
        else:
            self._doc = None

        if units is not None:
            self._units = units
        else:
            self._units = ''

        if source is not None:
            words = source.split('/')
            self._source = words[-1]
        else:
            self._source = None

        self._values = {}
        for val_name in values:
            vv = values[val_name]
            if isinstance(vv, unicode):
                vv = vv.encode(errors='ignore')

            self._values[val_name] = vv


    def write_param(self, handle=sys.stdout):
        handle.write("\n%s\n" % self._name)
        if self._doc is not None:
            handle.write("%s\n" % format_documentation(self._doc))

        handle.write("    ####\n")
        for val_name in self._values:
            handle.write("    "+val_name+": "+self._values[val_name]
                         +" "+self._units+"\n")

        handle.write("    ####\n")
        handle.write("    %s\n" % self._source)

    @property
    def name(self):
        return self._name

    @property
    def doc(self):
        return self._doc

    @property
    def units(self):
        return self._units

    @property
    def source(self):
        return self._source

    @property
    def values(self):
        return self._values


class ParameterTree(object):

    def __init__(self, file_name):
        words = file_name.split('/')
        self.file_name = words[-1]
        tree = etree.parse(file_name)
        doc_dict, units_dict = self.generate_documentation_dict(tree)
        values_dict = self.get_values(tree)

        self.parameter_list = []

        for param_name in values_dict:
            if param_name in doc_dict:
                doc = doc_dict[param_name]
            else:
                doc = None
            if param_name in units_dict:
                units = units_dict[param_name]
            else:
                units = None

            pp = Parameter(param_name, doc=doc, units=units, values=values_dict[param_name],
                           source=file_name)

            self.parameter_list.append(pp)


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


