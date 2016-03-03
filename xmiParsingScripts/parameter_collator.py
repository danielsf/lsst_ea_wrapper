from __future__ import with_statement
import os

from ParameterTree import Parameter, ParameterTree, write_keyword_params

if __name__ == "__main__":

    data_dir = os.path.join("/Users", "danielsf", "physics", "lsst_150412")
    data_dir = os.path.join(data_dir, "Development", "garage", "SysML")
    data_dir = os.path.join(data_dir, "xmi", "systematic_data")
    list_of_file_names = os.listdir(data_dir)

    tree_list = []
    for file_name in list_of_file_names:
        local_tree = ParameterTree(os.path.join(data_dir, file_name))
        tree_list.append(local_tree)

    printed_params = {}

    with open("test_output.sav", "w") as output_file:

        for local_tree in tree_list:

            for param in local_tree.parameter_list:
                param.write_param(output_file)

                if param.name not in printed_params:
                    printed_params[param.name] = [param.source]
                else:
                    print "WARNING %s in %s and %s" % \
                    (param.name, param.source, printed_params[param.name])

                    printed_params[param.name].append(param.source)

    with open("test_kinematic_parameters.sav", "w") as output_file:
        for local_tree in tree_list:
            write_keyword_params(local_tree.parameter_list,
                                ['rotator', 'rotation', 'accel', 'veloc'],
                                output_file)
