"""
    @description:   
    @author:        RoyalClown
    @date:          2016/11/17
"""

from DBSave.oracleSave import OracleSave
from Spider.Rohm.VoltageRegulator.DDR_SDRAM.productList import Detail, ProductList


def db_save(url, task_code, task_id):
    detail_attributes = Detail(url)
    component = detail_attributes.get_component()

    orcl_conn = OracleSave(task_code, task_id)
    try:
        orcl_conn.component_insert(component)
    except Exception as e:
        print(e)

    many_properties = detail_attributes.get_base_attributes()

    for properties in many_properties:
        try:
            orcl_conn.properties_insert(properties)
        except Exception as e:
            print(e)
    orcl_conn.commit()


def all_go(task_code, task_id):
    product_list = ProductList()
    detail_urls = product_list.get_urls_pdfs()

    # threading_pool = ThreadingPool()
    # threading_pool.multi_thread(db_save, detail_urls)

    for detail_url in detail_urls:
        db_save(detail_url, task_code, task_id)
