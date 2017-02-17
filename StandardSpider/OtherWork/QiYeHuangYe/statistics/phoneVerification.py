"""
    @description:   
    @author:        RoyalClown
    @date:          2017/2/17
"""
from pymongo import MongoClient


class PhoneVerification:
    def __init__(self):
        pass

    def phone_verification(self):
        mongo_conn = MongoClient("10.10.101.22", 27017)
        col = mongo_conn.spider.All_Company_Info
        datas = col.find({"状态": "已完成"})
        phone_nums = ""
        for data in datas:
            base_info = data["data"]["baseInfo"]
            company_name = base_info["name"]
            try:
                phone_num = base_info["phoneNumber"]
            except Exception as e:
                print(e)
                phone_num = "null"
            phone_nums += company_name + "," + phone_num + "\n"

        with open("..//statistics//phone_num.csv", "wb") as f:
            f.write("公司名称,电话号码\n".encode())
            f.write(phone_nums.encode())
        return

if __name__ == "__main__":
    phone_verification = PhoneVerification()
    phone_verification.phone_verification()