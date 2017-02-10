"""
    @description:   
    @author:        RoyalClown
    @date:          2016/11/14
"""
from DBSave.oracleSave import OracleSave
from Spider.Azurewave.ModuleIC.detailAttributes import DetailAttributes


def db_save(product_tag, img_tag, task_code, task_id):
    detail_attributes = DetailAttributes()
    component = detail_attributes.get_components(product_tag, img_tag)
    try:
        orcl_conn = OracleSave(task_code, task_id)
        orcl_conn.component_insert(component)

        many_properties = detail_attributes.get_attributes(product_tag)
        for properties in many_properties:
            orcl_conn.properties_insert(properties)
            orcl_conn.commit()
    except Exception as e:
        print(e)


def all_go(task_code, task_id):
    product_list = DetailAttributes()
    products_tags, img_tags = product_list.get_product_list()

    # threading_pool = ThreadingPool()
    # threading_pool.multi_thread(db_save, detail_urls)

    for product_tag, img_tag in zip(products_tags, img_tags):
        db_save(product_tag, img_tag, task_code, task_id)


if __name__ == "__main__":
    all_go("0", 0)
