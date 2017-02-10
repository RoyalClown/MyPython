from DataAnalyse.dbDataGet.ST_data import UtilDataAnalyse
from DataAnalyse.valueProcessing.propertyValueModify import PropertyValueModify


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
            crawl_component_code = crawl_component[7].strip()
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

                # 参数合并
                tmp_two_first0 = ''
                tmp_two_second0 = ''

                for crawl_property in crawl_base_properties:
                    crawl_property_name = crawl_property[5]

                    crawl_property_value = crawl_property[7]
                    if not crawl_property_value:
                        continue
                    # 目标类目匹配
                    if crawl_property_name.lower().replace(" ", "") in aim_property_name.lower().replace(" ", ""):


                        # 储存为范围值
                        # 获取最小值
                        if crawl_property_name == "Die Size (X)":
                            tmp_two_first0 = crawl_property_value.replace("mm", "").strip()
                            continue
                        # 获取最大值
                        elif crawl_property_name == "Die Size (Y)":
                            tmp_two_second0 = crawl_property_value.replace("mm", "").strip()
                            if tmp_two_first0 != '':
                                pv_min = tmp_two_first0
                                pv_max = tmp_two_second0
                                save_value = pv_min + "mm*" + pv_max + "mm"
                                pv_id = spcap_data.save_to_property(base_property_id, component_id,
                                                                    base_property_detno,
                                                                    "'" + save_value + "'", pv_max=pv_max,
                                                                    pv_min=pv_min,
                                                                    pv_unit="'" + base_property_unit + "'")
                                property_json = spcap_data.get_property_json(base_property_detno, pv_id,
                                                                             base_property_id,
                                                                             base_property_name, save_value,
                                                                             min=pv_min, max=pv_max,
                                                                             unit=base_property_unit)
                                properties_json.append(property_json)
                                break
                            else:
                                continue
                        if crawl_property_name == 'Operating Temperature min':
                            try:
                                flag = property_value_modify.double_with_unit(crawl_property_value)
                                pv_min = flag.group(1)
                                save_value = pv_min + base_property_unit
                                pv_id = spcap_data.save_to_property(base_property_id, component_id, base_property_detno,
                                                                    "'" + save_value + "'",
                                                                    pv_min=pv_min,
                                                                    pv_unit="'" + base_property_unit + "'")
                                property_json = spcap_data.get_property_json(base_property_detno, pv_id,
                                                                             base_property_id,
                                                                             base_property_name, save_value,
                                                                             min=pv_min,
                                                                             unit=base_property_unit)
                                properties_json.append(property_json)
                                break
                            except:
                                continue

                        """ 这里还需要对不同属性值进行处理 """
                        # F类型
                        if base_property_type == 'F':
                            # 尝试解析成min、max
                            flag = property_value_modify.double_without_unit(crawl_property_value)
                            flag1 = property_value_modify.double_with_unit(crawl_property_value)
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
                            elif flag1:
                                pv_min, pv_max = flag1.group(1), flag1.group(6)
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
                                                                    pv_min=crawl_property_value,
                                                                    pv_unit="'" + base_property_unit + "'")
                                property_json = spcap_data.get_property_json(base_property_detno, pv_id,
                                                                             base_property_id,
                                                                             base_property_name, save_value,
                                                                             min=crawl_property_value,
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

                                        else:
                                            print("出现异常")

                                    # 只有一个单位
                                    else:
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