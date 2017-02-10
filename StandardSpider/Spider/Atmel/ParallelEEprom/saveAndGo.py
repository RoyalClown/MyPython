"""
    @description:   
    @author:        RoyalClown
    @date:          2016/11/25
"""
from DBSave.oracleSave import OracleSave
from Spider.Atmel.ParallelEEprom.productList import Detail, ProductList


def db_save(component, many_properties, task_code, task_id):

    orcl_conn = OracleSave(task_code, task_id)
    try:
        orcl_conn.component_insert(component)
    except Exception as e:
        print(e)

    for properties in many_properties:
        try:
            orcl_conn.properties_insert(properties)
        except Exception as e:
            print(e)
    orcl_conn.commit()
    orcl_conn.conn.close()


def all_go(task_code, task_id):
    product_list = ProductList()
    imgs_urls = product_list.get_product_url()

    # threading_pool = ThreadingPool()
    # threading_pool.multi_thread(db_save, detail_urls)

    for img_url in imgs_urls:
        detail = Detail(img_url)
        component_properties_list = detail.get_component_list()
        for component_properties in component_properties_list:
            db_save(component_properties[0], component_properties[1], task_code, task_id)
