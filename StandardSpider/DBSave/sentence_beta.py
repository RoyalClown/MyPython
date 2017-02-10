import time
from threading import Timer

import cx_Oracle
import dill
from StandardSpider.DataAnalyse.valueProcessing.propertyValueModify import PropertyValueModify
from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.DBConnection.Constant import Oracle_Url
from Lib.DBConnection.OracleConnection import OracleConnection


def get_component2():
    conn = cx_Oracle.connect(Oracle_Url)
    cursor = conn.cursor()
    cursor.execute(
        "select /*+ first_rows */  cc_code, cc_b2c_brid, cc_b2c_kiid from product$component_crawl abc where cc_task = '9999999' and cc_b2c_brid is not null and cc_b2c_kiid is not null and cc_uuid is null and not exists (select 1 from product$component where abc.cc_code=cmp_code and abc.cc_b2c_brid=cmp_brid) and rownum < 10000")
    i = 0
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def thread_go(ls_return):
    conn = cx_Oracle.connect(Oracle_Url)
    try:
        for row in ls_return:
            cc_code = row[0]
            cc_b2c_brid = row[1]
            cc_b2c_kiid = row[2]
            # component = find_component(conn, cc_b2c_brid, cc_code)
            # if component:
            #     uuid = component[-1]
            #     update_crawl_uuid(conn, uuid=uuid, code=cc_code)
            #     continue
            # else:
            uuid = make_uuid(cc_b2c_kiid)
            component_id = save_to_component(conn, cc_code, cc_b2c_kiid, cc_b2c_brid, uuid)
            if not component_id:
                continue
            update_crawl_uuid(conn, uuid=uuid, code=cc_code)
            conn.commit()
            print("go")
        conn.close()
    except Exception as e:
        print(e)


# 更新爬虫表的uuid
def update_crawl_uuid(conn, uuid, code, taskid=7777777):
    cursor = conn.cursor()
    cursor.execute(
        "update product$component_crawl set cc_uuid='{}' where cc_task={} and cc_code='{}'".format(
            uuid, taskid, code))
    cursor.close()


# 查询正式数据库中是否存在同品牌同型号器件
def find_component(conn, brid, code):
    cursor = conn.cursor()
    cursor.execute("select * from product$component where cmp_brid={} and cmp_code='{}'".format(brid, code))
    component = cursor.fetchone()
    cursor.close()
    return component


# 如果不存在，则重新生成uuid
def make_uuid(kiid):
    conn = cx_Oracle.connect(Oracle_Url)
    cursor = conn.cursor()
    cursor.execute("select ki_cmpprefix,ki_cmpsuffix from product$kind where ki_id={}".format(kiid))

    data = cursor.fetchone()

    cursor.execute(
        "update product$kind k set ki_count=(k.ki_count+1),ki_cmpsuffix=(k.ki_cmpsuffix+1) where ki_id={}".format(
            kiid))
    cursor.close()

    conn.commit()
    conn.close()

    cmpprefix = data[0]
    cmpsuffix = data[1]
    lenth = 16 - len(cmpprefix) - len(str(cmpsuffix))
    uuid = cmpprefix + '0' * lenth + str(cmpsuffix)
    return uuid


# 将新器件信息存入正式数据库
def save_to_component(conn, code, kiid, brid, cmp_uuid, version=1):
    cursor = conn.cursor()
    cursor.execute(
        "select to_timestamp(to_char(sysdate, 'yyyy-mm-dd hh24:mi:ss'),'YYYY-MM-DD HH24:MI:SS')  from dual")
    modify_time = cursor.fetchone()[0]

    define_time = modify_time
    cursor = conn.cursor()
    cursor.execute("select product$component_seq.nextval from dual")
    component_id = cursor.fetchone()[0]
    try:
        cursor.execute(
            "insert into product$component(cmp_id, cmp_code,cmp_unit,cmp_version,cmp_kiid,cmp_brid,cmp_uuid,cmp_createtime,cmp_modifytime) values({},'{}','PCS',{},{},{},'{}',to_timestamp('{}','YYYY-MM-DD HH24:MI:SS'),to_timestamp('{}','YYYY-MM-DD HH24:MI:SS'))".format(
                component_id, code, version, kiid, brid, cmp_uuid, define_time, modify_time))
    except Exception as e:
        print(e)
        return None
    cursor.close()
    return component_id


def div_list(ls, n):
    if not isinstance(ls, list) or not isinstance(n, int):
        return []
    ls_len = len(ls)
    if n <= 0 or 0 == ls_len:
        return []
    if n > ls_len:
        return []
    elif n == ls_len:
        return [[i] for i in ls]
    else:
        j = int(ls_len / n)
        k = ls_len % n
        ### j,j,j,...(前面有n-1个j),j+k
        # 步长j,次数n-1
        ls_return = []
        for i in range(0, (n - 1) * j, j):
            ls_return.append(ls[i:i + j])
            # 算上末尾的j+k
        ls_return.append(ls[(n - 1) * j:])
        return ls_return


if __name__ == "__main__":
    while True:
        rows = get_component2()
        ls_return = div_list(rows, 20)
        if len(rows) == 0:
            break
        # for ls_ret in ls_return:
        #     thread_go(ls_ret)

        threadingpool = ThreadingPool()
        threadingpool.multi_process(thread_go, ls_return)
