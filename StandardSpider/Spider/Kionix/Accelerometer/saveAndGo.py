"""
    @description:   
    @author:        RoyalClown
    @date:          2016/11/17
"""
from DBSave.oracleSave import OracleSave
from Spider.Kionix.Accelerometer.productList import Detail, ProductList


def db_save(url, single_json, task_code, task_id):
    detail_attributes = Detail(url, single_json)
    component = detail_attributes.get_component()

    orcl_conn = OracleSave(task_code, task_id)
    try:
        orcl_conn.component_insert(component)
    except Exception as e:
        print(e)

    many_properties = detail_attributes.get_attributes()

    for properties in many_properties:
        try:
            orcl_conn.properties_insert(properties)
        except Exception as e:
            print(e)
    orcl_conn.commit()


def all_go(task_code, task_id):
    product_list = ProductList()
    detail_url, productlist_json = product_list.get_product_list()

    for single_json in productlist_json:
        db_save(detail_url, single_json, task_code, task_id)
