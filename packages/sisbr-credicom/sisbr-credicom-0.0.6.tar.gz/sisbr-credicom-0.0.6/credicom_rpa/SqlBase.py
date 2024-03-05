import pyodbc


class ObjetoDinamico():
    def __init__(self, row, fields):
        for field in fields:
            setattr(self, field, getattr(row, field))


class CursorByName():
    def __init__(self, cursor):
        self._cursor = cursor
    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()
        propiedades = []
        for description in enumerate(self._cursor.description):
            propiedades.append(description[1][0])
        return ObjetoDinamico(row, propiedades)


class SqlBase(object):
    def __init__(self, connectionString):
        self.__connectionString = connectionString

    def __getConnection(self):
        connStr = self.__connectionString
        try:
            return pyodbc.connect(connStr)
        except Exception as err:
            print(err)
            raise TypeError(f"Erro ao estabelecer conexão: {connStr}")

    def execute(self, strQuery, dataRow):
        con = self.__getConnection()
        cursor = con.cursor()
        if dataRow:
            cursor.execute(strQuery, dataRow)
        else:
            cursor.execute(strQuery)
        cursor.commit()
        con.close()

        
    def read(self, strQuery, dataRow = None):
        data = []
        con = self.__getConnection()
        cursor = con.cursor()
        if dataRow:
            cursor.execute(strQuery, dataRow)
        else:
            cursor.execute(strQuery)
        for row in CursorByName(cursor):
            data.append(row)
        cursor.commit()
        con.close()
        return data

    def execProc(self, strQuery, dataRow = None):
        data = []
        con = self.__getConnection()
        cursor = con.cursor()
        con.autocommit = True
        if dataRow:
            cursor.execute(strQuery, dataRow)
        else:
            cursor.execute(strQuery)
        for row in CursorByName(cursor):
            data.append(row)
        cursor.commit()
        con.close()
        return data
    

       
