from mysql.connector import connect, Error
from config import *


class DB:
    _config = None
    _connection = None
    _cursor = None
    _dict_cursor = None

    def __init__(self, host, user, password, database, port='3306'):
        self._config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': port,
            'autocommit': True,
        }
        self.__connect()

    def __connect(self):
        try:
            self._connection = connect(**self._config)
            self._cursor = self._connection.cursor()
            self._dict_cursor = self._connection.cursor(dictionary=True)
            return True
        except Error:
            self._connection = None
            return False

    def query(self, sql, params=None, simple=True, retry=True):
        try:
            cursor = self._cursor if simple else self._dict_cursor
            cursor.execute(sql, params)
            return cursor.fetchall()
        except Error as e:
            print('Error occurred in MySQL', e.msg, 'Try to reconnect')
            if retry and self.__connect():
                return self.query(sql, params, simple, False)
            print('Reconnection failed! End sql and params: ', end='')
            print(sql)
            print(params)
            return False


db = DB(DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT)
