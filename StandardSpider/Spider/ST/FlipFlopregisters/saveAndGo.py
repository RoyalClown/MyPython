"""
    @description:   
    @author:        RoyalClown
    @date:          2016/11/30
"""
from DBSave.oracleSave import OracleSave
from Spider.ST.FlipFlopregisters.productList import Detail, ProductList


def db_save(product_json, task_code, task_id):
    detail_attributes = Detail(product_json)
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
    orcl_conn.conn.close()


def all_go(task_code, task_id):
    product_list = ProductList()
    products_json = product_list.get_product_list()

    # threading_pool = ThreadingPool()
    # threading_pool.multi_thread(db_save, detail_urls)

    for product_json in products_json:
        db_save(product_json, task_code, task_id)
