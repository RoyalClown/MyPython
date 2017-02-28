"""
    @description:   
    @author:        RoyalClown
    @date:          2017/2/16
"""
from Components.DBSAVE.oracleSave import OracleSave
from Components.MLCC1.detail import MLCC1Detail
from Components.MLCC1.getUrls import GetUrls
from Lib.Currency.ThreadingPool import ThreadingPool


class AllInteraction:
    def __init__(self):
        pass

    def thread_go(self, page_url):
        many_components_properties = self.detail.get_page_components(page_url)
        for component_properties in many_components_properties:
            component, single_properties = component_properties
            while True:
                try:
                    orcl_conn = OracleSave(1111111)

                    orcl_conn.component_insert(component)

                    for properties in single_properties:
                        orcl_conn.properties_insert(properties)
                    orcl_conn.commit()
                    orcl_conn.conn.close()
                except Exception as e:
                    print(e, "存储错误")
        return

    def all_go(self):
        get_urls = GetUrls()
        first_classes = get_urls.get_first_classes()
        for first_class in first_classes:
            second_classes = get_urls.get_second_classes(first_class)
            for second_class in second_classes:
                self.detail = MLCC1Detail(second_class)
                page_urls = self.detail.get_class_components()

                threadingpool = ThreadingPool(800)
                threadingpool.multi_process(self.thread_go, page_urls)

if __name__ == "__main__":
    all_i = AllInteraction()
    all_i.all_go()
