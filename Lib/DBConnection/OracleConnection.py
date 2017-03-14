import cx_Oracle

from Lib.DBConnection.Constant import B2B_Oracle_Url
import os

os.environ["NLS_LANG"] = ".AL32UTF8"


class OracleConnection:
    # 存储数据
    def __init__(self, ):
        while True:
            try:
                self.conn = cx_Oracle.connect(B2B_Oracle_Url)
                break
            except Exception as e:
                print(e)

    def retrieve(self, sql_sentence):
        cursor = self.conn.cursor()
        cursor.execute(sql_sentence)
        retrieve_data = cursor.fetchall()
        return retrieve_data

    # 接受处理之后的数据data
    def insert(self, sql_sentence):
        cursor = self.conn.cursor()
        cursor.execute(sql_sentence)
        cursor.close()
        return

if __name__ == "__main__":
    oracle_connection = OracleConnection()
