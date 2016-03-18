import sqlite3
import os

from ParameterTree import Parameter
from ParameterDB_constructor import parameter_db_name

__all__ = ["get_table_names", "get_column_names", "keyword_query"]

class connection_cache(object):

    def __init__(self):
        self._connection_dict = {}

    def connect(self, file_name):
        if file_name in self._connection_dict:
            return self._connection_dict[file_name]

        conn = sqlite3.connect(file_name)
        self._connection_dict[file_name] = conn
        return conn

_global_connection_cache = connection_cache()


def _convert_row_to_parameter(row):
    name = row[0]
    values = {'defaultValue':row[1],
               'upperValue':row[2],
               'lowerValue':row[3]}

    if str(row[4]) != 'NULL':
        units = row[4]
    else:
        units = None

    if str(row[5]) != 'NULL':
        doc = row[5]
    else:
        doc = None

    if str(row[6]) != 'NULL':
        source = row[6]
    else:
        source = None

    return Parameter(name, doc=doc, units=units, values=values, source=source)

def get_table_names(db_name):
    cursor = _global_connection_cache.connect(db_name).cursor()
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor.execute(query)
    results = cursor.fetchall()
    return results


def get_column_names(db_name, table_name):
    if ')' in table_name:
        raise RuntimeError("%s is not a valid table_name" % table_name)
    cursor = _global_connection_cache.connect(db_name).cursor()
    cursor.execute("PRAGMA table_info(%s)" % table_name)
    raw_results = cursor.fetchall()
    results = []
    for rr in raw_results:
        results.append(rr[1])
    return results


def keyword_query(db_name, table_name, keyword_list):
    cmd = "SELECT * from %s" % table_name
    like_statement = None
    formatted_kw_list = []
    list_of_chars = []
    for kw in keyword_list:
        list_of_chars.append("%{}%".format(kw))
        list_of_chars.append("%{}%".format(kw))
        if like_statement is None:
            like_statement = " WHERE name LIKE ? OR docstring like ?"
        else:
            like_statement += " OR name LIKE ? OR docstring like ?"

    cursor = _global_connection_cache.connect(db_name).cursor()

    cmd+=like_statement

    cursor.execute(cmd, tuple(list_of_chars))
    results = cursor.fetchall()
    output = []
    for rr in results:
        output.append(_convert_row_to_parameter(rr))
    return output
