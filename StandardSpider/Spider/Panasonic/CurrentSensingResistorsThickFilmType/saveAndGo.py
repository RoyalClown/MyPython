"""
    @description:   
    @author:        RoyalClown
    @date:          2016/12/12
"""
from DBSave.oracleSave import OracleSave
from Spider.Panasonic.productList import ProductList, Detail


def db_save(url, task_code, task_id):
    detail_attributes = Detail(url)
    component = detail_attributes.get_component()
    try:
        orcl_conn = OracleSave(task_code, task_id)
        orcl_conn.component_insert(component)

        many_properties = detail_attributes.get_properties()
        for properties in many_properties:
            orcl_conn.properties_insert(properties)
        orcl_conn.commit()
    except Exception as e:
        print(e)


def all_go(task_code, task_id, url="https://industrial.panasonic.cn/ea/products/resistors/chip-resistors/chip-resistors/current-sensing-resistors-thick-film-type?reset=1&limit=100"):
    product_list = ProductList()
    codes_urls = product_list.get_code_urls(url)
    for code_url in codes_urls:
        db_save(code_url, task_code, task_id)

