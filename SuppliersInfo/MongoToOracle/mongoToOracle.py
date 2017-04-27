"""
    @description:   
    @author:        RoyalClown
    @date:          2017/2/21
"""

import cx_Oracle
import sys
from pymongo import MongoClient

from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.DBConnection.Constant import Manage_Oracle_Url


def dec_str(func):
    def wrapper(self, str_list):
        special_characters = "��_!#$.=-〓*＊\"'<>《》,.\\，。\ue29c\ue29b\ue2f1\ue006\u3000\ue000\ue020★"
        modify_str_list = []
        for single_str in str_list:
            for special_character in special_characters:
                single_str = single_str.replace(special_character, "")

            modify_str = single_str.replace("None", "").replace("null", "").strip()
            modify_str_list.append(modify_str)
        return func(self, modify_str_list)

    return wrapper


class MongoToOracle:
    def __init__(self):
        pass

    @dec_str
    def oracle_save(self, company):
        while True:
            try:
                conn = cx_Oracle.connect(Manage_Oracle_Url)
                cursor = conn.cursor()
                company_id = cursor.execute("select AC$US$DETAIL_SEQ.nextval from dual").fetchone()[0]
                sql_sentence = "insert into ac$us$detail(id, name, businessCode, address, corporation, tel, type, industry, " \
                               "adminName, adminTel, adminEmail, orgCode, email, fromTime, toTime, regStatus, approvedTime, " \
                               "estiblishTime, regCapital, businessScope, regInstitute, spider) values ({},'{}','{}','{}','{}','{}'," \
                               "'{}','{}','{}','{}','{}','{}','{}'," \
                               "to_timestamp(TO_CHAR({} / (1000 * 60 * 60 * 24) + TO_DATE('1970-01-01 08:00:00', 'YYYY-MM-DD HH:MI:SS'), 'YYYY-MM-DD HH:MI:SS'),'YYYY-MM-DD HH24:MI:SS')," \
                               "to_timestamp(TO_CHAR({} / (1000 * 60 * 60 * 24) + TO_DATE('1970-01-01 08:00:00', 'YYYY-MM-DD HH:MI:SS'), 'YYYY-MM-DD HH:MI:SS'),'YYYY-MM-DD HH24:MI:SS')," \
                               "'{}'," \
                               "to_timestamp(TO_CHAR({} / (1000 * 60 * 60 * 24) + TO_DATE('1970-01-01 08:00:00', 'YYYY-MM-DD HH:MI:SS'), 'YYYY-MM-DD HH:MI:SS'),'YYYY-MM-DD HH24:MI:SS')," \
                               "to_timestamp(TO_CHAR({} / (1000 * 60 * 60 * 24) + TO_DATE('1970-01-01 08:00:00', 'YYYY-MM-DD HH:MI:SS'), 'YYYY-MM-DD HH:MI:SS'),'YYYY-MM-DD HH24:MI:SS')," \
                               "'{}','{}','{}','LYJ')".format(company_id, *company)
                print(company)
                cursor.execute(sql_sentence)
                cursor.close()
                conn.commit()
                conn.close()
                break
            except Exception as e:
                print(e)

    def data_to_oracle(self, data):
        url = data["url"]
        data = data["data"]
        if data == 'too fast':
            while True:
                try:
                    mongo_conn = MongoClient("10.10.101.22", 27017)
                    col = mongo_conn.spider.All_Company_Info
                    col.update_many({"url": url}, {'$set': {"入库": "数据错误"}})
                    mongo_conn.close()
                    return
                except Exception as e:
                    print(sys._getframe().f_code.co_name, e)

        base_info = data.get("baseInfo")
        if base_info:

            regInstitute = base_info.get("regInstitute")
            regCapital = base_info.get("regCapital")
            regStatus = base_info.get("regStatus")
            name = base_info.get("name")
            businessScope = base_info.get("businessScope")
            estiblishTime = base_info.get("estiblishTime")
            if not estiblishTime:
                estiblishTime = 0
            address = base_info.get("regLocation")
            type = base_info.get("companyOrgType")
            businessCode = base_info.get("creditCode")
            tel = base_info.get("phoneNumber")
            email = base_info.get("email")
            industry = base_info.get("industry")
            corporation = base_info.get("legalPersonName")
            orgCode = base_info.get("orgNumber")

            fromTime = base_info.get("fromTime")
            if not fromTime:
                fromTime = 0
            toTime = base_info.get("toTime")
            if not toTime:
                toTime = 0
            approvedTime = base_info.get("approvedTime")
            if not approvedTime:
                approvedTime = 0

        else:
            approvedTime = data.get("approvedTime")
            if not approvedTime:
                approvedTime = 0
            businessScope = data.get("businessScope")
            type = data.get("companyOrgType")
            businessCode = data.get("creditCode")
            email = data.get("email")
            estiblishTime = data.get("estiblishTime")
            if not estiblishTime:
                estiblishTime = 0
            fromTime = data.get("fromTime")
            if not fromTime:
                fromTime = 0
            industry = data.get("industry")
            corporation = data.get("legalPersonName")
            name = data.get("name")
            orgCode = data.get("orgNumber")
            tel = data.get("phoneNumber")
            regCapital = data.get("regCapital")
            regInstitute = data.get("regInstitute")
            address = data.get("regLocation")
            regStatus = data.get("regStatus")
            toTime = data.get("toTime")
            if not toTime:
                toTime = 0
        adminName = corporation
        adminTel = tel
        adminEmail = email

        if not name:
            while True:
                try:
                    mongo_conn = MongoClient("10.10.101.22", 27017)
                    col = mongo_conn.spider.All_Company_Info
                    col.update_many({"url": url}, {'$set': {"入库": "数据错误"}})
                    mongo_conn.close()
                    return
                except Exception as e:
                    print(sys._getframe().f_code.co_name, e)

        company = (
            name, businessCode, address, corporation, tel, type, industry, adminName, adminTel, adminEmail, orgCode,
            email, fromTime, toTime, regStatus, approvedTime, estiblishTime, regCapital, businessScope, regInstitute)

        modify_company = []
        for company_property in company:
            try:
                modify_property = str(company_property).replace("'", '"').replace("\u3000", "").replace("\xa0", "").replace("�", "")
            except:
                modify_property = company_property
            modify_company.append(modify_property)
        self.oracle_save(modify_company)
        while True:
            try:
                mongo_conn = MongoClient("10.10.101.22", 27017)
                col = mongo_conn.spider.All_Company_Info
                col.update_many({"url": url}, {'$set': {"入库": "已完成"}})
                mongo_conn.close()
                break
            except Exception as e:
                print(e)
        return

    def get_mongo_data(self):
        conn = MongoClient("10.10.101.22", 27017)
        col = conn.spider.All_Company_Info
        datas = col.find({"入库": None, "状态": "已完成"})
        conn.close()
        return datas
if __name__ == "__main__":
    import os

    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    while True:
        try:
            mongo_to_oracle = MongoToOracle()
            conn = MongoClient("10.10.101.22", 27017)
            col = conn.spider.All_Company_Info
            """
                Hayley Westenra
            """
            # threadingpool = ThreadingPool(4)
            # threadingpool.multi_thread(mongo_to_oracle.data_to_oracle, col.find({"入库": None, "状态": "已完成"}))

            for data in col.find({"入库": None, "状态": "已完成"}):
                mongo_to_oracle.data_to_oracle(data)
            conn.close()
            break
        except:
            continue
