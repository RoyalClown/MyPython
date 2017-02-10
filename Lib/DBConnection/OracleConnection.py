import cx_Oracle

from Lib.DBConnection.Constant import Oracle_Url
import os

os.environ["NLS_LANG"] = ".AL32UTF8"


class OracleConnection:
    # 存储数据
    def __init__(self, ):
        self.conn = cx_Oracle.connect(Oracle_Url)

    def retrieve(self):
        pass

    # 接受处理之后的数据data
    def insert(self, sql):
        cursor = self.conn.cursor()
        insert_data = cursor.execute(sql)
        cursor.close()
        return insert_data
