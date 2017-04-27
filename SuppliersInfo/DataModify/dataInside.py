"""
    @description:   
    @author:        RoyalClown
    @date:          2017/4/24
"""
import cx_Oracle

from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.DBConnection.Constant import Manage_Oracle_Url


def dec_str(func):
    def wrapper(self, str_list):
        modify_str_list = []
        special_characters = "“”�ɽʯ�_!#$.=-〓*＊\"'<>《》,.\\，。\ue29c\ue29b\ue2f1\ue006\u3000\ue000\ue020\ue236★"
        for single_str in str_list:
            for special_character in special_characters:
                single_str = single_str.replace(special_character, "")

            modify_str = single_str.replace("None", "").replace("null", "").strip()
            modify_str_list.append(modify_str)
        return func(self, modify_str_list)

    return wrapper


class DataInside:
    def __init__(self):
        pass

    def get_data(self):
        import os

        os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
        conn = cx_Oracle.connect(Manage_Oracle_Url)
        cursor = conn.cursor()
        cursor.execute(
            "select /*+ first_rows */ ADMINNAME,name,SHORTNAME,INDUSTRY,tel,address,type from ac$us$detail where modifystatus is null and rownum<10000 order by id")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def modify_data(self, init_row):
        special_characters = "“”�ɽʯ�_!#$.=-〓*＊\"'<>《》,.\\，。\ue29c\ue29b\ue2f1\ue006\u3000\ue000\ue020\ue236\u3000★"
        row = []
        for column in init_row:
            for special_character in special_characters:
                try:
                    column = column.replace(special_character, "")
                except:
                    column = ""
            try:
                column = column.replace("None", "").replace("null", "").strip()
            except:
                column = ""
            row.append(column)

        conn = cx_Oracle.connect(Manage_Oracle_Url)
        cursor = conn.cursor()
        if not row[1]:
            cursor.execute("delete from ac$us$detail where name='{}'".format(init_row[1]))
        elif row == init_row:
            cursor.execute("update ac$us$detail set modifystatus=0 where name='{}'".format(init_row[1]))
        else:
            sql = "update ac$us$detail set adminname='{}',name='{}',shortname='{}',industry='{}',tel='{}',address='{}',type='{}',modifystatus=1 where name='{}'".format(
                    *row, init_row[1].replace("'", "''"))
            cursor.execute(sql)
        print(row, init_row, (row == init_row))
        cursor.close()
        conn.commit()
        conn.close()


if __name__ == "__main__":
    while True:
        data_inside = DataInside()
        rows = data_inside.get_data()
        if not rows:
            break
        # for row in rows:
        #     data_inside.modify_data(row)

        threadingpool = ThreadingPool(8)
        threadingpool.multi_process(data_inside.modify_data, rows)
