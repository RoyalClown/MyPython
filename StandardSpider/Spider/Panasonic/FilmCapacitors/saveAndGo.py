"""
    @description:   
    @author:        RoyalClown
    @date:          2016/12/6
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


def all_go(task_code, task_id, url="https://industrial.panasonic.cn/ea/products/capacitors/film-capacitors/film-cap-electroequip#quicktabs-line_up_page_tab=1"):
    product_list = ProductList()
    series_urls = product_list.get_series_urls(url)
    for series_url in series_urls:
        codes_urls = product_list.get_code_urls(series_url)
        for code_url in codes_urls:
            db_save(code_url, task_code, task_id)
