import psycopg2
import sys

class PostgresDBMSCLS(object):

    __instance = None
    __host = None
    __user = None
    __password = None
    __database = None
    __cursor = None
    __connection = None

    def __new__(cls,host,user,password,database, *args, **kwargs):
        if not cls.__instance or not cls.__database:
            cls.__instance = super(PostgresDBMSCLS, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, host='localhost', user='nester', password='', database=''):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

    def __open(self):

        try:
            self.__connection = psycopg2.connect("host='{0}' dbname='{1}' user='{2}' password='{3}'".format(self.__host,self.__database,self.__user, self.__password))
            self.__cursor = self.__connection.cursor()

        except psycopg2.DatabaseError as e:
            if self.__connection:
                    self.__connection.rollback()
            print('Error %s' % e)
            sys.exit(1)

    def __close(self):
        self.__connection.close()
    
    def create_table(self, table_name, table_structure):

        query = "CREATE TABLE " + table_name + table_structure
        self.__open()
        self.__cursor.execute("DROP TABLE IF EXISTS {0}".format(table_name))
        self.__cursor.execute(query)
        self.__connection.commit()
        self.__close()
    
    def callStore(self, store_name, params):
        resultset=[]
        self.__open()
        self.__cursor.callproc(store_name, params)
        try:
            self.__open()
            self.__cursor.callproc(store_name, params)
            for buff in self.__cursor:
                row = {}
                c = 0
                for col in self.__cursor.description:
                    row.update({str(col[0]): buff[c]})
                    c += 1
                resultset.append(row)
            self.__connection.commit()
        finally:
            self.__close()
            return resultset
        return resultset
        
    def insert(self, table, *args, **kwargs):

        values = None
        query = 'INSERT INTO {0} '.format(table)
        if kwargs:
            keys = kwargs.keys()
            values = tuple(kwargs.values())
            query += "(" + ",".join(["%s"] * len(keys)) % tuple(keys) + \
                     ") VALUES (" + ",".join(["%s"]*len(values)) + ") RETURNING *"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"]*len(values)) + ") RETURNING *"
        self.__open()
        self.__cursor.execute(query, values)
        result = {}
        for buff in self.__cursor:
            c = 0
            for col in self.__cursor.description:
                result.update({str(col[0]): buff[c]})
                c += 1
        self.__connection.commit()
        self.__close()
        return result

    def select_one(self, table, where=None, *args, **kwargs):

        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1

        for i, key in enumerate(keys):
            query += key
            if i < l:
                query += ","

        query += ' FROM %s' % table

        if where:
            query += " WHERE {0}".format(where)
        self.__open()
        self.__cursor.execute(query, values)
        rows = {}
        for buff in self.__cursor:
            c = 0
            for col in self.__cursor.description:
                rows.update({str(col[0]): buff[c]})
                c += 1       
        #rows = self.__cursor.fetchall()
        self.__connection.commit()
        self.__close()
        return rows
     
    def select(self, table, where=None, other=None, *args, **kwargs):

        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += key
            if i < l:
                query += ","
        query += ' FROM %s' % table
        if where:
            query += " WHERE {0}".format(where)
        if other:
            query += " " + other
        self.__open()
        self.__cursor.execute(query, values)
        result_set = []
        for buff in self.__cursor:
            rows = {}
            c = 0
            for col in self.__cursor.description:
                rows.update({str(col[0]): buff[c]})
                c += 1
            result_set.append(rows)
        self.__connection.commit()
        self.__close()
        return result_set

    def select_all(self, table, other=None):
        self.__open()
        query = "SELECT * FROM {0}".format(table)
        if other:
            query += " " + other
        self.__cursor.execute(query)
        resultset=[]
        for buff in self.__cursor:
            row = {}
            c = 0
            for col in self.__cursor.description:
                row.update({str(col[0]): buff[c]})
                c += 1
            resultset.append(row)
        self.__connection.commit()
        self.__close()
        return resultset

    def delete(self, table, where=None, *args):
        query = "DELETE FROM {0}".format(table)
        if where:
            query += ' WHERE %s' % where + " RETURNING *"

        values = tuple(args)

        self.__open()
        self.__cursor.execute(query, values)
        result = {}
        for buff in self.__cursor:
            c = 0
            for col in self.__cursor.description:
                result.update({str(col[0]): buff[c]})
                c += 1
        self.__connection.commit()
        self.__close()
        return result

    def update(self, table, where=None, *args, **kwargs):

        query = "UPDATE %s SET " % table
        keys = kwargs.keys()
        values = tuple(kwargs.values()) + tuple(args)
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += key+" = %s"
            if i < l:
                query += ","

        query += " WHERE %s" % where + " RETURNING *"

        self.__open()
        self.__cursor.execute(query, values)
        result = {}
        for buff in self.__cursor:
            c = 0
            for col in self.__cursor.description:
                result.update({str(col[0]): buff[c]})
                c += 1
        self.__connection.commit()
        self.__close()
        return result