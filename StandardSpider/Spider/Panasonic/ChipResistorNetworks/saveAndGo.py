"""
    @description:   
    @author:        RoyalClown
    @date:          2016/12/14
"""
from DBSave.oracleSave import OracleSave
from Spider.Panasonic.ChipResistorNetworks.listProducts import ProductList, Detail


def db_save(product, task_code, task_id):
    detail_attributes = Detail(product)
    component = detail_attributes.get_component(kiname="片式电阻电路",
                                                attach="https://industrial.panasonic.cn/cdbs/www-data/pdf/AOC0000/AOC0000C4.pdf",
                                                img="https://industrial.panasonic.cn/cdbs/www-data/gif/AOC0000/AOC0000SC3.gif")
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
           url="https://industrial.panasonic.cn/ea/products/resistors/resistor-network-array/resistor-network-array/chip-resistor-networks?reset=1&limit=100"):
    product_list = ProductList()
    products = product_list.get_products_list(url)
    for product in products:
        db_save(product, task_code, task_id)
