#!/usr/bin/env python3

'''
2024 - smaller.
'''
import os.path

from collections import OrderedDict
import sqlite3


class Maxims:

    def __init__(self):
        pdir = os.path.abspath(os.path.dirname(__file__))
        self.db = os.path.join(pdir, 'MightyMaxims2024.sqlt3')
        self.conn = None
        self.curs = None
        self.bOpen = False
        self.fields = OrderedDict([('ID', 'integer'), ('Author', 'text'), ('Quote', 'text')])
        self.table_name = 'MightyMaxims'
        
    @classmethod
    def get_fields(cls, value):
        if isinstance(value, dict) and 'ID' in value.keys():
            value = OrderedDict(value)
            del value['ID']
            return list(value.values())
        if isinstance(value, cls):
            return cls.get_fields(value.fields)
        return value
        
    def open(self):
        if self.bOpen is False:
            self.conn = sqlite3.connect(self.db)
            self.conn.row_factory = sqlite3.Row
            self.curs = self.conn.cursor()
            self.bOpen = True
        return True
        
    def close(self):
        if self.bOpen:
            self.conn.commit()
            self.bOpen = False
        return True
        
    def count(self):
        if self.bOpen:
            res = self.curs.execute("SELECT count(*) FROM MightyMaxims;")
            return res.fetchone()[0]
        return -1
        
    def select(self, sql_select):
        if self.bOpen:
            self.curs.execute(sql_select)
            zlist = self.curs.fetchall()
            for ref in zlist:
                try:
                    yield ref
                except:
                    pass
            return None



