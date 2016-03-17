import sqlite3
import os

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
    for kw in keyword_list:
        if like_statement is None:
            like_statement = " WHERE name LIKE ?"
        else:
            like_statement += " OR name LIKE ?"

    cursor = _global_connection_cache.connect(db_name).cursor()

    cmd+=like_statement

    list_of_chars = ["%{}%".format(kw) for kw in keyword_list]

    cursor.execute(cmd, tuple(list_of_chars))
    return cursor.fetchall()
