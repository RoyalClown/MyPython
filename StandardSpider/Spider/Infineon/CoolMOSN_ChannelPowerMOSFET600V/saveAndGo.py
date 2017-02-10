"""
    @description:   
    @author:        RoyalClown
    @date:          2016/12/9
"""
from DBSave.oracleSave import OracleSave
from Spider.Infineon.CoolMOSN_ChannelPowerMOSFET600V.productList import Detail, ProductList


def db_save(product_url, task_code, task_id):
    detail_attributes = Detail(product_url)
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
    products_url = product_list.get_product_list()

    # threading_pool = ThreadingPool()
    # threading_pool.multi_thread(db_save, detail_urls)

    for product_url in products_url:
        db_save(product_url, task_code, task_id)
