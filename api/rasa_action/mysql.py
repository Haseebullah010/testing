import pymysql.cursors
import pymysql

class DB(object):
    __instance = None
    __host = None
    __user = None
    __password = None
    __database = None
    __cursor = None
    __connection = None
    
    def __init__(self, host='localhost', user='root', password='', database='rasa'):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
    
    def __open(self):

        try:
            self.__connection = pymysql.connect(host=self.__host, user=self.__user, password=self.__password, db=self.__database, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
            self.__cursor = self.__connection.cursor()

        except psycopg2.DatabaseError as e:
            if self.__connection:
                    self.__connection.rollback()
            print('Error %s' % e)
            sys.exit(1)
            
    def callStore(self, store_name, params):
        self.__open()
        result=[]
        try:
            with self.__connection.cursor() as cursor:
                cursor.callproc(store_name, params)            
                result = cursor.fetchall()
                self.__connection.commit()
        finally:
            self.__connection.close()
            return result
        return result
            
    def insert(self, table_name, inserted_array ):
        insert_val = []
        if table_name :
            sql = "INSERT INTO "+table_name+" ("
            for key, value in inserted_array.items():
                sql += " `"+key+"`, ";
            sql = sql[:-2]
            sql += ") values ( "
            for key, value in inserted_array.items():
                sql += "%s, "
                insert_val.append(value)
            sql = sql[:-2]
            sql += " ) ";
            insert_id = -1
            try:
                with self.connector.cursor() as cursor:
                    cursor.execute(sql, insert_val)            
                    insert_id = cursor.execute('select last_insert_id() from '+table_name)
                    self.connector.commit()
            finally:
                self.connector.close()
                return insert_id
            return insert_id
        
    def fetchRow(self, table_name, collum_name, where_arr = []):
        where_cond = ' WHERE 1'
        insert_val = result = responce = []
        try:
            with self.connector.cursor() as cursor:
                sql = "SELECT "

                for collums in collum_name:
                    sql += "`"+collums+"`, ";                
                sql = sql[:-2]
                sql += " FROM "+table_name
                if where_arr:
                    for key, value in where_arr.items():
                        where_cond += ' and `'+key+'`= %s'

                    for key, value in where_arr.items():
                        insert_val.append(value)

                sql = sql+where_cond
                cursor.execute(sql, (insert_val))
                result = cursor.fetchone()
                responce = result
        finally:
            self.connector.close()
            
        return responce
    
    def fetchAll(self, table_name, collum_name, where_arr = []):
        where_cond = ' WHERE 1'
        insert_val = result = responce = []
        try:
            with self.connector.cursor() as cursor:
                sql = "SELECT "

                for collums in collum_name:
                    sql += "`"+collums+"`, ";                
                sql = sql[:-2]
                sql += " FROM "+table_name
                if where_arr:
                    for key, value in where_arr.items():
                        where_cond += ' and `'+key+'`= %s'

                    for key, value in where_arr.items():
                        insert_val.append(value)

                sql = sql+where_cond
                cursor.execute(sql, (insert_val))
                result = cursor.fetchall()
                responce = result
        finally:
            self.connector.close()
            
        return responce
    
    def updateTable(self, table_name = '', updated_val = [], where_arr = []):
        responce = where_final_arr = [];
        sql = collum_str = where_str = ""
        try:
            with self.connector.cursor() as cursor:
                if table_name :
                    for key,value in updated_val.items():
                        collum_str = '`'+key+'` = "'+value+'", '

                    collum_str = collum_str[:-2]
                    for key, value in where_arr.items():
                        where_str = ' and `'+key+'` = %s'
                        where_final_arr.append(value)

                    sql = "update "+table_name+" set "+collum_str+" where 1 "+where_str
                    cursor.execute(sql, (where_final_arr))
                    self.connector.commit()
                    responce = {"message": "updated succesfully" }
                else:
                    responce = {"type":False, "message": "Provide valid table name" }
        finally:
            self.connector.close()
        return responce;
    
    def delete(self, table_name = '', where_arr = []):
        responce = where_final_arr = []
        sql = where_str = '';
        deleted_row_count = 0
        for key, value in where_arr.items():
            where_str = ' and `'+key+'` = %s'
            where_final_arr.append(value)
        if table_name:
            sql = "DELETE FROM `"+table_name+"` "
            try:
                with self.connector.cursor() as cursor:
                    sql = sql+" where 1 "+where_str;
                    tmp = cursor.execute(sql, (where_final_arr))
                    deleted_row_count = cursor.rowcount
                    self.connector.commit()
            finally:
                self.connector.close()
                return deleted_row_count
       
        return deleted_row_count