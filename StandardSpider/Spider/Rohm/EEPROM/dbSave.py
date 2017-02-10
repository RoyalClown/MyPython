"""
    @description:   
    @author:        RoyalClown
    @date:          2016/11/14
"""
from DBSave.oracleSave import OracleSave
from Spider.Rohm.EEPROM.detailAttributes import DetailAttributes
from Spider.Rohm.EEPROM.productlist import ProductList


def db_save(url, task_code, task_id):
    detail_attributes = DetailAttributes(url)
    component = detail_attributes.get_component()
    try:
        orcl_conn = OracleSave(task_code, task_id)
        orcl_conn.component_insert(component)

        many_properties = detail_attributes.get_base_attributes()
        for properties in many_properties:
            orcl_conn.properties_insert(properties)
            orcl_conn.commit()
    except Exception as e:
        print(e)


def all_go(task_code, task_id):
    product_list = ProductList()
    detail_urls = product_list.get_urls_pdfs()

    # threading_pool = ThreadingPool()
    # threading_pool.multi_thread(db_save, detail_urls)

    for detail_url in detail_urls:
        db_save(detail_url, task_code, task_id)


if __name__ == "__main__":
    all_go("0", 0)
