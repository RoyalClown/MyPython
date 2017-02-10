"""
    @description:   
    @author:        RoyalClown
    @date:          2016/12/14
"""
from DBSave.oracleSave import OracleSave
from Spider.Panasonic.listProducts import ProductList, Detail


def db_save(product, task_code, task_id):
    detail_attributes = Detail(product)
    component = detail_attributes.get_component(kiname="低电阻金属板片式电阻器　用于电流检测(MP型)",
                                                attach="https://industrial.panasonic.cn/cdbs/www-data/pdf/RDA0000/AOA0000C265.pdf",
                                                img="https://industrial.panasonic.cn/cdbs/www-data/gif/RDA0000/AOA0000SC100.JPG")
    try:
        orcl_conn = OracleSave(task_code, task_id)
        orcl_conn.component_insert(component)

        many_properties = detail_attributes.get_properties()
        for properties in many_properties:
            orcl_conn.properties_insert(properties)
        orcl_conn.commit()
    except Exception as e:
        print(e)


def all_go(task_code, task_id,
           url="https://industrial.panasonic.cn/ea/products/resistors/chip-resistors/chip-resistors/current-sensing-resistors-metal-plate-type-mp?reset=1&limit=100"):
    product_list = ProductList()
    products = product_list.get_products_list(url)
    for product in products:
        db_save(product, task_code, task_id)
