import sqlite3
import os

from ParameterTree import Parameter

__all__ = ["db_from_param_list"]

def db_from_param_list(param_list, file_name):

    if os.path.exists(file_name):
        os.unlink(file_name)

    conn = sqlite3.connect(file_name)

    cc = conn.cursor()

    cc.execute(
        """CREATE TABLE parameters (name text, defaultValue text,
                                    upperValue text, lowerValue text,
                                    units text, docstring text)
        """
    )

    conn.commit()

    for param in param_list:
        name = param.name
        if 'defaultValue' in param.values:
           default = param.values['defaultValue']
        else:
            default = 'NULL'

        if 'upperValue' in param.values:
            upper = param.values['upperValue']
        else:
            upper = 'NULL'

        if 'lowerValue' in param.values:
            lower = param.values['lowerValue']
        else:
            lower = 'NULL'

        if param.doc is not None:
            doc = param.doc
        else:
            doc = 'NULL'

        if param.units is not None:
            units = param.units
        else:
            units = 'NULL'

        cc.execute("""INSERT INTO parameters VALUES(?, ?, ?, ?, ?, ?)""",
                   (name, default, upper, lower, units, doc))

    conn.commit()
    conn.close()
