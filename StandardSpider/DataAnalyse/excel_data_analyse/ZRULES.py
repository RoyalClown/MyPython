"""
    @description:
    @author:        RoyalClown
    @date:          2016/12/7
"""

# 最大值最小值合并
"""
# 获取最小值
if crawl_property_name == "Operating Temperature (Min.)[°C]" or crawl_property_name == "Storage Temperature (Min.)[°C]":
    tmp_pv_min = crawl_property_value
    if tmp_pv_max != '':
        pv_min = tmp_pv_min
        pv_max = tmp_pv_max
        save_value = pv_min + base_property_unit + '~' + pv_max + base_property_unit
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
# 获取最大值
elif crawl_property_name == "Operating Temperature (Max.)[°C]" or crawl_property_name == "Storage Temperature (Max.)[°C]":
    tmp_pv_max = crawl_property_value
    if tmp_pv_max != '':
        pv_min = tmp_pv_min
        pv_max = tmp_pv_max
        save_value = pv_min + base_property_unit + '~' + pv_max + base_property_unit
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
# 储存为范围值
"""

# 三个值合并
"""
# 获取最小值
if crawl_property_name == "Supply Voltage (V) min":
    tmp_voltage_min = crawl_property_value
    if tmp_voltage_max != '':
        pv_min = tmp_voltage_min
        pv_max = tmp_voltage_max
        save_value = pv_min + base_property_unit + '~' + pv_max + base_property_unit
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
# 获取典型值
elif crawl_property_name == "Supply Voltage (V) typ":
    tmp_voltage_typ = crawl_property_value
    if tmp_voltage_max != '':
        pv_min = tmp_voltage_min.split(",")[0]
        pv_max = tmp_voltage_max.split(",")[0]
        pv_typ = tmp_voltage_typ
        save_value = pv_min + base_property_unit + '~' + pv_max + base_property_unit + "," + tmp_voltage_typ
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
# 获取最大值
elif crawl_property_name == "Supply Voltage (V) max":
    tmp_voltage_max = crawl_property_value
    if tmp_voltage_min != '':
        pv_min = tmp_voltage_min.split(",")[0]
        pv_max = tmp_voltage_max.split(",")[0]
        save_value = pv_min + base_property_unit + '~' + pv_max + base_property_unit + "," + tmp_voltage_typ
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


"""