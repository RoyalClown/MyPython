import time
from pymongo import MongoClient

from Lib.DBConnection.Constant import Mongo_Url


class MongoConnection:
    def __init__(self):
        conn = MongoClient(*Mongo_Url)
        self.db = conn.spider
        # self.col = self.db.Company_Info
        self.col = self.db.Company_Info_Test

    def db_create(self, data):
        print(data)
        self.col.insert(data)
        return

    def db_retrieve_all(self):
        try:
            data = self.col.find()
            return data
        except:
            print("查询全部数据失败")

    def db_retrieve(self, data):
        try:
            data = self.col.find(data)
            return data
        except:
            print("查询数据失败")

    def db_update(self, data, new_data):
        try:
            self.col.update({data}, {'$set': {new_data}})
        except:
            print("更新数据失败")
        return new_data

    def db_delete(self, data):
        try:
            self.col.remove({data})
        except:
            print("删除数据失败")

        return


if __name__ == "__main__":
    # connection = MongoConnection()
    mongo_conn = MongoClient("10.10.101.22", 27017)
