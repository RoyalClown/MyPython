from DataAnalyse.dbDataGet.Constant import UserJson
from DataAnalyse.valueProcessing.propertyValueModify import PropertyValueModify
from Lib.DBConnection.OracleConnection import OracleConnection


class UtilDataAnalyse(OracleConnection):
    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__()

    # 获取爬虫任务信息
    def get_from_table(self):
        cursor = self.conn.cursor()
        cursor.execute("select * from product$component_crawl_task where cct_id={}".format(self.task_id))
        table_data = str(cursor.fetchone()[-3])
        cursor.close()
        return eval(table_data)

    # 获得此次任务所有爬取的器件信息
    def get_all_components(self):
        cursor = self.conn.cursor()
        cursor.execute("select * from product$component_crawl where cc_task={}".format(self.task_id))
        components = cursor.fetchall()
        cursor.close()

        return components

    # 获得爬虫表中单个器件的所有属性信息
    def get_single_properties(self, componentid):
        cursor = self.conn.cursor()
        cursor.execute(
            "select * from product$propertyvalue_crawl where pvc_componentid={}".format(
                componentid))
        properties = cursor.fetchall()
        cursor.close()
        return properties

    # 查询正式数据库中是否存在同品牌同型号器件
    def find_component(self, brid, code):
        cursor = self.conn.cursor()
        cursor.execute("select * from product$component where cmp_brid={} and cmp_code='{}'".format(brid, code))
        component = cursor.fetchone()
        cursor.close()
        return component

    # 如果不存在，则重新生成uuid
    def make_uuid(self, kiid):
        cursor = self.conn.cursor()
        cursor.execute("select ki_cmpprefix,ki_cmpsuffix from product$kind where ki_id={}".format(kiid))
        data = cursor.fetchone()
        cursor.execute(
            "update product$kind k set ki_count=(k.ki_count+1),ki_cmpsuffix=(k.ki_cmpsuffix+1) where ki_id={}".format(
                kiid))
        cursor.close()
        cmpprefix = data[0]
        cmpsuffix = data[1]
        lenth = 16 - len(cmpprefix) - len(str(cmpsuffix))
        uuid = cmpprefix + '0' * lenth + str(cmpsuffix)
        return uuid

    # 将新器件信息存入正式数据库
    def save_to_component(self, code, kiid, brid, cmp_uuid, attach, img, version=1):
        cursor = self.conn.cursor()
        cursor.execute(
            "select to_timestamp(to_char(sysdate, 'yyyy-mm-dd hh24:mi:ss'),'YYYY-MM-DD HH24:MI:SS')  from dual")
        modify_time = cursor.fetchone()[0]
        if version > 1:
            cursor.execute("select cmp_definetime from product$component_version where cmp_uuid='{}'".format(cmp_uuid))
            rough_define_time = cursor.fetchone()
            if rough_define_time is None:
                define_time = modify_time
            else:
                define_time = rough_define_time[0]
        else:
            define_time = modify_time
        cursor = self.conn.cursor()
        cursor.execute("select product$component_seq.nextval from dual")
        component_id = cursor.fetchone()[0]
        cursor.execute(
            "insert into product$component(cmp_id, cmp_code,cmp_unit,cmp_version,cmp_kiid,cmp_brid,cmp_uuid,cmp_attach,cmp_img,cmp_createtime,cmp_modifytime) values({},'{}','PCS',{},{},{},'{}','{}','{}',to_timestamp('{}','YYYY-MM-DD HH24:MI:SS'),to_timestamp('{}','YYYY-MM-DD HH24:MI:SS'))".format(
                component_id, code, version, kiid, brid, cmp_uuid, attach, img, define_time, modify_time))
        cursor.close()
        return component_id

    # 取得所有标准属性，已弃用
    # def get_all_base_propertyies(self, kindid):
    #     cursor = self.conn.cursor()
    #     cursor.execute(
    #         "select * from product$kindproperty where KP_KINDID={} order by KP_DETNO".format(kindid))
    #     all_base_properties = cursor.fetchall()
    #     cursor.close()
    #     return all_base_properties

    # 将所有标准属性数据进行处理后存入属性表
    def save_to_property(self, pv_propertyid, pv_componentid, pv_detno, pv_value, pv_unit='null', pv_numberic='null',
                         pv_min='null', pv_max='null', pv_flag=10):
        cursor = self.conn.cursor()
        cursor.execute("select product$propertyvalue_seq.nextval from dual")
        pv_id = cursor.fetchone()[0]
        cursor.close()

        cursor = self.conn.cursor()
        sql = "insert into product$propertyvalue(pv_id, pv_propertyid, pv_componentid, pv_detno, pv_value, pv_unit, pv_numberic, pv_min, pv_max, pv_flag) values ({},{},{},{},{},{},{},{},{},'{}')".format(
            pv_id, pv_propertyid, pv_componentid, pv_detno, pv_value, pv_unit, pv_numberic, pv_min, pv_max,
            pv_flag)

        cursor.execute(sql)
        cursor.close()
        return pv_id

    # 如果存在相同品牌、相同型号的器件，则删除原有器件
    def delete_old_component(self, uuid):
        cursor = self.conn.cursor()
        cursor.execute("delete from product$component where cmp_uuid='{}'".format(uuid))
        cursor.close()

    # 更新爬虫表的uuid
    def update_crawl_uuid(self, uuid, taskid, code, cc_modify, cc_flag):
        cursor = self.conn.cursor()
        cursor.execute(
            "update product$component_crawl set cc_uuid='{}', cc_flag={}, cc_modify={} where cc_task={} and cc_code='{}'".format(
                uuid, cc_flag, cc_modify, taskid, code))
        cursor.close()

    # 将标准属性信息和处理过的属性值封装为json格式
    def get_property_json(self, detno, pv_id, propertyid, propertylabelCn, stringValue, numberic='', unit='', min='',
                          max=''):
        property_json = {
            'detno': detno,
            'id': pv_id,
            'property': {
                'id': propertyid,
                'labelCn': propertylabelCn
            },
            'propertyid': propertyid,
            'stringValue': stringValue,
            'numberic': numberic,
            'unit': unit,
            'min': min,
            'max': max,
        }
        return property_json

    # 将器件所有信息包括所有期间基本信息，属性信息、类目信息、品牌信息、创建用户信息的json格式与版本号存入版本表中
    def save_to_version(self, cmp_code, cmp_attach, cmp_img, cmp_unit, cmp_uuid, cmp_properties_json, cmp_brand_json,
                        cmp_kind_json, cmp_version, cmp_user_json=UserJson):
        cursor = self.conn.cursor()
        cursor.execute(
            "select to_timestamp(to_char(sysdate, 'yyyy-mm-dd hh24:mi:ss'),'YYYY-MM-DD HH24:MI:SS')  from dual")
        modify_time = cursor.fetchone()[0]
        if cmp_version > 1:
            cursor.execute("select cmp_definetime from product$component_version where cmp_uuid='{}'".format(cmp_uuid))
            rough_define_time = cursor.fetchone()
            if rough_define_time is None:
                define_time = modify_time
            else:
                define_time = rough_define_time[0]
        else:
            define_time = modify_time
        cursor.execute("select product$propertyvalue_seq.nextval from dual")
        component_version_id = cursor.fetchone()[0]
        sql = \
            "insert into product$component_version(id, cmp_code, cmp_attach, cmp_img, cmp_unit, cmp_uuid, properties_json, brand_json, kind_json, cmp_version, cmp_defineuser_json, cmp_definetime, cmp_modify_date) values ({},'{}','{}','{}','{}','{}','{}','{}','{}',{},'{}',to_timestamp('{}','YYYY-MM-DD HH24:MI:SS'),to_timestamp('{}','YYYY-MM-DD HH24:MI:SS'))".format(
                component_version_id, cmp_code, cmp_attach, cmp_img, cmp_unit, cmp_uuid, cmp_properties_json,
                cmp_brand_json, cmp_kind_json, cmp_version, cmp_user_json, define_time, modify_time)
        cursor.execute(sql)
        cursor.close()

if __name__ == "__main__":
    main = DataProcessing()
    main.go(29)
