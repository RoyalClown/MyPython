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


class DataProcessing:
    def go(self, task_id):
        # 合并
        spcap_data = UtilDataAnalyse(task_id=task_id)
        table_data = spcap_data.get_from_table()

        b2c_brand_json = str(table_data['b2cBrand']).replace("'", "\"")
        b2c_kind_json = str(table_data['b2cKind']).replace("'", "\"")

        b2c_brid = table_data['b2cBrId']
        b2c_kiid = table_data['b2cKiId']
        b2c_kind_name = table_data['kindName']

        base_properties = table_data['properties']
        resource = table_data['resource']
        url = table_data['url']
        unit = 'PCS'

        crawl_components = spcap_data.get_all_components()

        for crawl_component in crawl_components:
            # 爬取获得
            crawl_component_id = crawl_component[0]
            crawl_component_attach = crawl_component[2]
            crawl_component_img = crawl_component[4]
            crawl_component_url = crawl_component[13]
            crawl_component_code = crawl_component[7]
            cc_flag = crawl_component[17]
            # 事先给出

            # 查找确认是否存在同品牌同型号器件
            component = spcap_data.find_component(b2c_brid, crawl_component_code)

            if component is None:
                insert_or_update = 0

                uuid = spcap_data.make_uuid(b2c_kiid)
                cmp_version = 1
                #
            else:
                insert_or_update = 1
                uuid = component[28]
                cmp_old_version = component[21]
                if cmp_old_version is None:
                    cmp_version = 1
                else:
                    try:
                        int(cmp_old_version)
                        cmp_version = cmp_old_version + 1
                    except:
                        cmp_version = 1
                spcap_data.delete_old_component(uuid)

            # 保存component并返回id
            component_id = spcap_data.save_to_component(crawl_component_code, b2c_kiid, b2c_brid, uuid,
                                                        crawl_component_attach, crawl_component_img,
                                                        version=cmp_version)
            # 更新爬虫表返回uuid
            #
            crawl_base_properties = spcap_data.get_single_properties(crawl_component_id)
            properties_json = []
            cc_modify = 0
            for base_property in base_properties:
                # 对value值进行分析处理
                property_value_modify = PropertyValueModify()

                base_property_detno = base_property['detno']
                try:
                    aim_property_name = base_property['name']
                except:
                    aim_property_name = ''
                # 判断是否为多个单位
                try:
                    base_property_unit_list = base_property['unit'].split(",")
                    if len(base_property_unit_list) == 1:
                        base_property_unit = base_property_unit_list[0]
                except:
                    base_property_unit = ''
                base_property_id = base_property['property']['id']
                base_property_name = base_property['property']['labelCn']
                try:
                    base_property_type = base_property['type']
                except:
                    base_property_type = ''

                for crawl_property in crawl_base_properties:
                    crawl_property_name = crawl_property[5]

                    crawl_property_value = crawl_property[7]
                    if not crawl_property_value:
                        continue
                    # 目标类目匹配
                    if crawl_property_name.lower().replace(" ", "") in aim_property_name.lower().replace(" ", ""):

                        """ 这里还需要对不同属性值进行处理 """
                        # F类型
                        if base_property_type == 'F':
                            # 尝试解析成min、max
                            flag = property_value_modify.double_without_unit(crawl_property_value)
                            if flag:
                                pv_min, pv_max = flag.group(1), flag.group(2)
                                save_value = pv_min + base_property_unit + '~' + pv_max + base_property_unit
                                pv_id = spcap_data.save_to_property(base_property_id, component_id, base_property_detno,
                                                                    "'" + save_value + "'", pv_max=pv_max,
                                                                    pv_min=pv_min,
                                                                    pv_unit="'" + base_property_unit + "'")
                                property_json = spcap_data.get_property_json(base_property_detno, pv_id,
                                                                             base_property_id,
                                                                             base_property_name, save_value,
                                                                             min=pv_min, max=pv_max,
                                                                             unit=base_property_unit)
                            else:
                                # 为数值类型
                                try:
                                    crawl_property_value1 = crawl_property_value.replace(base_property_unit, "").strip()
                                    numberic = float(crawl_property_value1)
                                    save_value = crawl_property_value + base_property_unit

                                    pv_id = spcap_data.save_to_property(base_property_id, component_id,
                                                                        base_property_detno,
                                                                        "'" + save_value + "'",
                                                                        pv_numberic=crawl_property_value,
                                                                        pv_unit="'" + base_property_unit + "'")
                                    property_json = spcap_data.get_property_json(base_property_detno, pv_id,
                                                                                 base_property_id,
                                                                                 base_property_name, save_value,
                                                                                 numberic=crawl_property_value,
                                                                                 unit=base_property_unit)
                                except:
                                    # value为空的状态
                                    if crawl_property_value == '' or crawl_property_value == '-':
                                        pv_id = spcap_data.save_to_property(base_property_id, component_id,
                                                                            base_property_detno,
                                                                            "'" + crawl_property_value + "'",
                                                                            pv_unit="'" + base_property_unit + "'",
                                                                            pv_flag=12)
                                        property_json = spcap_data.get_property_json(base_property_detno, pv_id,
                                                                                     base_property_id,
                                                                                     base_property_name,
                                                                                     crawl_property_value,
                                                                                     unit=base_property_unit)
                                    # 无法处理
                                    else:
                                        pv_id = spcap_data.save_to_property(base_property_id, component_id,
                                                                            base_property_detno,
                                                                            "'" + crawl_property_value + "'",
                                                                            pv_unit="'" + base_property_unit + "'",
                                                                            pv_flag=11)
                                        cc_modify = 1
                                        property_json = spcap_data.get_property_json(base_property_detno, pv_id,
                                                                                     base_property_id,
                                                                                     base_property_name,
                                                                                     crawl_property_value,
                                                                                     unit=base_property_unit)
                            properties_json.append(property_json)
                            break
                        if base_property_type == 'N':
                            # 尝试将value转化为int，存入numberic值中
                            try:
                                crawl_property_value1 = crawl_property_value.replace(base_property_unit, "").strip()
                                numberic = float(crawl_property_value1)
                                save_value = crawl_property_value + base_property_unit

                                pv_id = spcap_data.save_to_property(base_property_id, component_id, base_property_detno,
                                                                    "'" + save_value + "'",
                                                                    pv_numberic=crawl_property_value,
                                                                    pv_unit="'" + base_property_unit + "'")
                                property_json = spcap_data.get_property_json(base_property_detno, pv_id,
                                                                             base_property_id,
                                                                             base_property_name, save_value,
                                                                             numberic=crawl_property_value,
                                                                             unit=base_property_unit)
                            except:
                                # N类型数值加单位
                                single_unit_flag = property_value_modify.single_with_unit(crawl_property_value)
                                if single_unit_flag:
                                    str_numberic = single_unit_flag.group(1)
                                    crawl_unit = single_unit_flag.group(3)
                                    # 单位超过一个
                                    if len(base_property_unit_list) > 1:
                                        for rough_base_property_unit in base_property_unit_list:
                                            if crawl_unit.lower() in rough_base_property_unit.lower():
                                                base_property_unit = rough_base_property_unit
                                                save_value = str_numberic + rough_base_property_unit
                                                pv_id = spcap_data.save_to_property(base_property_id, component_id,
                                                                                    base_property_detno,
                                                                                    "'" + save_value + "'",
                                                                                    pv_numberic=str_numberic,
                                                                                    pv_unit="'" + rough_base_property_unit + "'")
                                                property_json = spcap_data.get_property_json(base_property_detno, pv_id,
                                                                                             base_property_id,
                                                                                             base_property_name,
                                                                                             save_value,
                                                                                             numberic=str_numberic,
                                                                                             unit=rough_base_property_unit)
                                                break

                                        else:
                                            print("出现异常")

                                    # 只有一个单位
                                    else:
                                        if crawl_unit.lower() in base_property_unit.lower():
                                            save_value = str_numberic + base_property_unit
                                            pv_id = spcap_data.save_to_property(base_property_id, component_id,
                                                                                base_property_detno,
                                                                                "'" + save_value + "'",
                                                                                pv_numberic=str_numberic,
                                                                                pv_unit="'" + base_property_unit + "'")
                                            property_json = spcap_data.get_property_json(base_property_detno, pv_id,
                                                                                         base_property_id,
                                                                                         base_property_name,
                                                                                         save_value,
                                                                                         numberic=str_numberic,
                                                                                         unit=base_property_unit)

                                else:
                                    # N类型范围值
                                    flag = property_value_modify.double_without_unit(crawl_property_value)
                                    if flag:
                                        if abs(float(flag.group(1))) == abs(float(flag.group(2))):
                                            save_value = '+/-' + flag.group(2)
                                            numberic = flag.group(2)
                                            pv_id = spcap_data.save_to_property(base_property_id, component_id,
                                                                                base_property_detno,
                                                                                "'" + save_value + "'",
                                                                                pv_unit="'" + base_property_unit + "'",
                                                                                pv_numberic=numberic)
                                            property_json = spcap_data.get_property_json(base_property_detno, pv_id,
                                                                                         base_property_id,
                                                                                         base_property_name,
                                                                                         save_value,
                                                                                         unit=base_property_unit,
                                                                                         numberic=numberic)
                                        # N类型无法处理范围值
                                        else:
                                            pv_id = spcap_data.save_to_property(base_property_id, component_id,
                                                                                base_property_detno,
                                                                                "'" + crawl_property_value + "'",
                                                                                pv_unit="'" + base_property_unit + "'",
                                                                                pv_flag=11)
                                            cc_modify = 1
                                            property_json = spcap_data.get_property_json(base_property_detno, pv_id,
                                                                                         base_property_id,
                                                                                         base_property_name,
                                                                                         crawl_property_value,
                                                                                         unit=base_property_unit)
                                    # N类型非正常数据
                                    else:
                                        # 如果为空
                                        if crawl_property_value == '' or crawl_property_value == '-':
                                            pv_id = spcap_data.save_to_property(base_property_id, component_id,
                                                                                base_property_detno,
                                                                                "'" + crawl_property_value + "'",
                                                                                pv_unit="'" + base_property_unit + "'",
                                                                                pv_flag=12)
                                            property_json = spcap_data.get_property_json(base_property_detno, pv_id,
                                                                                         base_property_id,
                                                                                         base_property_name,
                                                                                         crawl_property_value,
                                                                                         unit=base_property_unit)
                                        # 无法处理
                                        else:
                                            pv_id = spcap_data.save_to_property(base_property_id, component_id,
                                                                                base_property_detno,
                                                                                "'" + crawl_property_value + "'",
                                                                                pv_unit="'" + base_property_unit + "'",
                                                                                pv_flag=11)
                                            cc_modify = 1
                                            property_json = spcap_data.get_property_json(base_property_detno, pv_id,
                                                                                         base_property_id,
                                                                                         base_property_name,
                                                                                         crawl_property_value,
                                                                                         unit=base_property_unit)
                            properties_json.append(property_json)
                            break
                        else:
                            pv_id = spcap_data.save_to_property(base_property_id, component_id,
                                                                base_property_detno,
                                                                "'" + crawl_property_value + "'",
                                                                pv_unit="'" + base_property_unit + "'",
                                                                pv_flag=10)
                            property_json = spcap_data.get_property_json(base_property_detno, pv_id,
                                                                         base_property_id,
                                                                         base_property_name,
                                                                         crawl_property_value,
                                                                         unit=base_property_unit)
                            properties_json.append(property_json)
                            break


                else:
                    pv_id = spcap_data.save_to_property(base_property_id, component_id, base_property_detno, 'null')
                    # property_json = spcap_data.get_property_json(base_property_detno, pv_id, base_property_id, base_property_name, '')

            if not cc_flag:
                cc_flag = insert_or_update
            spcap_data.update_crawl_uuid(uuid, task_id, crawl_component_code, cc_flag=cc_flag,
                                         cc_modify=cc_modify)
            str_properties_json = str(properties_json).replace("'", "\"")
            spcap_data.save_to_version(crawl_component_code, crawl_component_attach, crawl_component_img, unit, uuid,
                                       str_properties_json, b2c_brand_json, b2c_kind_json, cmp_version)
            spcap_data.conn.commit()
            print("come on")


if __name__ == "__main__":
    main = DataProcessing()
    main.go(29)
